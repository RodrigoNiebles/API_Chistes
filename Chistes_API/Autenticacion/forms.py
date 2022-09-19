'''
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from . import devices_for_user, match_token
from .models import Device, VerifyNotAllowed



class OTPAuthenticationFormMixin:
    otp_error_messages = {
        'token_required': _('Please enter your OTP token.'),
        'challenge_exception': _('Error generating challenge: {0}'),
        'not_interactive': _('The selected OTP device is not interactive'),
        'challenge_message': _('OTP Challenge: {0}'),
        'invalid_token': _('Invalid token. Please make sure you have entered it correctly.'),
        'n_failed_attempts': ngettext_lazy(
            "Verification temporarily disabled because of %(failure_count)d failed attempt, please try again soon.",
            "Verification temporarily disabled because of %(failure_count)d failed attempts, please try again soon.",
            "failure_count"),
        'verification_not_allowed': _("Verification of the token is currently disabled"),
    }

    def clean_otp(self, user):
        if user is None:
            return

        validation_error = None
        with transaction.atomic():
            try:
                device = self._chosen_device(user)
                token = self.cleaned_data.get('otp_token')

                user.otp_device = None

                try:
                    if self.cleaned_data.get('otp_challenge'):
                        self._handle_challenge(device)
                    elif token:
                        user.otp_device = self._verify_token(user, token, device)
                    else:
                        raise forms.ValidationError(self.otp_error_messages['token_required'], code='token_required')
                finally:
                    if user.otp_device is None:
                        self._update_form(user)
            except forms.ValidationError as e:
                # Validation errors shouldn't abort the transaction, so we have
                # to carefully transport them out.
                validation_error = e

        if validation_error:
            raise validation_error


    def _chosen_device(self, user):
        device_id = self.cleaned_data.get('otp_device')

        if device_id:
            device = Device.from_persistent_id(device_id, for_verify=True)
        else:
            device = None 

        if (device is not None) and (device.user_id != user.pk):
            device = None

        return device

    def _handle_challenge(self, device):
        try:
            challenge = device.generate_challenge() if (device is not None) else None
        except Exception as e:
            raise forms.ValidationError(
                self.otp_error_messages['challenge_exception'].format(e), code='challenge_exception'
            )
        else:
            if challenge is None:
                raise forms.ValidationError(self.otp_error_messages['not_interactive'], code='not_interactive')
            else:
                raise forms.ValidationError(
                    self.otp_error_messages['challenge_message'].format(challenge), code='challenge_message'
                )

    def _verify_token(self, user, token, device=None):
        if device is not None:
            verify_is_allowed, extra = device.verify_is_allowed()
            if not verify_is_allowed:
                # Try to match specific conditions we know about.
                if ('reason' in extra and extra['reason'] == VerifyNotAllowed.N_FAILED_ATTEMPTS):
                    raise forms.ValidationError(self.otp_error_messages['n_failed_attempts'] % extra)
                if 'error_message' in extra:
                    raise forms.ValidationError(extra['error_message'])
                # Fallback to generic message otherwise.
                raise forms.ValidationError(self.otp_error_messages['verification_not_allowed'])

            device = device if device.verify_token(token) else None
        else:
            device = match_token(user, token)

        if device is None:
            raise forms.ValidationError(self.otp_error_messages['invalid_token'], code='invalid_token')

        return device

    def _update_form(self, user):
        if 'otp_device' in self.fields:
            self.fields['otp_device'].widget.choices = self.device_choices(user)

        if 'password' in self.fields:
            self.fields['password'].widget.render_value = True

    @staticmethod
    def device_choices(user):
        return list((d.persistent_id, d.name) for d in devices_for_user(user))               


class OTPAuthenticationForm(OTPAuthenticationFormMixin, AuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.Select)
    otp_token = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    
    otp_challenge = forms.CharField(required=False)

    def clean(self):
        self.cleaned_data = super().clean()
        self.clean_otp(self.get_user())

        return self.cleaned_data        



class OTPTokenForm(OTPAuthenticationFormMixin, forms.Form):
    otp_device = forms.ChoiceField(choices=[])
    otp_token = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    otp_challenge = forms.CharField(required=False)

    def __init__(self, user, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.fields['otp_device'].choices = self.device_choices(user)

    def clean(self):
        super().clean()

        self.clean_otp(self.user)

        return self.cleaned_data

    def get_user(self):
        return self.user        

'''

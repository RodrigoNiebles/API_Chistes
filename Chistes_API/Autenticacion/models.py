'''
from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from .util import random_number_token


class DeviceManager(models.Manager):
    def devices_for_user(self, user, confirmed=None):
        devices = self.model.objects.filter(user=user)
        if confirmed is not None:
            devices = devices.filter(confirmed=bool(confirmed))

        return devices

class Device(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), help_text="The user that this device belongs to.", on_delete=models.CASCADE)
    name = models.CharField(max_length=64, help_text="The human-readable name of this device.")
    confirmed = models.BooleanField(default=True, help_text="Is this device ready for use?")

    objects = DeviceManager()

    class Meta:
        abstract = True

    def __str__(self):
        try:
            user = self.user
        except ObjectDoesNotExist:
            user = None

        return "{0} ({1})".format(self.name, user)

    @property
    def persistent_id(self):
        return '{0}/{1}'.format(self.model_label(), self.id)


    @classmethod
    def model_label(cls):    
        return '{0}.{1}'.format(cls._meta.app_label, cls._meta.model_name) 

    @classmethod
    def from_persistent_id(cls, persistent_id, for_verify=False):    
        device = None

        try:
            model_label, device_id = persistent_id.rsplit('/', 1)
            app_label, model_name = model_label.split('.')

            device_cls = apps.get_model(app_label, model_name)
            if issubclass(device_cls, Device):
                device_set = device_cls.objects.filter(id=int(device_id))
                if for_verify:
                    device_set = device_set.select_for_update()
                device = device_set.first()
        except (ValueError, LookupError):
            pass

        return device

    def is_interactive(self):  
        return not hasattr(self.generate_challenge, 'stub')
        

    def generate_challenge(self):    
        return None

    generate_challenge.stub = True


    def verify_is_allowed(self):
        return (True, None)


    def verify_token(self, token):
        return False



class SideChannelDevice(Device):  
    token = models.CharField(max_length=16, blank=True, null=True)
    valid_until = models.DateTimeField(
        default=timezone.now,
        help_text="The timestamp of the moment of expiry of the saved token."
    )

    class Meta:
        abstract = True

    def generate_token(self, length=6, valid_secs=300, commit=True):

        self.token = random_number_token(length)
        self.valid_until = timezone.now() + timedelta(seconds=valid_secs)
        if commit:
            self.save()

    def verify_token(self, token):        
        _now = timezone.now()

        if (self.token is not None) and (token == self.token) and (_now < self.valid_until):
            self.token = None
            self.valid_until = _now
            self.save()

            return True
        else:
            return False


class VerifyNotAllowed:
    N_FAILED_ATTEMPTS = 'N_FAILED_ATTEMPTS'



class ThrottlingMixin(models.Model):
    throttling_failure_timestamp = models.DateTimeField(
        null=True, blank=True, default=None,
        help_text="A timestamp of the last failed verification attempt. Null if last attempt succeeded."
    )
    throttling_failure_count = models.PositiveIntegerField(
        default=0, help_text="Number of successive failed attempts."
    )

    def verify_is_allowed(self):
        if (self.throttling_enabled and
                self.throttling_failure_count > 0 and
                self.throttling_failure_timestamp is not None):
            now = timezone.now()
            delay = (now - self.throttling_failure_timestamp).total_seconds()
            # Required delays should be 1, 2, 4, 8 ...
            delay_required = self.get_throttle_factor() * (2 ** (self.throttling_failure_count - 1))
            if delay < delay_required:
                return (False,
                        {'reason': VerifyNotAllowed.N_FAILED_ATTEMPTS,
                         'failure_count': self.throttling_failure_count,
                         'locked_until': self.throttling_failure_timestamp + timedelta(seconds=delay_required)}
                        )

        return super().verify_is_allowed()


    def throttle_reset(self, commit=True):
        self.throttling_failure_timestamp = None
        self.throttling_failure_count = 0
        if commit:
            self.save()


    def throttle_increment(self, commit=True):
        self.throttling_failure_timestamp = timezone.now()
        self.throttling_failure_count += 1
        if commit:
            self.save()


    @cached_property
    def throttling_enabled(self):
        return self.get_throttle_factor() > 0

    def get_throttle_factor(self):  # pragma: no cover
        raise NotImplementedError()

    class Meta:
        abstract = True        


'''        
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def valid_no(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )
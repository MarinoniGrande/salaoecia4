import functools
import gzip
import re
from difflib import SequenceMatcher
from pathlib import Path

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.functional import lazy
from django.utils.html import format_html, format_html_join
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _, ngettext


class MinimumLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, max_length=32):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "This password is too long. It must contain more than %(max_length)d character.",
                    "This password is too long. It must contain more than %(max_length)d characters.",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain  more than %(max_length)d characters.",
            "Your password must contain  more than %(max_length)d characters.",
            self.max_length
        ) % {'max_length': self.max_length}


class IsActiveValidator:
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self):
        pass

    def validate(self, user=None):
        if not user.is_active:
            raise ValidationError(
                ngettext(
                    "This user is not active.",
                    "This user is not active.",
                    number=19
                ),
                code='not_active',
                params={},
            )

    def get_help_text(self):
        return ngettext(
            "This user is not active.",
                    "This user is not active.", number=19
        )
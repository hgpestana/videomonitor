from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Camera(models.Model):
    """
    Camera table to be used by the Video Monitor platform.
    TODO: Develop this table
    """

    name = models.CharField('Name', max_length=255)
    description = models.TextField('Description', blank=True, null=True)
    comments = models.TextField('Comments', blank=True, null=True)
    vat = models.CharField('VAT', max_length=15, blank=True, null=True)
    url = models.CharField('URL', max_length=150, blank=True, null=True)
    created = models.DateTimeField('Created', default=now, blank=True, null=True)
    last_updated = models.DateTimeField('Last Updated', default=now, blank=True, null=True)
    is_visible = models.BooleanField('Is Visible')

    class Meta:
        # Translators: This string is used to identify the Client table name
        verbose_name = _('Camera')

        # Translators: This string is used to identify the Client table name in plural form
        verbose_name_plural = _('Cameras')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view', kwargs={'pk': self.pk})

from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from agent.models import Person

class RFIDCard(models.Model):
    class Meta:
        verbose_name = _("RFID Card")
        verbose_name_plural = _("RFID Cards")
        ordering = ['card_id']
    card_id = models.CharField(max_length=50, unique=True, verbose_name=_("Card ID"))
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='rfid_cards', verbose_name=_("Person"))
    valid_from = models.DateField(verbose_name=_("Valid From"), null=True, blank=True)
    valid_to = models.DateField(verbose_name=_("Valid To"), null=True, blank=True)

    def __str__(self):
        return f"{self.card_id} ({self.person})"

class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Permission Name"))

    def __str__(self):
        return self.name

class CardPermission(models.Model):
    card = models.ForeignKey(RFIDCard, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('card', 'permission')

class RFIDLog(models.Model):
    EVENT_CHOICES = [
    ('entry', _('Entry')),
    ('exit', _('Exit')),
    ('denied', _('Access Denied')),
]
    card = models.ForeignKey(RFIDCard, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
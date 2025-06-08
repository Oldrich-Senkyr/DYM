from django.db import models

# Create your models here.
from django.db import models

class IngestedData(models.Model):
    data = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IngestedData {self.id} at {self.received_at}"


from django.db import models
from django.utils.translation import gettext_lazy as _
from agent.models import Person


class CardEventType(models.TextChoices):
    ENTRY = "1", _("Entry")
    EXIT = "2", _("Exit")
    BREAK_START = "3", _("Break Start")
    DOOR_UNLOCK = "4", _("Door Unlock")
    # Lze doplňovat další typy událostí


class CardEvent(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="card_events",
        verbose_name=_("Person")
    )

    card_number = models.CharField(
        max_length=32,
        verbose_name=_("Card Number"),
        db_index=True
    )

    timestamp = models.DateTimeField(
        verbose_name=_("Timestamp")
    )

    date = models.DateField(
        verbose_name=_("Event Date"),
        db_index=True
    )

    time = models.TimeField(
        verbose_name=_("Event Time")
    )

    object_id = models.CharField(
        max_length=20,
        verbose_name=_("Object ID")
    )

    reader_id = models.CharField(
        max_length=20,
        verbose_name=_("Reader ID")
    )

    event_type = models.CharField(
        max_length=2,
        choices=CardEventType.choices,
        verbose_name=_("Event Type")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    class Meta:
        verbose_name = _("Card Event")
        verbose_name_plural = _("Card Events")
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.card_number} {self.timestamp} ({self.get_event_type_display()})"

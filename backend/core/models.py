from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import transaction
# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Reaction(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name
class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee",
    )
    employee_no = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=120)
    position = models.CharField(max_length=120, blank=True)
    group = models.CharField(max_length=120, blank=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees"
    )

    def __str__(self):
        return f"{self.employee_no} {self.first_name} {self.last_name}"
    
class SafetyWalk(models.Model):
    SHIFT_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    ]

    number = models.CharField(max_length=30, unique=True, blank=True)
    date = models.DateField(default=timezone.now)
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="safety_walks"
    )

    def __str__(self):
        return f"{self.number} ({self.date})"
    
    def save(self, *args, **kwargs):
        if not self.number:
            year = (self.date.year if self.date else timezone.now().year)
            prefix = f"SW-{year}-"
            with transaction.atomic():
                last = (
                    SafetyWalk.objects
                    .select_for_update()
                    .filter(number__startswith=prefix)
                    .order_by("-number")
                    .first()
                )
                last_seq = int(last.number.split("-")[-1]) if last and last.number else 0
                self.number = f"{prefix}{last_seq + 1:04d}"
        super().save(*args, **kwargs)

class Observation(models.Model):
    safety_walk = models.OneToOneField(
        SafetyWalk,
        on_delete=models.CASCADE,
        related_name="observation",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="observation",
    )

    # pola z Accessa (na start prosto)
    ppe = models.BooleanField(default=False)         # ŚOI
    work = models.BooleanField(default=False)        # Praca
    environment = models.BooleanField(default=False) # Środowisko

    reaction = models.ForeignKey(Reaction, on_delete=models.PROTECT, null=True, blank=True)
    comment = models.TextField(blank=True)                  # Komentarz

    def __str__(self):
        return f"Obs #{self.id} - {self.safety_walk.number}"


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class BrainArea(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    analogy = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} — {self.name}"


class Phase(models.Model):
    number = models.PositiveSmallIntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(6)])
    title = models.CharField(max_length=200)
    objective = models.TextField()
    protocol_instructions = models.TextField(blank=True, default='')
    primary_circuits = models.ManyToManyField(BrainArea, blank=True, related_name='phases')

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Fase {self.number}: {self.title}"


class TrainingMethod(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    protocol_steps = models.TextField()
    adaptation_flat_affect = models.TextField(blank=True, default='')
    implementable_in_app = models.BooleanField(default=False)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code}: {self.name}"


class Artwork(models.Model):
    EMOTIONAL_CATEGORIES = [
        ('A', 'Cat A — Sin dependencia emocional'),
        ('B', 'Cat B — Dependencia parcial'),
        ('C', 'Cat C — Alta dependencia emocional'),
    ]

    catalog_id = models.CharField(max_length=10, unique=True)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='artworks')
    order_standard = models.PositiveSmallIntegerField()
    order_flat_affect = models.PositiveSmallIntegerField(null=True, blank=True)
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    year = models.CharField(max_length=50)
    wikimedia_url = models.URLField(max_length=500)
    emotional_category = models.CharField(max_length=1, choices=EMOTIONAL_CATEGORIES, default='A')
    brain_areas = models.ManyToManyField(BrainArea, blank=True, related_name='artworks')
    training_purpose = models.TextField(blank=True, default='')
    instructions_standard = models.TextField(blank=True, default='')
    instructions_flat_affect = models.TextField(blank=True, default='')
    emotional_intensity_level = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(3)]
    )
    reexposure_prompt = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['phase__number', 'order_standard']

    def __str__(self):
        return f"{self.catalog_id}: {self.artist} — {self.title}"


class UserProfile(models.Model):
    MODE_CHOICES = [
        ('standard', 'Estándar'),
        ('flat_affect', 'Flat Affect (TEPT)'),
    ]

    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='standard')
    program_start_date = models.DateField(null=True, blank=True)
    current_phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True, blank=True)
    vviq_baseline = models.PositiveSmallIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and UserProfile.objects.exists():
            raise ValueError("Solo puede existir un UserProfile (singleton).")
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"Perfil — modo: {self.mode}"


class TrainingSession(models.Model):
    SESSION_TYPES = [
        ('standard', 'Sesión estándar'),
        ('image_streaming', 'Image Streaming'),
        ('free', 'Práctica libre'),
    ]

    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='standard')
    date = models.DateTimeField(auto_now_add=True)
    viewing_duration = models.PositiveIntegerField(default=0, help_text='Segundos de visualización')
    retention_duration = models.PositiveIntegerField(default=0, help_text='Segundos de retención')
    vividness_rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    stability_rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    detail_rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    emotional_response = models.TextField(blank=True, default='')
    emotional_indicator_detected = models.BooleanField(default=False)
    prosody_change_noted = models.BooleanField(default=False)
    body_reaction_noted = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Sesión {self.pk} — {self.artwork.catalog_id} ({self.date:%Y-%m-%d %H:%M})"

    @property
    def average_rating(self):
        ratings = [r for r in [self.vividness_rating, self.stability_rating, self.detail_rating] if r is not None]
        return sum(ratings) / len(ratings) if ratings else None


class FieldCapture(models.Model):
    CAPTURE_TYPES = [
        ('FFA', 'Rostro (FFA)'),
        ('EBA', 'Cuerpo (EBA)'),
        ('PPA', 'Lugar (PPA)'),
        ('OPA', 'Escena abierta (OPA)'),
        ('NAV', 'Navegación'),
        ('OBJ', 'Objeto (LOC)'),
        ('COLOR', 'Color (V4)'),
        ('MOTION', 'Movimiento (V5/MT)'),
        ('MULTI', 'Integración múltiple'),
        ('OTHER', 'Otro'),
    ]

    capture_type = models.CharField(max_length=10, choices=CAPTURE_TYPES)
    quality = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    description = models.TextField()
    eyes_open = models.BooleanField(default=True)
    in_motion = models.BooleanField(default=False)
    deliberate = models.BooleanField(default=True)
    immediate_retention = models.BooleanField(default=True)
    session_end_retention = models.BooleanField(null=True, blank=True)
    next_day_retention = models.BooleanField(null=True, blank=True)
    repetition_count = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Captura {self.capture_type} — {self.date:%Y-%m-%d %H:%M}"


class VVIQResponse(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(80)]
    )
    item_scores = models.JSONField(default=dict)
    context = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"VVIQ {self.total_score}/80 — {self.date:%Y-%m-%d}"

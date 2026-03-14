from django import forms
from .models import (
    TrainingSession, FieldCapture, VVIQResponse, UserProfile,
    Symbol, WorkspaceExercise, Capability,
)


class SessionStartForm(forms.Form):
    artwork_id = forms.IntegerField(widget=forms.HiddenInput())
    viewing_duration = forms.ChoiceField(
        choices=[(30, '30 segundos'), (60, '60 segundos'), (90, '90 segundos')],
        initial=60,
        label='Duración de visualización',
    )


class SessionAssessForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = [
            'vividness_rating', 'stability_rating', 'detail_rating',
            'emotional_response', 'emotional_indicator_detected',
            'prosody_change_noted', 'body_reaction_noted', 'notes',
        ]
        widgets = {
            'vividness_rating': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'stability_rating': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'detail_rating': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'emotional_response': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'vividness_rating': 'Viveza (1-10)',
            'stability_rating': 'Estabilidad (1-10)',
            'detail_rating': 'Detalle (1-10)',
            'emotional_response': 'Respuesta emocional',
            'emotional_indicator_detected': '¿Se detectó indicador emocional?',
            'prosody_change_noted': '¿Cambio de prosodia?',
            'body_reaction_noted': '¿Reacción corporal?',
            'notes': 'Notas',
        }


class FieldCaptureForm(forms.ModelForm):
    class Meta:
        model = FieldCapture
        fields = [
            'capture_type', 'quality', 'description', 'eyes_open',
            'in_motion', 'deliberate', 'immediate_retention',
            'repetition_count', 'notes',
            'text_content', 'text_format', 'readback_verified',
            'symbols_used', 'composition_layer_count', 'bounding_boxes_used',
        ]
        widgets = {
            'quality': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'text_content': forms.TextInput(attrs={'placeholder': 'Texto proyectado'}),
            'symbols_used': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'capture_type': 'Tipo de captura',
            'quality': 'Calidad (1-10)',
            'description': 'Descripción',
            'eyes_open': 'Ojos abiertos',
            'in_motion': 'En movimiento',
            'deliberate': 'Deliberada',
            'immediate_retention': 'Retención inmediata',
            'repetition_count': 'Repeticiones',
            'notes': 'Notas',
            'text_content': 'Contenido de texto',
            'text_format': 'Formato de texto',
            'readback_verified': 'Readback verificado',
            'symbols_used': 'Símbolos usados',
            'composition_layer_count': 'Capas de composición',
            'bounding_boxes_used': 'Bounding boxes usados',
        }


class VVIQForm(forms.Form):
    ITEMS = [
        ('1', 'Piensa en un pariente o amigo que veas frecuentemente. Examina la imagen que te viene a la mente: el contorno exacto de su cara, cabeza, hombros y cuerpo.'),
        ('2', 'Rasgos y colores característicos del cabello de esa persona.'),
        ('3', 'Color exacto de los ojos de esa persona.'),
        ('4', 'Piensa en el frente de una tienda que visitas frecuentemente. La apariencia general de la tienda vista desde la calle opuesta.'),
        ('5', 'Una vitrina de esa tienda, incluyendo colores, formas y detalles de artículos individuales en venta.'),
        ('6', 'Piensa en un paisaje campestre con árboles, montañas y un lago. Los colores y formas de los árboles.'),
        ('7', 'El color y la forma del lago.'),
        ('8', 'Un fuerte viento soplando sobre los árboles, causando olas en el lago.'),
        ('9', 'Piensa en un amanecer. Observa el sol saliendo sobre el horizonte en un cielo brumoso.'),
        ('10', 'El cielo despejándose y rodeando el sol con un enorme cielo azul.'),
        ('11', 'Piensa en la fachada de un edificio familiar. Nota los colores de las paredes.'),
        ('12', 'La forma y diseño de las ventanas.'),
        ('13', 'Piensa en un campo abierto de hierba. Los diferentes tonos de verde.'),
        ('14', 'Flores silvestres salpicando la hierba.'),
        ('15', 'El campo se extiende hasta encontrarse con un cielo de nubes suaves.'),
        ('16', 'Un sendero de tierra cruza el campo hacia el horizonte.'),
    ]

    RATING_CHOICES = [
        (5, '5 — Tan vívida como ver realmente'),
        (4, '4 — Razonablemente clara y vívida'),
        (3, '3 — Moderadamente clara y vívida'),
        (2, '2 — Vaga y borrosa'),
        (1, '1 — Sin imagen, solo "sé" que estoy pensando en ello'),
    ]

    context = forms.CharField(
        max_length=100, required=False,
        label='Contexto',
        widget=forms.TextInput(attrs={'placeholder': 'p.ej. baseline, semana 4, post-entrenamiento'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item_num, item_text in self.ITEMS:
            self.fields[f'item_{item_num}'] = forms.ChoiceField(
                choices=self.RATING_CHOICES,
                label=item_text,
                widget=forms.RadioSelect(),
            )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mode', 'program_start_date']
        widgets = {
            'program_start_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'mode': 'Modo de entrenamiento',
            'program_start_date': 'Fecha de inicio del programa',
        }


class SymbolForm(forms.ModelForm):
    class Meta:
        model = Symbol
        fields = [
            'name', 'glyph', 'geometric_form', 'nesting_level',
            'primary_meaning', 'additional_meanings', 'notes',
        ]
        widgets = {
            'additional_meanings': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'name': 'Nombre',
            'glyph': 'Glifo',
            'geometric_form': 'Forma geométrica',
            'nesting_level': 'Nivel de anidamiento',
            'primary_meaning': 'Significado principal',
            'additional_meanings': 'Significados adicionales',
            'notes': 'Notas',
        }


class WorkspaceStartForm(forms.Form):
    exercise_type = forms.ChoiceField(
        choices=WorkspaceExercise.EXERCISE_TYPES,
        label='Tipo de ejercicio',
    )
    duration = forms.ChoiceField(
        choices=[
            (60, '1 minuto'), (120, '2 minutos'), (180, '3 minutos'),
            (300, '5 minutos'), (600, '10 minutos'),
        ],
        initial=180,
        label='Duración',
    )


class WorkspaceAssessForm(forms.ModelForm):
    class Meta:
        model = WorkspaceExercise
        fields = [
            'text_content', 'text_format', 'text_original_composition', 'readback_success',
            'layer_count', 'degradation_noted',
            'annotation_count', 'bounding_boxes_used',
            'symbols_used', 'sources_used',
            'vividness_rating', 'stability_rating', 'detail_rating', 'semantic_clarity',
            'description', 'notes',
        ]
        widgets = {
            'vividness_rating': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'stability_rating': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'detail_rating': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'semantic_clarity': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'value': 5}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'text_content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Texto proyectado/leído'}),
            'symbols_used': forms.CheckboxSelectMultiple(),
            'sources_used': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'text_content': 'Contenido de texto',
            'text_format': 'Formato de texto',
            'text_original_composition': 'Composición original',
            'readback_success': 'Readback exitoso',
            'layer_count': 'Número de capas',
            'degradation_noted': 'Degradación observada',
            'annotation_count': 'Número de anotaciones',
            'bounding_boxes_used': 'Bounding boxes usados',
            'symbols_used': 'Símbolos usados',
            'sources_used': 'Áreas cerebrales fuente',
            'vividness_rating': 'Viveza (1-10)',
            'stability_rating': 'Estabilidad (1-10)',
            'detail_rating': 'Detalle (1-10)',
            'semantic_clarity': 'Claridad semántica (1-10)',
            'description': 'Descripción',
            'notes': 'Notas',
        }


class CapabilityUpdateForm(forms.ModelForm):
    class Meta:
        model = Capability
        fields = ['status', 'confirmed_date']
        widgets = {
            'confirmed_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'status': 'Estado',
            'confirmed_date': 'Fecha de confirmación',
        }

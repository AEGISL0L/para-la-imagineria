from django.utils.safestring import mark_safe
from django import template

register = template.Library()

SVG_GLYPHS = {
    'triángulo²': (
        '<svg viewBox="0 0 100 100" class="inline-block" fill="none" stroke="currentColor" stroke-width="4">'
        '<polygon points="50,8 95,88 5,88"/>'
        '<polygon points="50,32 75,75 25,75"/>'
        '</svg>'
    ),
}


@register.filter
def symbol_glyph(symbol, size='1em'):
    """Render symbol glyph as SVG when needed, plain text otherwise."""
    svg = SVG_GLYPHS.get(symbol.name)
    if svg:
        return mark_safe(svg.replace('class="inline-block"',
                                     f'class="inline-block" width="{size}" height="{size}"'))
    return symbol.glyph


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def format_duration(seconds):
    if not seconds:
        return '0:00'
    minutes = seconds // 60
    secs = seconds % 60
    return f'{minutes}:{secs:02d}'


@register.filter
def emotional_category_badge(category):
    badges = {
        'A': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'B': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        'C': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    }
    return badges.get(category, '')


@register.filter
def phase_color(number):
    colors = {
        1: 'bg-gray-500',
        2: 'bg-blue-500',
        3: 'bg-amber-500',
        4: 'bg-indigo-500',
        5: 'bg-emerald-500',
        6: 'bg-purple-500',
    }
    return colors.get(number, 'bg-gray-500')

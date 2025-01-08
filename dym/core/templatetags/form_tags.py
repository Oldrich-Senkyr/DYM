# In templatetags/form_tags.py

from django import template


register = template.Library()

@register.inclusion_tag('partials/field_errors.html')
def render_field_errors(field):
    """
    Vykreslí chyby pro dané pole formuláře pomocí šablony.
    """
    return {'errors': field.errors}


@register.simple_tag
def render_field_errors_for_formset(formset):
    """
    Renders errors for all fields within a formset.
    """
    errors = []
    for form in formset:
        for field in form:
            if field.errors:
                errors.append('<div class="text-sm text-red-600">{}</div>'.format('</br>'.join(field.errors)))
    return ''.join(errors)
# *********************************************************
# ft_formTags.py */

from django.template import Library
register = Library()

# *********************************************************
@register.inclusion_tag('ft_fieldset_start.html') 
def ft_fieldset_start(legend='', classname=''):
    return { 'legend': legend, 'classname':classname }

# *********************************************************
@register.inclusion_tag('ft_fieldset_end.html') 
def ft_fieldset_end():
    return {}

# *********************************************************
@register.inclusion_tag('ft_button.html') 
def ft_button(classname='', typename='', value='', eventname='', eventaction=''):
    return {'classname':classname, 'typename':typename, 'value':value, 'eventname':eventname, 'eventaction':eventaction}

# *********************************************************
@register.inclusion_tag('ft_formclass.html') 
def ft_formclass(classname=''):
    return {'classname':classname}

# *********************************************************
@register.inclusion_tag('ft_instructions.html') 
def ft_instructions(request, bbcodetext=0):
    return {'request':request,'bbcodetext':bbcodetext}

# *********************************************************
@register.inclusion_tag('ft_rendererrors.html') 
def ft_rendererrors(non_field_errors, field_errors):
    return {'non_field_errors':non_field_errors, 'field_errors':field_errors}

# *********************************************************
@register.inclusion_tag('ft_errorbanner.html') 
def ft_errorbanner(form_non_field_errors='', form_field_errors=''):
    return {'form_non_field_errors':form_non_field_errors, 'form_field_errors':form_field_errors}

# *********************************************************
@register.inclusion_tag('ft_hidden.html') 
def ft_hidden(field): 
    fieldString = field.as_widget()
    return {'fieldString':fieldString}

# *********************************************************
@register.inclusion_tag('ft_field.html') 
def ft_field(field, request): 
    fieldString = field.as_widget()
    return { 'field': field, 'fieldString':fieldString, 'request':request }
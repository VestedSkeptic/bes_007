# *********************************************************
# form_tags.py */

from django.template import Library
register = Library()

# *********************************************************
def render_field_guts(field, cssClass=''): 
    fieldString = field.as_widget()
    if cssClass:
        # split field tag by first space
        splitList = fieldString.split(' ',1)
        # insert class attributes BACKWARDS because I'm inserting at position 1 each time
        splitList.insert(1, '" ')
        splitList.insert(1, cssClass)
        splitList.insert(1, ' class="')
        # join and assemble fieldString
        fieldString = ''.join(splitList)  
    return fieldString

# *********************************************************
@register.inclusion_tag('_render_field.html') 
def render_field(field, cssClass=''): 
    fieldString = render_field_guts(field, cssClass)
    return { 'field': field, 'fieldString':fieldString }

# *********************************************************
@register.inclusion_tag('_render_field_login.html') 
def render_field_login(field, cssClass=''): 
    fieldString = render_field_guts(field, cssClass)
    return { 'field': field, 'fieldString':fieldString }

# *********************************************************
@register.inclusion_tag('_render_field_bare.html') 
def render_field_bare(field, cssClass=''): 
    fieldString = render_field_guts(field, cssClass)
    return { 'field': field, 'fieldString':fieldString }

# *********************************************************
@register.inclusion_tag('_render_submit.html') 
def render_submit(cssClass='', titleText=''): 
    if not titleText: titleText = "Submit"
    if cssClass: fieldString = '<input class="%s" type="submit" value="%s"/>' % (cssClass, titleText)
    else:        fieldString = '<input type="submit" value="%s"/>' % (titleText)
    return {'fieldString':fieldString }

# *********************************************************
@register.inclusion_tag('_render_submit_login.html') 
def render_submit_login(cssClass='', titleText=''): 
    if not titleText: titleText = "Submit"
    if cssClass: fieldString = '<input class="%s" type="submit" value="%s"/>' % (cssClass, titleText)
    else:        fieldString = '<input type="submit" value="%s"/>' % (titleText)
    return {'fieldString':fieldString }

# *********************************************************
@register.inclusion_tag('_render_field_bare.html') 
def render_submit_bare(cssClass='', titleText=''): 
    if not titleText: titleText = "Submit"
    if cssClass: fieldString = '<input class="%s" type="submit" value="%s"/>' % (cssClass, titleText)
    else:        fieldString = '<input type="submit" value="%s"/>' % (titleText)
    return {'fieldString':fieldString }

# *********************************************************
@register.inclusion_tag('_render_non_field_errors.html') 
def render_non_field_errors(errors): 
    return {'errors': errors }


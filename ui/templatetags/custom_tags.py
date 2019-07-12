from django import template
register = template.Library()

@register.filter
def index(List, i):
    try:
        return List[int(i)]
    except:
        return None

@register.filter
def lookup(Dict, i):
    return Dict.get(i)

@register.filter
def attr(obj, att):
    atts = att.split(".")
    if len(atts) > 1 :
        a = atts.pop(0)
        try:
            r = getattr(obj,a)
        except:
            return ''
        return attr(r,'.'.join(atts))
    return getattr(obj, atts.pop(0))

@register.filter
def find_itm_ivr7020h(List, itm):
    for l in List:
        if l.itm == itm:
            return l

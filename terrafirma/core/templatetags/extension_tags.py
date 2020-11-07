from django import template

register = template.Library()


class IfAppNode(template.Node):
    def __init__(self, app, nodelist):
        self.app = app
        self.nodelist = nodelist

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def render(self, context):
        from django.apps import apps

        has_app = apps.is_installed(self.app)

        if has_app:
            return self.nodelist.render(context)
        return ''


@register.tag
def if_calendar_installed(parser, token):
    nodelist = parser.parse(('endif', ))
    parser.delete_first_token()
    return IfAppNode('terrafirma.calendar', nodelist)


@register.tag
def if_map_installed(parser, token):
    nodelist = parser.parse(('endif', ))
    parser.delete_first_token()
    return IfAppNode('terrafirma.map', nodelist)


@register.tag
def if_planner_installed(parser, token):
    nodelist = parser.parse(('endif', ))
    parser.delete_first_token()
    return IfAppNode('terrafirma.planner', nodelist)


@register.tag
def if_stock_installed(parser, token):
    nodelist = parser.parse(('endif', ))
    parser.delete_first_token()
    return IfAppNode('terrafirma.stock', nodelist)


@register.tag
def if_store_installed(parser, token):
    nodelist = parser.parse(('endif', ))
    parser.delete_first_token()
    return IfAppNode('terrafirma.store', nodelist)


@register.inclusion_tag('terrafirma/header_link.html', takes_context=True)
def maybe_link(context, text, url, *args, **kwargs):
    from django.urls import reverse

    request = context['request']
    link = reverse(url, args=args, kwargs=kwargs)
    return {
        'link': link if not request.path == link else None,
        'text': text,
    }


@register.simple_tag(takes_context=True)
def path_env_bed(context):
    env = context['env']
    bed = context['bed']
    return '?env={}&bed={}'.format(env.abbrev, bed.abbrev)


@register.simple_tag(takes_context=True)
def form_kind(context, obj_type=None):
    return 'Edit' if context.get('object', None) else 'New {}'.format(obj_type)



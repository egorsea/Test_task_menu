from django import template
from django.utils.safestring import mark_safe
from django.core.cache import cache
from django.urls import reverse

from Menu.models import MenuModel

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path

    menu_cache_key = f"menu_{menu_name}_cache_key"
    menu = cache.get(menu_cache_key)
    if menu is None:
        menu = MenuModel.objects.filter(name=menu_name).order_by('order')
        cache.set(menu_cache_key, menu)

    def render_menu(menu, parent = None):
        result = ''
        for element in menu:
            if str(element.parent) != str(parent):      #проверка чтобы отобразить только элементы текущего уровня
                continue

            if '/' not in str(element.url):             #проверка на named URL
                element.url = reverse(element.url)

            if element.url == current_url:
                active_class = 'active'
            else:
                active_class = ''

            if element.children.count() > 0:
                result += '<li  class="multi {0}">'.format(active_class)
                result += '<a href="{0}">{1}</a>'.format(element.url, element.item)
                result += '<ul>{0}</ul>'.format(render_menu(element.children.all(), element.item))
                result += '</li>'
            else:
                result += '<li class="{0}"><a href="{1}">{2}</a></li>'.format(active_class, element.url, element.item)
        return result

    menu_html = render_menu(menu)

    return mark_safe(f'<ul id="nav">{menu_html}</ul>')

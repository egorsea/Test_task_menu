from django.contrib import admin
from Menu.models import MenuModel

# Register your models here.
class MenuAdminForm(admin.ModelAdmin):
    list_display = ('name', 'item', 'url', 'parent', 'order')
    search_fields = ('name', 'url')

admin.site.register(MenuModel, MenuAdminForm)

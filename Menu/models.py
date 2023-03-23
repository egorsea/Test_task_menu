from django.db import models

# Create your models here.


class MenuModel(models.Model):

    name = models.CharField(verbose_name='Наименование меню', max_length=255, default = 'main')
    item = models.CharField(verbose_name='Пункт меню', max_length=255)
    url = models.CharField(verbose_name='Ссылка', max_length=255)
    parent = models.ForeignKey('self', verbose_name='Родительский пункт меню', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='Порядок', default=0)

    def __str__(self):
        return self.item

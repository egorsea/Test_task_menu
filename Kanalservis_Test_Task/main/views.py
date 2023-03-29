from django.shortcuts import render

# Create your views here.
from .models import OrderbookModel


def table(request):
    queryset = OrderbookModel.objects.all().order_by('orderbook_id')
    total_price = sum(el.price for el in queryset)
    chartdata = OrderbookModel.objects.values(
        'deliverytime', 'price').order_by('deliverytime')
    context = {
        'queryset': queryset,
        'total_price': total_price,
        'chartdata': chartdata,
    }
    return render(request, 'main/layout.html', context)

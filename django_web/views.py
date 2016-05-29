from django.shortcuts import render
from django_web.models import ItemInfo
from django.core.paginator import Paginator


# Create your views here.

def pure_index(request):
    context = {
        'item_info': 'this is an example',
    }
    return render(request,'index.html',context=context)

def home_page(request):
    limit = 15
    item_info = ItemInfo.objects
    paginator = Paginator(item_info,limit)
    page = request.GET.get('page',1)
    load = paginator.page(page)
    context={
        'item_info' : load,
    }
    return render(request,'index_page.html',context=context)

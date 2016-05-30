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
#-----------------------------------------------------------
def topx(date1,date2,area,limit):

    pipeline = [
        {'$match':{'$and':[{'pub_date':{'$gte':date1,'$lte':date2}},{'area':{'$all':area}}]}},
        {'$group':{'_id':{'$slice':['$cates',2,1]},'counts':{'$sum':1}}},
        {'$limit':limit},
        {'$sort':{'counts':-1}}
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data

series_CY = [i for i in topx('2015.12.25','2015.12.27',['朝阳'],3)]
series_TZ = [i for i in topx('2015.12.25','2015.12.27',['通州'],3)]
series_HD = [i for i in topx('2015.12.25','2015.12.27',['海淀'],3)]
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# 数据中发帖总量柱状图
def total_post():
    pipeline = [
        {'$group':{'_id':{'$slice':['$cates',2,1]},'counts':{'$sum':1}}},
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        print(i)
        data = {
            'name':i['_id'][0],
            'y':i['counts']
        }
        yield data

series_post = [i for i in total_post()]



#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



def info(request):
    item_info = ItemInfo.objects
    times = [i.pub_date for i in item_info.order_by('pub_date').limit(1)]
    context = {
        'counts':item_info.count(),
        'last_time':times[0],
    }

    return render(request,'info.html',context=context)

def chart_page(request):
    context = {
        'chart_CY':series_CY,
        'chart_TZ':series_TZ,
        'chart_HD':series_HD,
        'series_post':series_post,
    }
    return render(request,'chart_info.html',context=context)


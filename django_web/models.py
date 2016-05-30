from django.db import models
from mongoengine import *

class ItemInfo(Document):
    title = StringField()  # 名称严格与数据库中的key 对应
    url = StringField()
    pub_date = StringField()
    area = ListField(StringField())
    cates = ListField(StringField())
    look = StringField()
    price = IntField()
    meta = {'collection':'items'}




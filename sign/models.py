from django.db import models


# Create your models here.
# 发布会表
class Event(models.Model):
    # 自动生成自增长的id字段   即id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)   # 发布会名称
    limit = models.IntegerField()     # 参加人数
    status = models.BooleanField()   # 状态
    address = models.CharField(max_length=200)    # 地址
    start_time = models.DateTimeField("event time")   # 发布会时间
    create_time = models.DateTimeField(auto_now=True)   # 创建时间（自动获取当前时间,修改model对象时，
    # 也能自动保存时间，但是不允许手动在数据库里编辑

    def __str__(self):
        return self.name


# 嘉宾表
class Guest(models.Model):
    # 自动生成自增长的id字段   即id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event)            # 外键  关联发布会id
    realname = models.CharField(max_length=64)      # 姓名
    phone = models.CharField(max_length=16)     # 手机号
    email = models.EmailField()
    sign = models.BooleanField()              # 签到状态
    create_time=models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间,修改model对象时，
    # 也能自动保存时间，但是不允许手动在数据库里编辑

    class Meta:
        unique_together = ("event", "phone")   # unique_together这个选项用于：当你需要通过两个字段
        # 保持唯一性时使用。这会在 Django admin 层和数据库层同时做出限制(也就是相关的 UNIQUE 语句会被包括在
        # CREATE TABLE 语句中)

    def __str__(self):
        return self.realname












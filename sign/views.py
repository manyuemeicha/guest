from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest


def index(request):
    # return HttpResponse("hello world！")
    return render(request, "sign/index.html")


# 点击登录按钮
def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        pwd = request.POST.get("pwd", "")
        user = auth.authenticate(username=username,password=pwd)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect("/event_manage")
            request.session["user"] = username
            return response
        else:
            return render(request, "sign/index.html", {"error": "用户名或者密码错误！"})


# 发布会管理页面
@login_required
def event_manage(request):
    # username = request.COOKIES.get("user", "")
    username = request.session.get("user", "")
    event_list = Event.objects.all()
    return render(request, "sign/event_manage.html", {"user": username, "events":event_list})


# 点击发布会页面的查询按钮
@login_required
def search_name(request):
    username = request.session.get("user", "")
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "sign/event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理页面
@login_required
def guest_manage(request):
    username = request.session.get("user", "")
    guest_list = Guest.objects.all()
    # guest_01 = Guest.objects.filter(realname__contains='oppo')[0].event
    # guest_02 = Guest.objects.filter(realname__contains='oppo')[1].event # 访问关联的外键属性event，
    # 返回的是Event对象，返回的是Event的str形式，即name，这样就省去了多表查询来返回嘉宾关联的发布会名称
    # (数据库存的是event_id),直接访问event_id，也是可以的，返回的是id
    return render(request, "sign/guest_manage.html", {"user": username, "guests": guest_list})


# 点击嘉宾页面的查询按钮
@login_required
def search_phone(request):
    username = request.session.get("user","")
    phone = request.GET.get("phone","")
    guest_list = Guest.objects.filter(phone__contains=phone)
    return render(request, "sign/guest_manage.html", {"user": username, "guests": guest_list})


# 点击发布会页面的签到按钮
@login_required
def sign_index(request, eid):
    sign_count = len(Guest.objects.filter(sign=1, event_id=eid))  # 已签到人数
    guest_count = len(Guest.objects.filter(event_id=eid))         # 该发布会的嘉宾数
    event = get_object_or_404(Event, id=eid)
    if sign_count == guest_count and guest_count != 0:
        return render(request, "sign/sign_index.html", {"event": event, "finish": "签到完成！！！",
                                                   "sign_count": sign_count, "guest_count": guest_count})
    return render(request, "sign/sign_index.html", {"event": event, "sign_count": sign_count,
                                               "guest_count": guest_count})


# 点击签到页面的签到按钮
@login_required
def sign_index_action(request, eid):
    guest_count = len(Guest.objects.filter(event_id=eid))   # 该发布会的嘉宾数
    '''
     sign_count = len(Guest.objects.filter(sign=1, event_id=eid))  # 已签到人数
     这句不能写在这里，因为返回页面的时候返回的已签到人数不是实时的，应该在每次返回页面的前边统计一次，
     才是正确的实时的数据。比如签到后，已签到嘉宾数会变化，如果在前边就统计好了已签到数，在render里返回，
     那么点击签到后，返回的签到数是少1的
    '''
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get("phone", "")
    sign_count = len(Guest.objects.filter(sign=1, event_id=eid))  # 已签到人数
    result = Guest.objects.filter(phone=phone)  # 因为有可能一个人参加两场发布会，所以用filter
    if not result:
        sign_count = len(Guest.objects.filter(sign=1, event_id=eid))  # 保证返回的签到数是实时的，因为也许其他用户已经签到了
        if sign_count == guest_count and guest_count != 0:            # 如果签到数和嘉宾数是相等的，返回签到完成，因为也许其他用户已签到，
                                                                       # 该用户只是进错了发布会，，或者最后一位嘉宾点击签到后，也应显示签到完成
            return render(request, "sign/sign_index.html", {"event": event, "finish": "签到完成！！！",
                                                       "hint": "手机号不存在!", "sign_count": sign_count,
                                                       "guest_count": guest_count})
        return render(request, "sign/sign_index.html", {"event": event, "hint": "手机号不存在!",
                                                   "sign_count": sign_count, "guest_count": guest_count})
    result = Guest.objects.filter(event_id=eid, phone=phone)  # 这里可以用get，因为手机号和发布会是唯一的
    if not result:
        sign_count = len(Guest.objects.filter(sign=1, event_id=eid))  # 保证返回的签到数是实时的，因为也许其他用户已经签到了
        if sign_count == guest_count and guest_count != 0:            # 如果签到数和嘉宾数是相等的，返回签到完成，
                                                                        # 因为也许其他用户已签到，该用户只是进错了发布会，或者最后一位嘉宾点击签到后，也应显示签到完成
            return render(request, "sign/sign_index.html", {"event": event, "finish": "签到完成！！！",
                                                       "hint": "手机号和发布会不匹配!", "sign_count": sign_count,
                                                       "guest_count": guest_count})
        return render(request, "sign/sign_index.html", {"event": event, "hint": "手机号和发布会不匹配!",
                                                   "sign_count": sign_count, "guest_count": guest_count})
    result = Guest.objects.get(phone=phone, event_id=eid)   # get返回一个对象
    if result.sign:
        sign_count = len(Guest.objects.filter(sign=1, event_id=eid))  # 保证返回的签到数是实时的，因为也许其他用户已经签到了
        if sign_count == guest_count and guest_count != 0:            # 如果签到数和嘉宾数是相等的，返回签到完成，因为也许其他用户已签到，
                                                                    # 该用户只是进错了发布会，或者最后一位嘉宾点击签到后，也应显示签到完成
            return render(request, "sign/sign_index.html", {"event": event, "finish": "签到完成！！！",
                                                       "hint": "该手机号已签到!", "guest": result, "sign_count": sign_count,
                                                       "guest_count": guest_count})
        return render(request, "sign/sign_index.html", {"event": event, "hint": "该手机号已签到!", "guest": result,
                                                   "sign_count": sign_count, "guest_count": guest_count})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign=1)
        sign_count = len(Guest.objects.filter(sign=1, event_id=eid))  # 保证返回的签到数是实时的，
        # 因为签到成功时，签到数要加1，写在前边的话，bug：签到数返回的数据少1
        if sign_count == guest_count and guest_count != 0:    # 如果签到数和嘉宾数是相等的，返回签到完成，因为也许其他用户已签到，
                                                            # 该用户只是进错了发布会，或者最后一位嘉宾点击签到后，也应显示签到完成
            return render(request, "sign/sign_index.html", {"event": event, "finish": "签到完成！！！",
                                                       "hint": "签到成功!", "guest": result, "sign_count": sign_count,
                                                       "guest_count": guest_count})
        return render(request, "sign/sign_index.html", {"event": event, "hint": "签到成功!", "guest": result,
                                                   "sign_count": sign_count, "guest_count": guest_count})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("sign//index/")



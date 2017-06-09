from django.shortcuts import render, HttpResponse

# Create your views here.


def test(request):
    return HttpResponse('ewfwefwfwefwfwefwfwfew')


def index(reqeust):
    return render(reqeust, 'base/base.html')


def iptables_init(reqeust):
    return render(reqeust, 'iptables/iptables_init.html')




















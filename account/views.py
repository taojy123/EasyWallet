# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse, HttpResponseRedirect

from account.models import Wallet, Transaction


def index(request):

    token = request.GET.get('token')

    wallet = Wallet.objects.filter(token=token).first()

    if not wallet:
        return HttpResponseRedirect('/login/')

    return render(request, 'index.html', locals())


def login(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        token = request.POST.get('token')

        if not name:
            name = uuid.uuid4().hex

        if not token:
            token = uuid.uuid4().hex

        if Wallet.objects.filter(name=name).exists():
            return HttpResponseBadRequest('name 重复')

        if Wallet.objects.filter(token=token).exists():
            return HttpResponseBadRequest('token 重复')

        w = Wallet.objects.create(name=name, token=token)

        return HttpResponseRedirect('/?token=%s' % w.token)

    return render(request, 'login.html', locals())


def pay(request):

    from_token = request.POST.get('from_token')
    to_name = request.POST.get('to_name')
    amount = float(request.POST.get('amount'))

    from_wallet = Wallet.objects.filter(token=from_token).first()
    if not from_wallet:
        return HttpResponseBadRequest('密钥无效')

    if from_wallet.balance < amount:
        return HttpResponseBadRequest('余额不足')

    to_wallet = Wallet.objects.filter(name=to_name).first()
    if not to_wallet:
        return HttpResponseBadRequest('收款账号不正确')

    if from_wallet == to_wallet:
        return HttpResponseBadRequest('不要给自己转账')

    Transaction.objects.create(from_wallet=from_wallet, to_wallet=to_wallet, amount=amount)

    return HttpResponseRedirect('/?token=%s' % from_wallet.token)



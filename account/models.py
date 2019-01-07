# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum


class Wallet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=100, unique=True)

    @property
    def balance(self):
        total_income = self.income_transation_set.aggregate(Sum('amount')).get('amount__sum') or 0
        total_payout = self.payout_transation_set.aggregate(Sum('amount')).get('amount__sum') or 0
        return total_income - total_payout

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    from_wallet = models.ForeignKey(Wallet, related_name='payout_transation_set', blank=True, null=True)
    to_wallet = models.ForeignKey(Wallet, related_name='income_transation_set')
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '#%s[%s]' % (self.id, self.amount)



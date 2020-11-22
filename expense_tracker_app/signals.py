from django.db.models.signals import post_init, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Category, Expense


@receiver(post_init, sender=Category)
def update_month_category(sender, instance, **kwargs):
    '''Updates month if it's older than 1 month and clears epxenses'''
    if instance.monthly:
        date_now = timezone.localdate()
        if not instance.date:
            instance.date = date_now
        elif (instance.date.month < date_now.month or
                instance.date.year < date_now.year):
            instance.expense_set.all().delete()
            instance.date = date_now


@receiver(pre_save, sender=Category)
def limit_check_category(sender, instance, **kwargs):
    '''
    Limits creating more than 16 categories for user
    Monthly categories = 16, Normal categories = 16
    '''
    amount = sender.objects.filter(
        monthly=instance.monthly, user=instance.user).count()
    if amount >= 16:
        raise Exception('Maximum number of categories is 16.')


@receiver(pre_save, sender=Expense)
def limit_check_expense(sender, instance, **kwargs):
    '''Limits creating more than 20 expenses for category'''
    category = instance.category
    amount = category.expense_set.all().count()
    if amount >= 20:
        raise Exception('Maximum number of expenses for category is 20.')

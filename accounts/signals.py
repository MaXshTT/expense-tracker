from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from expense_tracker_app.models import Category, Income


@receiver(post_save, sender=User)
def create_income(sender, instance, created, **kwargs):
    if created:
        Income.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_ready_categories(sender, instance, created, **kwargs):
    if created:
        Category.objects.bulk_create([
            Category(name='Utilities', user=instance),
            Category(name='Groceries', user=instance),
            Category(name='Transport', user=instance),
            Category(name='Restaurant', user=instance),
            Category(name='Shopping', user=instance),
            Category(name='Entertainment', user=instance),
            Category(name='Rent', user=instance),
            Category(name='Utilities', user=instance, monthly=True),
            Category(name='Groceries', user=instance, monthly=True),
            Category(name='Transport', user=instance, monthly=True),
            Category(name='Restaurant', user=instance, monthly=True),
            Category(name='Shopping', user=instance, monthly=True),
            Category(name='Entertainment', user=instance, monthly=True),
            Category(name='Rent', user=instance, monthly=True),
        ])

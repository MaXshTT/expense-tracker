from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Expense(models.Model):
    name = models.CharField('Name', max_length=20)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    cost = models.DecimalField('Cost', max_digits=9, decimal_places=2, validators=[
                               MinValueValidator(0.01)])
    day_due = models.IntegerField('Day Due',
                                  validators=[MaxValueValidator(31), MinValueValidator(1)], null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expected_cost = models.DecimalField('Expected Cost', max_digits=9, decimal_places=2, validators=[
                                        MinValueValidator(0.01)], null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Name', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly = models.BooleanField(default=False)
    date = models.DateField(null=True, editable=False)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['user', 'pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' 
        If date is given and monthly false, date field gets changed to None.
        Updates date field if monthly.
        '''
        if self.date and not self.monthly:
            self.date = None
        elif not self.id and self.monthly:
            self.date = timezone.localdate()
        return super(Category, self).save(*args, **kwargs)

    def get_sum_expenses_category(self):
        if self.expense_set.all():
            return self.expense_set.aggregate(Sum('cost'))['cost__sum']
        return 0


class Income(models.Model):

    class PaySchedule(models.IntegerChoices):
        MONTHLY = 0, 'Monthly'
        BI_MONTHLY = 1, 'Bi-Monthly'
        WEEKLY = 2, 'Weekly'
        BI_WEEKLY = 3, 'Bi-Weekly'

    net_income = models.DecimalField('Net Income',
                                     max_digits=9, decimal_places=2, default=0, validators=[
                                         MinValueValidator(0)])
    savings_percent = models.PositiveIntegerField('Savings Percent',
                                                  validators=[MaxValueValidator(100)], default=0)
    extra_income = models.DecimalField('Extra Monthly Income',
                                       max_digits=9, decimal_places=2, default=0, validators=[
                                           MinValueValidator(0)])
    pay_schedule = models.IntegerField('Pay Schedule',
                                       default=PaySchedule.MONTHLY, choices=PaySchedule.choices)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_total_monthly(self):
        if self.pay_schedule == self.PaySchedule.MONTHLY.value:
            return self.net_income + self.extra_income

        elif self.pay_schedule == self.PaySchedule.BI_MONTHLY.value:
            return round(((self.net_income + self.extra_income) / 2), 2)

        elif self.pay_schedule == self.PaySchedule.WEEKLY.value:
            return round(((self.net_income + self.extra_income) * 52 / 12), 2)

        elif self.pay_schedule == self.PaySchedule.BI_WEEKLY.value:
            return round(((self.net_income + self.extra_income) * 26 / 12), 2)

    def get_sum_expenses_user(self):
        expenses = Expense.objects.filter(
            user=self.user, category__monthly=False)
        if expenses:
            return expenses.aggregate(Sum('cost'))['cost__sum']
        return 0

    def get_sum_monthly_expenses_user(self):
        expenses = Expense.objects.filter(
            user=self.user, category__monthly=True)
        if expenses:
            return expenses.aggregate(Sum('cost'))['cost__sum']
        return 0

    def get_expenses_count(self):
        categories = Category.objects.filter(user=self.user, monthly=False)
        expenses_count = 0
        for expense in categories.values_list('expense', flat=True):
            expenses_count += 1 if expense else 0
        return expenses_count

    def get_monthly_savings(self):
        return round(self.get_total_monthly() * self.savings_percent / 100, 2)

    def get_monthly_spendable(self):
        return self.get_total_monthly() - self.get_sum_expenses_user() - self.get_monthly_savings()

    def get_daily_spendable(self):
        return round(self.get_monthly_spendable() * 12 / 365, 2)

    def get_month_left_money(self):
        return self.get_total_monthly() - self.get_sum_monthly_expenses_user() - self.get_monthly_savings()

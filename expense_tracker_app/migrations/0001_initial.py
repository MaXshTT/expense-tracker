from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('monthly', models.BooleanField(default=False)),
                ('date', models.DateField(editable=False, null=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['user', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('net_income', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[
                 django.core.validators.MinValueValidator(0)], verbose_name='Net Income')),
                ('savings_percent', models.PositiveIntegerField(default=0, validators=[
                 django.core.validators.MaxValueValidator(100)], verbose_name='Savings Percent')),
                ('extra_income', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[
                 django.core.validators.MinValueValidator(0)], verbose_name='Extra Monthly Income')),
                ('pay_schedule', models.IntegerField(choices=[
                 (0, 'Monthly'), (1, 'Bi-Monthly'), (2, 'Weekly'), (3, 'Bi-Weekly')], default=0, verbose_name='Pay Schedule')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=9, validators=[
                 django.core.validators.MinValueValidator(0.01)], verbose_name='Cost')),
                ('day_due', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(
                    31), django.core.validators.MinValueValidator(1)], verbose_name='Day Due')),
                ('expected_cost', models.DecimalField(decimal_places=2, max_digits=9, null=True, validators=[
                 django.core.validators.MinValueValidator(0.01)], verbose_name='Expected Cost')),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='expense_tracker_app.Category')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]

from rest_framework import serializers

from expense_tracker_app.models import Category, Expense, Income


class ExpenseSerializer(serializers.ModelSerializer):
    day_due = serializers.CharField(allow_blank=True)

    class Meta:
        model = Expense
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        """Delete user field if PUT/PATCH."""
        super().__init__(*args, **kwargs)
        if 'view' in self.context and self.context['view'].action in ['update', 'partial_update']:
            self.fields.pop('user', None)

    def validate_category(self, value):
        """Checks if it's user's category."""
        if value.user != self.context['request'].user:
            raise serializers.ValidationError(
                'Should be user\'s category.')
        return value

    def validate_day_due(self, value):
        if not value:
            return
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer.')
        if not (0 < int(value) < 31):
            raise serializers.ValidationError(
                'Should be greater than 0 and less than 31.')
        return int(value)

    def validate_user(self, value):
        """Checks if user matches to the user who's sending."""
        if value != self.context['request'].user:
            raise serializers.ValidationError("Wrong user.")
        return value

    @property
    def errors(self):
        errors = super().errors
        verbose_errors = {}

        # fields = { field.name: field.verbose_name } for each field in model
        fields = {field.name: field.verbose_name for field in
                  self.Meta.model._meta.get_fields() if hasattr(field, 'verbose_name')}

        # iterate over errors and replace error key with verbose name if exists
        for field_name, error in errors.items():
            if field_name in fields:
                verbose_errors[str(fields[field_name])] = error
            else:
                verbose_errors[field_name] = error
        return verbose_errors


class CategorySerializer(serializers.ModelSerializer):
    expenses = serializers.SerializerMethodField('get_expenses')

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        """Delete user field if PUT/PATCH."""
        super().__init__(*args, **kwargs)
        if 'view' in self.context and self.context['view'].action in ['update', 'partial_update']:
            self.fields.pop('user', None)

    def get_expenses(self, obj):
        return ExpenseSerializer(obj.expense_set.all(), many=True).data

    def validate_user(self, value):
        """Checks if user matches to the user who's sending."""
        if value != self.context['request'].user:
            raise serializers.ValidationError("Wrong user.")
        return value

    @property
    def errors(self):
        errors = super().errors
        verbose_errors = {}

        # fields = { field.name: field.verbose_name } for each field in model
        fields = {field.name: field.verbose_name for field in
                  self.Meta.model._meta.get_fields() if hasattr(field, 'verbose_name')}

        # iterate over errors and replace error key with verbose name if exists
        for field_name, error in errors.items():
            if field_name in fields:
                verbose_errors[str(fields[field_name])] = error
            else:
                verbose_errors[field_name] = error
        return verbose_errors


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        """Delete user field if PUT/PATCH."""
        super().__init__(*args, **kwargs)
        if 'view' in self.context and self.context['view'].action in ['update', 'partial_update']:
            self.fields.pop('user', None)

    @property
    def errors(self):
        errors = super().errors
        verbose_errors = {}

        # fields = { field.name: field.verbose_name } for each field in model
        fields = {field.name: field.verbose_name for field in
                  self.Meta.model._meta.get_fields() if hasattr(field, 'verbose_name')}

        # iterate over errors and replace error key with verbose name if exists
        for field_name, error in errors.items():
            if field_name in fields:
                verbose_errors[str(fields[field_name])] = error
            else:
                verbose_errors[field_name] = error
        return verbose_errors

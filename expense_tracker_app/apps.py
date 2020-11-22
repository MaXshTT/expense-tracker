from django.apps import AppConfig


class ExpenseTrackerAppConfig(AppConfig):
    name = 'expense_tracker_app'

    def ready(self):
        import expense_tracker_app.signals

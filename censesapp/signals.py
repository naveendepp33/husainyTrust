from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now

from .models import LoginReport


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):

    LoginReport.objects.create(
        user=user,
        login_time=now()
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):

    report = LoginReport.objects.filter(user=user, logout_time__isnull=True).last()

    if report:
        report.logout_time = now()
        report.save()
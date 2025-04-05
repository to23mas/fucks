from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings


def test_mail():
    print('sending test mail')
    User = get_user_model()
    admin_email = User.objects.get(username='admin').email
    subject = "Test Email from Birthday App"
    message = "This is a test email. If you received this, the email configuration is working correctly."

    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin_email],
        fail_silently=False,
    ) 

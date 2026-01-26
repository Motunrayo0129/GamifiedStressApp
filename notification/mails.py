from django.core.mail import send_mail

def send_welcome_email(user):
    print('Sending welcome email for {}'.format(user.username))
    send_mail(
        subject="Welcome to ThriveDaily 💙",
        message=f"Hi {user.username},\n\nWelcome to ThriveDaiy a GamifiedStressApp! We’re glad to have you.",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )

from django.core.mail import EmailMessage


def email_template(subject, content, to):
    # Email sending Template
    msg = EmailMessage(
        subject, content,
        'no-reply@authorshaven.com', [to]
    )
    msg.content_subtype = 'html'
    msg.send()

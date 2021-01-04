from celery import task
from django.core.mail import send_mail
from .models import Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO
import weasyprint

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
              f'Your order was successfully created.\n' \
              f'Your order ID is {order.id}.'

    email = EmailMessage(
        subject,
        message,
        'eshop@finesauces.store',
        [order.email]
    )

    # generate pdf
    html = render_to_string('pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)

    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
        out.getvalue(),
        'application/pdf'
    )

    # send e-mail
    email.send()

@task
def status_change_notification(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n'\
              f'Status of your order {order.id} was changed to {order.status}'

    mail_sent = send_mail(
        subject,
        message,
        'eshop@finesauces.store',
        [order.email]
    )

    return mail_sent

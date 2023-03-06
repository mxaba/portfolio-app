from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Skill, Contact, Certificate
from .forms import ContactForm
from .decorators import *

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def base_home(request):
    message = Contact.objects.filter(is_read=False).count()
    request.session['messages'] = message
    context = {}
    return render(request, 'base/base_home.html', context)


@admin_only
def inbox_page(request):
    inbox = Contact.objects.all()

    request.session['messages'] = Contact.objects.filter(is_read=False).count()

    context = {'inbox': inbox}
    return render(request, 'base/inbox.html', context)


@admin_only
def message_page(request, pk):
    message = get_object_or_404(Contact, id=pk)
    message.is_read = True
    message.save()

    context = {'message': message}
    return render(request, 'base/message.html', context)


@admin_only
def message_reply(request, pk):
    message = get_object_or_404(Contact, id=pk)

    if request.method == 'POST':

        template = render_to_string('base/email_template.html',
                                    {'name': request.POST.get('name'),
                                     'reply': request.POST.get('reply')})

        email = EmailMessage(request.POST.get('subject'),
                             template,
                             settings.EMAIL_HOST_USER,
                             [request.POST.get('email')])

        email.fail_silently = False
        email.send()

        messages.success(request, 'Email sent successfully!')
        return redirect('base:message', pk=message.id)

    context = {'message': message}
    return render(request, 'base/message_reply.html', context)



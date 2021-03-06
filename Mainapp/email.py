from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def welcome(username,receiver):
    # Creating message subject and sender
    subject = 'Welcome to neigbourhood community we value and cherish your status'
    sender = 'kiipmeshack@mail.com'

    #passing in the context vairables
    text_content = render_to_string('email/email.txt',{"username": username})
    html_content = render_to_string('email/email.html',{"username": username})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()
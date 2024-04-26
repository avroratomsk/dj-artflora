from django.core.mail import send_mail

EMAIL_FROM = "info@xn----7sbah6bllcobpj.xn--p1ai"
email_clients = "saniagolovanev@gmail.com"

def email_callback(messages, title):
  send_mail(
    title,
    messages,
    EMAIL_FROM,
    email_clients.split(','),
    fail_silently=False,
  )
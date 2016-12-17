import logging
from google.appengine.api import mail
email_templates = {
    'forgot_password': {'subject':"Your Password Is Now Re-set",
                        'body': '''Dear %s:
                        Thank you for using 52payments.
                        This is a link to re-set the password for the account linked to this email.
                        Please note that the link will expire in about 10 minutes.

                        %s

                        Thanks,
                        Sincerely

                        '''}
}
def send_email(user, subject, body, sender='admin@52payments.com'):
    name = user.first_name + ' '+ user.last_name
    message = mail.EmailMessage(
        sender=sender,
        subject=subject)
    message.to = "%s <%s>"%(name, user.email)
    logging.debug(body)
    message.body = body
    message.send()

import threading
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject, body, recipient_list, mail_from):
        self.subject = subject
        self.recipient_list = recipient_list
        self.body = body
        self.mail_from = mail_from
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.body,
                           self.mail_from, [self.mail_from], self.recipient_list)
        msg.send()


def send_mail_to_selected_candidate(myjob, candidates):
    recipient_list = []
    for candidate in candidates:
        recipient_list.append(candidate.email)

    subject = f'Result of application for the post of {myjob.title}'
    body = f'You have been shortlisted for viva for the post of {myjob.title} in {myjob.company_name}.\
    We will let you know about the location and time for the viva in a later time. Thank you for being with us'
    mail_from = 'cvrecommender@gmail.com'

    EmailThread(subject, body, recipient_list, mail_from).start()

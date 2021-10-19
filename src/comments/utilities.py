from core.settings import ALLOWED_HOSTS
from django.template.loader import render_to_string


def send_new_comment_notification(comment):
    if ALLOWED_HOSTS:
        host = "http://" + ALLOWED_HOSTS[0]
    else:
        host = "http://localhost:8000"
    author = comment.bb.author
    context = {"author": author, "comment": comment, "host": host}
    subject = render_to_string("email/new_comment_letter_subject.txt", context)
    body_text = render_to_string("email/new_comment_letter_body.txt", context)
    author.email_user(subject, body_text)

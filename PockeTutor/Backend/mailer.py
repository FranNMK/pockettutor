from flask_mail import Message
from flask import url_for
from .extensions import mail

def send_verification_email(user_email):
    # url_for will be called from a request context in the route
    verify_link = url_for("auth.verify_email", token="{{TOKEN}}", _external=True)
    # We replace token later in route to avoid app context issues
    msg = Message(subject="Verify your PocketTutor account", recipients=[user_email])
    msg.body = f"Welcome to PocketTutor! Click to verify: {verify_link}"
    return msg

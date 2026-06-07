from flask import Blueprint, render_template
from backend.services.email_service import send_email
from backend.services.sms_service import send_alert_sms

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@notifications_bp.route('/')
def show_notifications():
    # Example notification
    send_email("user@example.com", "Book Due Reminder", "Your book is due tomorrow!")
    send_alert_sms("+917610398277")
    return render_template('notifications.html', notifications=["Book due reminder sent!"])

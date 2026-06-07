from apscheduler.schedulers.background import BackgroundScheduler
from backend.services.email_service import send_email

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        lambda: send_email("user@example.com", "Reminder", "Return your books!"),
        trigger='interval',
        hours=24
    )
    scheduler.start()

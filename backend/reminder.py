from plyer import notification
import sqlite3
from datetime import datetime, timedelta

def get_reminder_days(reminder_str):
    if reminder_str == "1_day_before":
        return 1
    elif reminder_str == "2_days_before":
        return 2
    return 0  

def check_and_notify_tasks():
    conn = sqlite3.connect("personaltaskmanager.db")  
    cursor = conn.cursor()

    cursor.execute("SELECT taskname, due_date, remainder FROM task")
    tasks = cursor.fetchall()

    today = datetime.now().date()

    for taskname, due_date_str, remainder_str in tasks:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            continue  

        days_before = get_reminder_days(remainder_str)
        reminder_date = due_date - timedelta(days=days_before)

        if today == reminder_date:
            notification.notify(
                title="TASK REMINDER",
                message=f"'{taskname}' is due in {days_before} day(s) on {due_date_str}.",
                timeout=15  
            )

    conn.close()

if __name__ == "__main__":
    check_and_notify_tasks()

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from app.email_service import EmailService
import atexit

# Global scheduler instance
scheduler = BackgroundScheduler()


class ReminderScheduler:
    """Manages scheduled reminder notifications"""

    @staticmethod
    def start():
        """Start the background scheduler"""
        if not scheduler.running:
            scheduler.start()
            atexit.register(lambda: scheduler.shutdown())
            print("✅ Reminder scheduler started!")

    @staticmethod
    def stop():
        """Stop the background scheduler"""
        if scheduler.running:
            scheduler.shutdown()
            print("✅ Reminder scheduler stopped!")

    @staticmethod
    def schedule_task_reminder(
        task_name: str,
        deadline: str,
        reminder_times: list
    ):
        """
        Schedule email notifications for task reminder
        
        Args:
            task_name: Name of the task
            deadline: Deadline datetime string
            reminder_times: List of reminder datetime objects
        """
        try:
            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")

            # Schedule 15 minutes before
            time_15min_before = deadline_dt - timedelta(minutes=15)
            if time_15min_before > datetime.now():
                scheduler.add_job(
                    EmailService.send_task_reminder_notification,
                    args=(task_name, deadline, "15 minutes", "15min"),
                    trigger=DateTrigger(run_date=time_15min_before),
                    id=f"task_{task_name}_15min_{time_15min_before.timestamp()}"
                )
                print(f"⏰ Scheduled 15-min reminder for: {task_name}")

            # Schedule 5 minutes before
            time_5min_before = deadline_dt - timedelta(minutes=5)
            if time_5min_before > datetime.now():
                scheduler.add_job(
                    EmailService.send_task_reminder_notification,
                    args=(task_name, deadline, "5 minutes", "5min"),
                    trigger=DateTrigger(run_date=time_5min_before),
                    id=f"task_{task_name}_5min_{time_5min_before.timestamp()}"
                )
                print(f"⏰ Scheduled 5-min reminder for: {task_name}")

            # Schedule at exact time
            if deadline_dt > datetime.now():
                scheduler.add_job(
                    EmailService.send_task_reminder_notification,
                    args=(task_name, deadline, "NOW", "exact"),
                    trigger=DateTrigger(run_date=deadline_dt),
                    id=f"task_{task_name}_exact_{deadline_dt.timestamp()}"
                )
                print(f"⏰ Scheduled exact reminder for: {task_name}")

        except Exception as e:
            print(f"❌ Error scheduling task reminder: {str(e)}")

    @staticmethod
    def schedule_fixed_reminder(
        title: str,
        time: str,
        days_ahead: int = 7
    ):
        """
        Schedule email notifications for fixed reminder
        
        Args:
            title: Title of the reminder
            time: Time in HH:MM format
            days_ahead: Number of days to generate reminders for
        """
        try:
            hour, minute = map(int, time.split(":"))
            now = datetime.now()
            start_date = now.date()

            # Schedule for each day
            for day_offset in range(days_ahead):
                reminder_date = start_date + timedelta(days=day_offset)
                reminder_time = datetime.combine(reminder_date, datetime.min.time())
                reminder_time = reminder_time.replace(hour=hour, minute=minute)

                if reminder_time > now:
                    # Schedule 15 minutes before
                    time_15min_before = reminder_time - timedelta(minutes=15)
                    if time_15min_before > now:
                        scheduler.add_job(
                            EmailService.send_fixed_reminder_notification,
                            args=(title, time, "15min"),
                            trigger=DateTrigger(run_date=time_15min_before),
                            id=f"fixed_{title}_{reminder_date}_15min_{time_15min_before.timestamp()}"
                        )

                    # Schedule 5 minutes before
                    time_5min_before = reminder_time - timedelta(minutes=5)
                    if time_5min_before > now:
                        scheduler.add_job(
                            EmailService.send_fixed_reminder_notification,
                            args=(title, time, "5min"),
                            trigger=DateTrigger(run_date=time_5min_before),
                            id=f"fixed_{title}_{reminder_date}_5min_{time_5min_before.timestamp()}"
                        )

                    # Schedule at exact time
                    scheduler.add_job(
                        EmailService.send_fixed_reminder_notification,
                        args=(title, time, "exact"),
                        trigger=DateTrigger(run_date=reminder_time),
                        id=f"fixed_{title}_{reminder_date}_exact_{reminder_time.timestamp()}"
                    )

            print(f"⏰ Scheduled fixed reminder for: {title} at {time} for {days_ahead} days")

        except Exception as e:
            print(f"❌ Error scheduling fixed reminder: {str(e)}")

    @staticmethod
    def get_scheduled_jobs():
        """Get list of all scheduled jobs"""
        jobs = []
        for job in scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "next_run_time": str(job.next_run_time),
                "trigger": str(job.trigger)
            })
        return jobs

    @staticmethod
    def remove_job(job_id: str):
        """Remove a scheduled job"""
        try:
            scheduler.remove_job(job_id)
            print(f"✅ Removed job: {job_id}")
            return True
        except Exception as e:
            print(f"❌ Error removing job: {str(e)}")
            return False

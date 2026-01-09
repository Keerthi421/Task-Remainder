import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    """Service to send email notifications"""

    # Gmail SMTP settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    # Load credentials from environment variables
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "your_email@gmail.com")

    @staticmethod
    def send_task_reminder_notification(
        task_name: str,
        deadline: str,
        time_remaining: str,
        notification_type: str
    ):
        """
        Send email notification for task reminder
        
        Args:
            task_name: Name of the task
            deadline: Deadline of the task
            time_remaining: How much time is left
            notification_type: "15min", "5min", or "exact"
        """
        try:
            subject, body = EmailService._create_task_email(
                task_name,
                deadline,
                time_remaining,
                notification_type
            )
            EmailService._send_email(subject, body)
            print(f"✅ Email sent: {task_name} - {notification_type}")

        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")

    @staticmethod
    def send_fixed_reminder_notification(
        title: str,
        time: str,
        notification_type: str
    ):
        """
        Send email notification for fixed reminder
        
        Args:
            title: Title of the reminder (e.g., Take Paracetamol)
            time: Scheduled time
            notification_type: "15min", "5min", or "exact"
        """
        try:
            subject, body = EmailService._create_fixed_email(
                title,
                time,
                notification_type
            )
            EmailService._send_email(subject, body)
            print(f"✅ Email sent: {title} - {notification_type}")

        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")

    @staticmethod
    def _create_task_email(task_name: str, deadline: str, time_remaining: str, notification_type: str):
        """Create task reminder email"""

        emoji_map = {
            "15min": "⏰ UPCOMING",
            "5min": "🔔 HURRY UP",
            "exact": "🎯 DUE NOW"
        }

        emoji = emoji_map.get(notification_type, "📌")

        subject = f"{emoji} Reminder: {task_name}"

        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; border-radius: 10px; padding: 30px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #667eea; text-align: center;">📝 Task Reminder</h1>
                    
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0;">
                        <h2 style="color: #333; margin: 0 0 10px 0;">{task_name}</h2>
                        <p style="color: #666; margin: 5px 0;"><strong>Deadline:</strong> {deadline}</p>
                        <p style="color: #666; margin: 5px 0;"><strong>Time Remaining:</strong> {time_remaining}</p>
                    </div>

                    <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0;">
                        <p style="margin: 0; color: #856404;">
                            <strong>{emoji} {notification_type.upper()}</strong>
                        </p>
                    </div>

                    <p style="color: #666; text-align: center; margin-top: 30px;">
                        ✨ Smart Deadline & Medication Reminder Engine
                    </p>
                </div>
            </body>
        </html>
        """

        return subject, body

    @staticmethod
    def _create_fixed_email(title: str, time: str, notification_type: str):
        """Create fixed reminder email"""

        emoji_map = {
            "15min": "⏰ UPCOMING",
            "5min": "🔔 HURRY UP",
            "exact": "🎯 TIME NOW"
        }

        emoji = emoji_map.get(notification_type, "💊")

        subject = f"{emoji} Reminder: {title}"

        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; border-radius: 10px; padding: 30px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #764ba2; text-align: center;">💊 Medication/Routine Reminder</h1>
                    
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 4px solid #764ba2; margin: 20px 0;">
                        <h2 style="color: #333; margin: 0 0 10px 0;">{title}</h2>
                        <p style="color: #666; margin: 5px 0;"><strong>Scheduled Time:</strong> {time}</p>
                    </div>

                    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; margin: 20px 0;">
                        <p style="margin: 0; color: #2e7d32;">
                            <strong>{emoji} {notification_type.upper()}</strong>
                        </p>
                    </div>

                    <p style="color: #666; text-align: center; margin-top: 30px;">
                        ✨ Smart Deadline & Medication Reminder Engine
                    </p>
                </div>
            </body>
        </html>
        """

        return subject, body

    @staticmethod
    def _send_email(subject: str, body: str):
        """Send email via Gmail SMTP"""

        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = EmailService.SENDER_EMAIL
            message["To"] = EmailService.RECIPIENT_EMAIL

            # Attach HTML
            part = MIMEText(body, "html")
            message.attach(part)

            # Send email
            server = smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT)
            server.starttls()
            server.login(EmailService.SENDER_EMAIL, EmailService.SENDER_PASSWORD)
            server.sendmail(
                EmailService.SENDER_EMAIL,
                EmailService.RECIPIENT_EMAIL,
                message.as_string()
            )
            server.quit()

            return True

        except Exception as e:
            raise Exception(f"Email sending failed: {str(e)}")


# Test function
def test_email():
    """Test email sending"""
    EmailService.send_task_reminder_notification(
        task_name="Test Assignment",
        deadline="2026-01-15 23:59",
        time_remaining="15 minutes",
        notification_type="15min"
    )


if __name__ == "__main__":
    test_email()

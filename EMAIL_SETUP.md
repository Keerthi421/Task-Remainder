# 📧 EMAIL NOTIFICATION SETUP GUIDE

## ✨ What's New?

Your Smart Reminder Engine now sends **EMAIL NOTIFICATIONS** at:
- ⏰ **15 minutes before** the reminder
- ⏰ **5 minutes before** the reminder  
- ⏰ **Exact time** of the reminder

## 🚀 Quick Setup (Gmail)

### Step 1: Create a .env File

Copy the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

### Step 2: Get Gmail App Password

1. **Enable 2-Step Verification**
   - Go to https://myaccount.google.com/security
   - Scroll down to "2-Step Verification"
   - Follow the prompts

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select **Mail** and **Windows Computer**
   - Google will generate a 16-character password
   - Copy it (it looks like: `abcd efgh ijkl mnop`)

### Step 3: Update .env File

Edit your `.env` file:

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
RECIPIENT_EMAIL=your_email@gmail.com
```

**Important:** 
- Use your **Gmail App Password**, NOT your regular password
- The RECIPIENT_EMAIL can be the same or different

### Step 4: Run the Application

```bash
python -m uvicorn app.main:app --reload
```

Open: **http://localhost:8000**

## 🧪 Test Email Sending

To test if emails work, create a reminder and check your inbox!

### Quick Test Script

```python
from app.email_service import EmailService

# Send a test email
EmailService.send_task_reminder_notification(
    task_name="Test Task",
    deadline="2026-01-15 23:59",
    time_remaining="15 minutes",
    notification_type="15min"
)
```

Run it:
```bash
python -c "from app.email_service import EmailService; EmailService.send_task_reminder_notification('Test', '2026-01-15 23:59', '15min', '15min')"
```

## 📋 How It Works

1. **User creates a reminder** (task or fixed)
2. **System schedules 3 emails:**
   - 15 minutes before → Email sent
   - 5 minutes before → Email sent
   - At exact time → Email sent
3. **Background scheduler** (APScheduler) manages the timing
4. **EmailService** sends beautiful HTML emails

## 🎨 Email Template

The emails look beautiful with:
- ✅ Color-coded design
- ✅ Task/reminder details
- ✅ Time remaining info
- ✅ Professional HTML formatting

## 🔧 File Structure

```
app/
├── email_service.py    ← Handles email sending
├── scheduler.py        ← Manages scheduled reminders
├── main.py            ← FastAPI with scheduler integration
├── logic.py           ← Reminder calculation logic
├── schemas.py         ← Data models
└── __init__.py

.env                   ← Your email credentials (CREATE THIS!)
.env.example          ← Template for .env
```

## ⚠️ Troubleshooting

### "Email sending failed: Login failed"
- ✅ Check your Gmail app password is correct
- ✅ Make sure 2-Step Verification is enabled
- ✅ Verify SENDER_EMAIL matches your Gmail

### "Connection refused"
- ✅ Check internet connection
- ✅ Gmail SMTP might be blocked by firewall
- ✅ Try using a VPN

### "No emails received"
- ✅ Check spam/junk folder
- ✅ Verify RECIPIENT_EMAIL is correct
- ✅ Check .env file is in root directory

## 🌐 Alternative Email Providers

You can use other email services:

### SendGrid (Recommended for production)
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
```

### AWS SES
```python
import boto3
client = boto3.client('ses')
```

### Microsoft Outlook
```
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
```

## 📊 Monitoring Scheduled Jobs

List all scheduled email jobs:

```python
from app.scheduler import ReminderScheduler
jobs = ReminderScheduler.get_scheduled_jobs()
print(jobs)
```

## 🚀 Deploy to Production

### Railway.app Deployment

1. **Create account** at railway.app
2. **Connect GitHub** (or upload manually)
3. **Add environment variables**
   ```
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=xxxx xxxx xxxx xxxx
   RECIPIENT_EMAIL=your_email@gmail.com
   ```
4. **Deploy!**

### Other Platforms
- Heroku
- Render.com
- AWS Lambda
- Google Cloud Run
- DigitalOcean

## 💡 Advanced Features

### Custom Email Triggers
Modify `scheduler.py` to add:
- 30 minutes before reminder
- 1 hour before reminder
- Custom time intervals

### SMS Notifications (Twilio)
Add to scheduler to send SMS instead:
```python
pip install twilio
```

### Webhook Notifications
Post to external services (Discord, Slack):
```python
import requests
requests.post("https://your-webhook.com/reminder")
```

### Database Storage
Save reminders to SQLite/PostgreSQL:
```python
pip install sqlalchemy
```

## 📧 Email Customization

Edit `app/email_service.py`:
- Change email subject format
- Modify HTML template
- Add company logo/branding
- Include task deadline details

## ✅ Features Summary

- ✅ Automatic email notifications
- ✅ 3-stage reminder system (15, 5, exact)
- ✅ Beautiful HTML emails
- ✅ Background scheduler
- ✅ Task & fixed reminders
- ✅ No database needed
- ✅ Production-ready
- ✅ Easy configuration

## 🎯 Next Steps

1. ✅ Set up .env with Gmail credentials
2. ✅ Test email by creating a reminder
3. ✅ Deploy to Railway/Heroku
4. ✅ Add SMS notifications (optional)
5. ✅ Add database persistence (optional)

---

**Enjoy your smart reminder system!** 🌟

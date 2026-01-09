# 📧 EMAIL NOTIFICATION FEATURE - COMPLETE GUIDE

## ✨ What's New?

Your Smart Reminder Engine now sends **automatic email notifications**!

### When You Create a Reminder:
- **15 minutes before** → Email sent ⏰
- **5 minutes before** → Email sent 🔔  
- **At exact time** → Email sent 🎯

---

## 🎬 Real Example

### You Create This Reminder:
```json
{
  "task": "Math Assignment",
  "deadline": "2026-01-15 18:00",
  "difficulty": "hard"
}
```

### You'll Receive These Emails:

#### Email #1 (at 2026-01-15 17:45)
```
Subject: ⏰ UPCOMING Reminder: Math Assignment

Dear User,

📝 Task Reminder

Math Assignment

Deadline: 2026-01-15 18:00
Time Remaining: 15 minutes

⏰ UPCOMING

✨ Smart Deadline & Medication Reminder Engine
```

#### Email #2 (at 2026-01-15 17:55)
```
Subject: 🔔 HURRY UP Reminder: Math Assignment

[Similar format, 5 minutes left]
```

#### Email #3 (at 2026-01-15 18:00)
```
Subject: 🎯 DUE NOW Reminder: Math Assignment

[Final reminder, time's up!]
```

---

## 🔧 Setup Instructions

### 1. Get Gmail App Password
- Go: https://myaccount.google.com/apppasswords
- Need 2-Step Verification enabled first
- Copy the 16-digit password

### 2. Create `.env` File

Create file: `c:\Users\SREE KEERTHI\task-remainder\.env`

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
RECIPIENT_EMAIL=your_email@gmail.com
```

### 3. Restart Server

The server will automatically detect the .env file and start the email scheduler!

```bash
python -m uvicorn app.main:app --reload
```

You should see:
```
✅ Reminder scheduler started!
🚀 Application started with email notification support!
```

---

## 📊 How It Works (Technical)

### Architecture:

```
User creates reminder
        ↓
FastAPI endpoint receives data
        ↓
Calculate reminder times
        ↓
Schedule 3 email jobs with APScheduler
        ↓
Background scheduler waits...
        ↓
At scheduled time → EmailService sends email
        ↓
User receives email! 📧
```

### Code Flow:

```python
# 1. User submits form → POST /task-reminder

# 2. main.py calls scheduler:
ReminderScheduler.schedule_task_reminder(
    task_name="Math Assignment",
    deadline="2026-01-15 18:00",
    reminders=["2026-01-10 18:00", ...]
)

# 3. scheduler.py schedules 3 jobs:
# Job 1: Send email at 17:45 (15 min before)
# Job 2: Send email at 17:55 (5 min before)  
# Job 3: Send email at 18:00 (exact time)

# 4. APScheduler runs background checks
# 5. EmailService sends emails via Gmail SMTP
```

---

## 📧 Email Service Details

### File: `app/email_service.py`

**Key Functions:**
- `send_task_reminder_notification()` - Send task reminders
- `send_fixed_reminder_notification()` - Send medication reminders
- `_create_task_email()` - Generate HTML email
- `_send_email()` - Send via Gmail SMTP

**Features:**
- ✅ Beautiful HTML emails
- ✅ Color-coded by reminder type
- ✅ Task/medication details included
- ✅ Professional branding

---

## ⏱️ Scheduler Details

### File: `app/scheduler.py`

**Key Classes:**
- `ReminderScheduler` - Main scheduler controller

**Key Methods:**
- `start()` - Initialize background scheduler
- `schedule_task_reminder()` - Schedule task emails
- `schedule_fixed_reminder()` - Schedule medication emails
- `get_scheduled_jobs()` - List all pending emails
- `remove_job()` - Cancel a scheduled email

---

## 🎯 Task Reminder Emails

### When Generated:

1. User submits: `{"task": "...", "deadline": "...", "difficulty": "..."}`
2. System schedules emails for specified times
3. Emails sent automatically by APScheduler

### Email Times:

- **Easy (1 reminder):** 1 day before
- **Medium (2 reminders):** 3 days + 1 day before  
- **Hard (3 reminders):** 5 days + 3 days + 1 day before

Plus additional **15 min, 5 min, exact time** notifications!

### Email Content:

```html
<h1 style="color: #667eea;">📝 Task Reminder</h1>

<div style="background-color: #f9f9f9; padding: 20px;">
  <h2>Math Assignment</h2>
  <p><strong>Deadline:</strong> 2026-01-15 23:59</p>
  <p><strong>Time Remaining:</strong> 15 minutes</p>
</div>

<div style="background-color: #fff3cd; padding: 15px;">
  <p><strong>⏰ UPCOMING</strong></p>
</div>
```

---

## 💊 Fixed Reminder Emails

### When Generated:

1. User submits medication reminder
2. System schedules daily emails for X days
3. Each day sends 3 emails (15 min, 5 min, exact)

### Example: Vitamin D at 8:00 AM for 7 days

```
Day 1: Emails at 7:45, 7:55, 8:00
Day 2: Emails at 7:45, 7:55, 8:00
Day 3: Emails at 7:45, 7:55, 8:00
... (repeat for 7 days)
```

---

## 🔐 Email Security

### Gmail Setup:
1. Uses official Gmail SMTP server
2. Requires 2-Step Verification
3. Requires App-specific password (not regular password)
4. Credentials stored in `.env` (not in code)

### Best Practices:
- ✅ `.env` is NOT committed to git
- ✅ Passwords encrypted at runtime
- ✅ Only sent to intended recipient
- ✅ Uses TLS encryption (port 587)

---

## 🚀 Deployment

### On Railway.app:

1. Add environment variables:
   ```
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=xxxx xxxx xxxx xxxx
   RECIPIENT_EMAIL=your_email@gmail.com
   ```

2. Deploy normally:
   ```bash
   railway up
   ```

3. Emails sent automatically from cloud! ☁️

### On Other Platforms:

- Heroku: Add Config Vars
- AWS: Use Secrets Manager
- Google Cloud: Use Secret Manager
- Any platform: Set environment variables

---

## 📈 Monitoring

### Check Scheduled Jobs:

```python
from app.scheduler import ReminderScheduler

jobs = ReminderScheduler.get_scheduled_jobs()
for job in jobs:
    print(f"Job: {job['id']}")
    print(f"Next Run: {job['next_run_time']}")
```

### View Server Logs:

```
✅ Reminder scheduler started!
🚀 Application started with email notification support!
⏰ Scheduled 15-min reminder for: Math Assignment
⏰ Scheduled 5-min reminder for: Math Assignment
⏰ Scheduled exact reminder for: Math Assignment
✅ Email sent: Math Assignment - 15min
```

---

## 🔧 Troubleshooting

### Error: "Login failed"
**Cause:** Wrong Gmail password or credentials  
**Fix:** Check `.env` has correct app password

### Error: "Connection refused"
**Cause:** Gmail SMTP blocked by firewall  
**Fix:** Check network, try VPN

### Error: "ModuleNotFoundError: apscheduler"
**Cause:** APScheduler not installed  
**Fix:** `pip install APScheduler==3.10.4`

### No emails received
**Cause:** Multiple possibilities  
**Fix:**
- Check spam folder
- Verify RECIPIENT_EMAIL
- Check server logs for errors
- Verify `.env` is in root directory

---

## 📝 Email Template Customization

### Modify Task Email Template:

Edit `app/email_service.py`, function `_create_task_email()`:

```python
@staticmethod
def _create_task_email(task_name: str, deadline: str, time_remaining: str, notification_type: str):
    """Create custom task reminder email"""
    
    # Customize subject
    subject = f"Custom: {task_name}"
    
    # Customize HTML body
    body = f"""
    <html>
        <body>
            <h1>Your Custom Email</h1>
            <p>Task: {task_name}</p>
            <p>Deadline: {deadline}</p>
        </body>
    </html>
    """
    
    return subject, body
```

---

## 💡 Advanced Features

### Multi-recipient emails:
```python
def send_to_multiple(recipients: list):
    for email in recipients:
        EmailService.RECIPIENT_EMAIL = email
        EmailService._send_email(subject, body)
```

### Scheduled reminders with SMS (Twilio):
```python
from twilio.rest import Client

def send_sms_reminder(phone: str):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        body="Your reminder!",
        from_=TWILIO_PHONE,
        to=phone
    )
```

### Database persistence:
```python
from sqlalchemy import create_engine
# Save reminders to SQLite/PostgreSQL
# Track email delivery status
# Retry failed emails
```

---

## 📊 Email Statistics

Track email deliveries:

```python
email_stats = {
    "sent": 0,
    "failed": 0,
    "delivered": 0,
    "total_tasks": 0
}

def increment_sent():
    email_stats["sent"] += 1
```

---

## ✅ Features Summary

**Current:**
- ✅ Automatic 3-stage email notifications
- ✅ Task & fixed reminders
- ✅ Beautiful HTML emails  
- ✅ APScheduler background jobs
- ✅ Gmail SMTP integration
- ✅ Environment variable security
- ✅ Error handling & logging

**Future:**
- 🚀 SMS notifications (Twilio)
- 🚀 Slack notifications
- 🚀 Discord webhooks
- 🚀 Database persistence
- 🚀 Email delivery tracking
- 🚀 Retry failed emails
- 🚀 Multiple recipients
- 🚀 Email templates customization

---

## 🎉 You're All Set!

Your reminder system now sends beautiful email notifications automatically!

**Next Steps:**
1. ✅ Create `.env` with Gmail credentials
2. ✅ Test with a reminder
3. ✅ Deploy to cloud platform
4. ✅ Get notifications 24/7!

**Questions?** Check `QUICK_START.md` or `EMAIL_SETUP.md`!

# 🎉 EMAIL NOTIFICATION SETUP - QUICK START

Your reminder system is **READY** but needs email configuration!

## ⚡ 3-Minute Setup

### **Step 1: Create a Gmail App Password**

1. Go to: https://myaccount.google.com/security
2. Turn on **2-Step Verification** (if not already on)
3. Go to: https://myaccount.google.com/apppasswords
4. Select **Mail** and **Windows Computer**
5. **Copy** the 16-digit password shown (e.g.: `abcd efgh ijkl mnop`)

### **Step 2: Create .env File**

In your project root (`c:\Users\SREE KEERTHI\task-remainder\`), create a file named `.env`:

```env
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
RECIPIENT_EMAIL=your_gmail@gmail.com
```

**Replace:**
- `your_gmail@gmail.com` with your actual Gmail address
- `abcd efgh ijkl mnop` with the 16-digit app password (keep the spaces)

### **Step 3: Test It!**

1. Open: http://localhost:8000
2. Create a task reminder with deadline 15 minutes from now
3. Check your Gmail inbox in 15 minutes! 📧

---

## 📧 What You'll Get

When you create a reminder, you'll receive **3 emails**:

### 🔔 Email 1: 15 minutes before
```
Subject: ⏰ UPCOMING Reminder: Math Assignment
Body: Beautiful HTML email with task details
```

### 🔔 Email 2: 5 minutes before
```
Subject: 🔔 HURRY UP Reminder: Math Assignment
Body: Beautiful HTML email reminding you it's coming soon
```

### 🔔 Email 3: At exact time
```
Subject: 🎯 DUE NOW Reminder: Math Assignment
Body: Final reminder email - time's up!
```

---

## 🔧 Environment Variables Explained

| Variable | What It Is | Example |
|----------|-----------|---------|
| `SENDER_EMAIL` | Gmail to send FROM | `myemail@gmail.com` |
| `SENDER_PASSWORD` | 16-digit app password | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAIL` | Email to send TO | `myemail@gmail.com` |

**Note:** Use your **Gmail App Password**, NOT your regular Gmail password!

---

## ⚠️ Troubleshooting

### "Email failed to send"
- ✅ Check 2-Step Verification is ON (https://myaccount.google.com/security)
- ✅ Check app password is correct in `.env`
- ✅ Make sure `.env` file is in root directory (same level as `requirements.txt`)

### "ModuleNotFoundError: No module named 'apscheduler'"
```bash
pip install APScheduler==3.10.4
```

### "No emails received"
- ✅ Check spam/junk folder
- ✅ Check RECIPIENT_EMAIL is correct
- ✅ Check server is running (should say "Reminder scheduler started!")

---

## 📂 Project Files

```
task-remainder/
├── app/
│   ├── main.py ..................... FastAPI with scheduler
│   ├── scheduler.py ................ Email scheduling logic
│   ├── email_service.py ............ Email sending
│   ├── logic.py .................... Reminder calculations
│   ├── schemas.py .................. Data models
│   └── __init__.py
├── static/
│   └── index.html .................. Frontend UI
├── .env ............................ ⭐ CREATE THIS!
├── .env.example .................... Template
├── EMAIL_SETUP.md .................. Full setup guide
├── requirements.txt ................ Dependencies
└── README.md ....................... Project info
```

---

## 🚀 How It Works (Behind the Scenes)

1. **User creates reminder** → Form submitted
2. **System calculates times** → 15 min before, 5 min before, exact time
3. **APScheduler registers jobs** → Background scheduler queues emails
4. **At scheduled time** → EmailService sends beautiful HTML email via Gmail SMTP
5. **User receives email** → In inbox with all details!

---

## 🌐 Alternative Email Services

### Gmail (Current - RECOMMENDED)
✅ Free  
✅ Reliable  
✅ No setup costs

### SendGrid (Production)
```python
from sendgrid import SendGridAPIClient
```
Get free API key at: https://sendgrid.com

### AWS SES
```python
import boto3
```

### Outlook/Microsoft
```
SMTP_SERVER = "smtp-mail.outlook.com"
```

---

## 💡 Advanced: Using Different Email

You can send FROM one email and TO another:

```env
SENDER_EMAIL=mybot@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
RECIPIENT_EMAIL=mywork@company.com
```

This sends emails from `mybot@gmail.com` to `mywork@company.com`!

---

## 🎯 Quick Checklist

- [ ] Created `.env` file in project root
- [ ] Added Gmail address to `SENDER_EMAIL`
- [ ] Added 16-digit app password to `SENDER_PASSWORD`
- [ ] Server shows "✅ Reminder scheduler started!"
- [ ] Created a test reminder
- [ ] Received email in inbox

---

## 📞 Still Having Issues?

Check the logs in terminal. You should see:

```
✅ Reminder scheduler started!
🚀 Application started with email notification support!
```

If you see errors, the .env file might be:
- In wrong location (should be in root)
- Wrong permissions
- Malformed credentials

---

## 🎉 You're All Set!

Your smart reminder system now sends emails automatically! 

**Next:** Deploy to Railway, Heroku, or any cloud platform and get reminders 24/7! 🚀

---

**Questions?** Check `EMAIL_SETUP.md` for the full detailed guide!

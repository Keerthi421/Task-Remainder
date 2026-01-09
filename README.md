#  Smart Deadline & Medication Reminder Engine (FastAPI)

A backend service that generates **intelligent reminders** for tasks and **fixed-time reminders** for medications & routines.

##  Features

###  Smart Task Reminder (Intelligent)
Used for assignments, projects, exams, work deadlines.

**Input:**
```json
{
  "task": "Math Assignment",
  "deadline": "2026-01-15 23:59",
  "difficulty": "hard"
}
```

**Output:**
```json
{
  "task": "Math Assignment",
  "deadline": "2026-01-15 23:59",
  "difficulty": "hard",
  "reminders": [
    "2026-01-10 18:00",
    "2026-01-13 18:00",
    "2026-01-15 18:00"
  ],
  "time_pressure_score": 82,
  "days_remaining": 6
}
```

### Fixed-Time Reminder (Tablet / Medicine / Alarm)
Used for taking tablets, drinking water, daily routines.

**Input:**
```json
{
  "title": "Take Paracetamol",
  "time": "17:00",
  "frequency": "daily",
  "days_ahead": 3
}
```

**Output:**
```json
{
  "title": "Take Paracetamol",
  "time": "17:00",
  "frequency": "daily",
  "next_reminders": [
    "2026-01-09 17:00",
    "2026-01-10 17:00",
    "2026-01-11 17:00"
  ]
}
```

##  Smart Logic

### Task Difficulty → Reminder Count
| Difficulty | Reminder Count | Schedule |
|-----------|---|----------|
| **easy** | 1 | 1 day before |
| **medium** | 2 | 3 days + 1 day before |
| **hard** | 3 | 5 days + 3 days + 1 day before |

### Time Pressure Score (0–100)
Calculated based on:
- **Days remaining** (closer to deadline = higher score)
- **Task difficulty** (hard tasks = higher base score)
- **Task type** (dynamic weighting)

Score interpretation:
- **0-30:** Low urgency
- **30-60:** Medium urgency
- **60-100:** High urgency

## 🛠 Tech Stack

- **FastAPI** - Modern async web framework
- **Python 3.8+** - Core language
- **Pydantic** - Data validation
- **datetime** - Time calculations
- **Uvicorn** - ASGI server

##  Project Structure

```
smart-reminder/
├── app/
│   ├── main.py         # FastAPI app & endpoints
│   ├── schemas.py      # Pydantic models
│   └── logic.py        # Reminder logic
├── requirements.txt    # Dependencies
└── README.md          # This file
```

##  Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

### 3. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

##  API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| **GET** | `/health` | Health check |
| **GET** | `/` | Welcome message |
| **POST** | `/task-reminder` | Smart task reminders |
| **POST** | `/fixed-reminder` | Fixed-time reminders |

##  Usage Examples

### Example 1: Hard Assignment Due in 6 Days
```bash
curl -X POST "http://localhost:8000/task-reminder" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Physics Project",
    "deadline": "2026-01-15 23:59",
    "difficulty": "hard"
  }'
```

**Response:**
```json
{
  "task": "Physics Project",
  "deadline": "2026-01-15 23:59",
  "difficulty": "hard",
  "reminders": [
    "2026-01-10 18:00",
    "2026-01-13 18:00",
    "2026-01-15 18:00"
  ],
  "time_pressure_score": 82,
  "days_remaining": 6
}
```

### Example 2: Daily Medication Reminder
```bash
curl -X POST "http://localhost:8000/fixed-reminder" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Take Vitamin D",
    "time": "08:00",
    "frequency": "daily",
    "days_ahead": 7
  }'
```

**Response:**
```json
{
  "title": "Take Vitamin D",
  "time": "08:00",
  "frequency": "daily",
  "next_reminders": [
    "2026-01-09 08:00",
    "2026-01-10 08:00",
    "2026-01-11 08:00",
    "2026-01-12 08:00",
    "2026-01-13 08:00",
    "2026-01-14 08:00",
    "2026-01-15 08:00"
  ]
}
```

### Example 3: Easy Quiz Due Tomorrow
```bash
curl -X POST "http://localhost:8000/task-reminder" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "English Quiz",
    "deadline": "2026-01-10 17:00",
    "difficulty": "easy"
  }'
```

**Response:**
```json
{
  "task": "English Quiz",
  "deadline": "2026-01-10 17:00",
  "difficulty": "easy",
  "reminders": [
    "2026-01-09 18:00"
  ],
  "time_pressure_score": 95,
  "days_remaining": 1
}
```

##  Why This Project Is Great

✅ **Real-life use case** - Medicine reminders, homework tracking
✅ **Intelligent logic** - Smart scheduling based on difficulty
✅ **Clean API design** - Easy to understand and use
✅ **Fully documented** - Swagger docs included
✅ **Production-ready** - Error handling, validation
✅ **Extendable** - Easy to add database, notifications, webhooks
✅ **Resume-worthy** - Shows backend architecture skills

##  Future Enhancements

-  Database persistence (SQLite/PostgreSQL)
-  Email/SMS notifications
-  Push notifications
-  Analytics dashboard
-  User authentication
-  Reminder history
-  Custom recurring patterns
-  Timezone support

##  Error Handling

The API returns proper HTTP status codes:

- **200 OK** - Successful request
- **400 Bad Request** - Invalid input (wrong difficulty, date format, etc.)
- **404 Not Found** - Endpoint not found
- **500 Internal Server Error** - Server error

Example error response:
```json
{
  "detail": "Invalid difficulty. Use: easy, medium, hard"
}
```

##  Testing in Swagger UI

1. Open http://localhost:8000/docs
2. Click on any endpoint (e.g., `/task-reminder`)
3. Click **"Try it out"**
4. Fill in the JSON example
5. Click **"Execute"**
6. View the response

##  Requirements

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dateutil==2.8.2
```

##  Author

Built with ❤️ using FastAPI





from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from pathlib import Path

from app.schemas import (
    TaskReminderRequest, 
    TaskReminderResponse,
    FixedReminderRequest, 
    FixedReminderResponse
)
from app.logic import ReminderLogic
from app.scheduler import ReminderScheduler
from app.email_service import EmailService

# Initialize FastAPI app
app = FastAPI(
    title="Smart Deadline & Medication Reminder Engine",
    description="🌟 Intelligent reminder service for tasks, deadlines, and medications",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Smart Reminder Engine",
        version="1.0.0",
        description="API for generating intelligent task and medication reminders",
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ==================== STARTUP & SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Initialize scheduler on app startup"""
    ReminderScheduler.start()
    print("🚀 Application started with email notification support!")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop scheduler on app shutdown"""
    ReminderScheduler.stop()


# ==================== ENDPOINTS ====================

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        - status: "healthy"
        - timestamp: Current server time
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Smart Reminder Engine is running 🚀"
    }


@app.post("/task-reminder", response_model=TaskReminderResponse, tags=["Smart Task Reminders"])
async def create_task_reminder(request: TaskReminderRequest):
    """
    Generate intelligent reminders for tasks with deadlines.
    
    **Used for:**
    - Assignments
    - Projects
    - Exams
    - Work deadlines
    
    **Input Example:**
    ```json
    {
        "task": "Math Assignment",
        "deadline": "2026-01-15 23:59",
        "difficulty": "hard"
    }
    ```
    
    **Output includes:**
    - List of reminder times
    - Time pressure score (0-100)
    - Days remaining until deadline
    
    **Difficulty → Reminder Count:**
    - easy: 1 reminder
    - medium: 2 reminders
    - hard: 3 reminders
    """
    try:
        # Parse and validate deadline
        deadline = ReminderLogic.parse_datetime(request.deadline)
        
        # Validate difficulty
        difficulty = request.difficulty.lower()
        if difficulty not in ReminderLogic.DIFFICULTY_MAP:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid difficulty. Use: easy, medium, hard"
            )
        
        # Generate reminders
        reminders = ReminderLogic.generate_task_reminders(deadline, difficulty)
        
        # Calculate time pressure
        days_remaining = ReminderLogic.calculate_days_remaining(deadline)
        time_pressure_score = ReminderLogic.calculate_time_pressure_score(
            days_remaining, 
            difficulty
        )
        
        # Schedule email notifications (15 min, 5 min, and exact time)
        try:
            ReminderScheduler.schedule_task_reminder(
                request.task,
                request.deadline,
                reminders
            )
        except Exception as e:
            print(f"⚠️ Warning: Could not schedule emails: {str(e)}")
        
        return TaskReminderResponse(
            task=request.task,
            deadline=request.deadline,
            difficulty=difficulty,
            reminders=reminders,
            time_pressure_score=time_pressure_score,
            days_remaining=days_remaining
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/fixed-reminder", response_model=FixedReminderResponse, tags=["Fixed-Time Reminders"])
async def create_fixed_reminder(request: FixedReminderRequest):
    """
    Generate fixed-time reminders for medications, routines, and daily tasks.
    
    **Used for:**
    - Taking medications/tablets
    - Drinking water
    - Daily routines
    - Regular alarms
    
    **Input Example:**
    ```json
    {
        "title": "Take Paracetamol",
        "time": "17:00",
        "frequency": "daily",
        "days_ahead": 3
    }
    ```
    
    **Output includes:**
    - List of next reminder times
    - Frequency information
    
    **Frequency Options:**
    - daily (generates for specified days)
    - weekly (can be extended in future)
    - custom (can be extended in future)
    """
    try:
        # Validate frequency
        frequency = request.frequency.lower()
        if frequency not in ["daily", "weekly", "custom"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid frequency. Use: daily, weekly, custom"
            )
        
        # Generate reminders
        reminders = ReminderLogic.generate_fixed_reminders(
            request.time,
            frequency,
            request.days_ahead
        )
        
        # Schedule email notifications for fixed reminders
        try:
            ReminderScheduler.schedule_fixed_reminder(
                request.title,
                request.time,
                request.days_ahead
            )
        except Exception as e:
            print(f"⚠️ Warning: Could not schedule emails: {str(e)}")
        
        return FixedReminderResponse(
            title=request.title,
            time=request.time,
            frequency=frequency,
            next_reminders=reminders
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# ==================== ROOT ENDPOINT ====================

@app.get("/", tags=["Root"])
async def root():
    """Serve the frontend UI"""
    return FileResponse(Path(__file__).parent.parent / "static" / "index.html")


@app.get("/api/info", tags=["Root"])
async def api_info():
    """Welcome endpoint with API information"""
    return {
        "message": " Smart Deadline &  Reminder Engine",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "task_reminder": "POST /task-reminder",
            "fixed_reminder": "POST /fixed-reminder",
            "docs": "/docs (Swagger UI)",
            "redoc": "/redoc (ReDoc)"
        },
        "quick_links": {
            "api_documentation": "/docs",
            "alternative_docs": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

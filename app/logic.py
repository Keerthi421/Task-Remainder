from datetime import datetime, timedelta
from typing import List, Tuple


class ReminderLogic:
    """Contains all reminder generation and calculation logic"""

    # Difficulty to reminder count mapping
    DIFFICULTY_MAP = {
        "easy": 1,
        "medium": 2,
        "hard": 3
    }

    @staticmethod
    def parse_datetime(datetime_str: str) -> datetime:
        """Parse datetime string in format YYYY-MM-DD HH:MM"""
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError(f"Invalid datetime format. Use: YYYY-MM-DD HH:MM")

    @staticmethod
    def parse_time(time_str: str) -> Tuple[int, int]:
        """Parse time string in format HH:MM"""
        try:
            hour, minute = map(int, time_str.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid hour or minute")
            return hour, minute
        except ValueError:
            raise ValueError(f"Invalid time format. Use: HH:MM")

    @staticmethod
    def get_reminder_count(difficulty: str) -> int:
        """Get number of reminders based on difficulty level"""
        if difficulty.lower() not in ReminderLogic.DIFFICULTY_MAP:
            raise ValueError(f"Invalid difficulty. Use: easy, medium, hard")
        return ReminderLogic.DIFFICULTY_MAP[difficulty.lower()]

    @staticmethod
    def calculate_time_pressure_score(days_remaining: int, difficulty: str) -> int:
        """
        Calculate time pressure score (0-100)
        
        Score increases with:
        - Fewer days remaining
        - Higher difficulty
        """
        if days_remaining < 0:
            return 100  # Deadline passed

        difficulty_weight = {
            "easy": 20,
            "medium": 50,
            "hard": 80
        }

        base_score = difficulty_weight.get(difficulty.lower(), 50)

        # Reduce days remaining factor
        if days_remaining == 0:
            days_factor = 40  # Same day deadline
        elif days_remaining == 1:
            days_factor = 30
        elif days_remaining <= 3:
            days_factor = 20
        elif days_remaining <= 7:
            days_factor = 10
        else:
            days_factor = 0

        total_score = min(base_score + days_factor, 100)
        return total_score

    @staticmethod
    def generate_task_reminders(deadline: datetime, difficulty: str) -> List[str]:
        """
        Generate smart reminders based on deadline and difficulty
        
        Strategy:
        - easy (1 reminder): Day before at 6 PM
        - medium (2 reminders): 3 days before + day before at 6 PM
        - hard (3 reminders): 5 days before + 3 days before + day before at 6 PM
        """
        reminder_count = ReminderLogic.get_reminder_count(difficulty)
        reminders = []

        now = datetime.now()

        if reminder_count == 1:
            # Easy: 1 day before
            reminder_time = deadline - timedelta(days=1)
            reminder_time = reminder_time.replace(hour=18, minute=0, second=0)
            if reminder_time > now:
                reminders.append(reminder_time.strftime("%Y-%m-%d %H:%M"))

        elif reminder_count == 2:
            # Medium: 3 days before + 1 day before
            for days_before in [3, 1]:
                reminder_time = deadline - timedelta(days=days_before)
                reminder_time = reminder_time.replace(hour=18, minute=0, second=0)
                if reminder_time > now:
                    reminders.append(reminder_time.strftime("%Y-%m-%d %H:%M"))

        elif reminder_count == 3:
            # Hard: 5 days before + 3 days before + 1 day before
            for days_before in [5, 3, 1]:
                reminder_time = deadline - timedelta(days=days_before)
                reminder_time = reminder_time.replace(hour=18, minute=0, second=0)
                if reminder_time > now:
                    reminders.append(reminder_time.strftime("%Y-%m-%d %H:%M"))

        return reminders

    @staticmethod
    def generate_fixed_reminders(
        time_str: str, 
        frequency: str, 
        days_ahead: int = 3
    ) -> List[str]:
        """
        Generate fixed-time reminders for medications/routines
        
        Current time is used as starting point
        Generates reminders for specified number of days
        """
        hour, minute = ReminderLogic.parse_time(time_str)
        reminders = []

        now = datetime.now()
        start_date = now.date()

        # Generate reminders for specified days ahead
        for day_offset in range(days_ahead):
            reminder_date = start_date + timedelta(days=day_offset)
            reminder_time = datetime.combine(reminder_date, datetime.min.time())
            reminder_time = reminder_time.replace(hour=hour, minute=minute)

            # Only add if reminder time is in future
            if reminder_time > now:
                reminders.append(reminder_time.strftime("%Y-%m-%d %H:%M"))

        return reminders

    @staticmethod
    def calculate_days_remaining(deadline: datetime) -> int:
        """Calculate days remaining until deadline"""
        now = datetime.now()
        days = (deadline.date() - now.date()).days
        return days

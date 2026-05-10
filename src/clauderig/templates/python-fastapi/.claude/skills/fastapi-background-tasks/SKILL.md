---
name: fastapi-background-tasks
description: FastAPI background tasks, Celery workers, and async task queue patterns.
---

# FastAPI Background Tasks

## Built-in BackgroundTasks

```python
# app/routers/users.py
from fastapi import APIRouter, BackgroundTasks, Depends
from app.services.email import send_welcome_email
from app.db import get_session

router = APIRouter()


def send_email_task(email: str, name: str) -> None:
    # Runs after response is sent — no await needed here
    send_welcome_email(to=email, name=name)


@router.post("/users", status_code=201)
async def create_user(
    payload: CreateUserSchema,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_session),
):
    user = await UserService(db).create(payload)
    background_tasks.add_task(send_email_task, user.email, user.name)
    return user
```

## Celery Setup

```python
# app/worker.py
from celery import Celery

celery_app = Celery(
    "app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
```

## Celery Tasks

```python
# app/tasks/email.py
from app.worker import celery_app
import logging

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,   # seconds
    name="tasks.send_email",
)
def send_welcome_email_task(self, email: str, name: str) -> dict:
    try:
        result = send_welcome_email(to=email, name=name)
        logger.info("Email sent to %s", email)
        return {"status": "sent", "to": email}
    except Exception as exc:
        logger.warning("Email failed for %s, retrying: %s", email, exc)
        raise self.retry(exc=exc)
```

## Dispatching from FastAPI

```python
from app.tasks.email import send_welcome_email_task

@router.post("/users", status_code=201)
async def create_user(payload: CreateUserSchema, db: AsyncSession = Depends(get_session)):
    user = await UserService(db).create(payload)

    # Fire-and-forget
    send_welcome_email_task.delay(user.email, user.name)

    # With result tracking
    task = send_welcome_email_task.apply_async(
        args=[user.email, user.name],
        countdown=5,    # delay 5s
    )
    return {"user": user, "email_task_id": task.id}
```

## Task Status Endpoint

```python
from celery.result import AsyncResult

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "id": task_id,
        "status": result.status,          # PENDING, STARTED, SUCCESS, FAILURE, RETRY
        "result": result.result if result.ready() else None,
    }
```

## Celery Beat — Periodic Tasks

```python
# app/worker.py
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "cleanup-expired-tokens": {
        "task": "tasks.cleanup_expired_tokens",
        "schedule": crontab(hour=3, minute=0),  # daily at 3am
    },
    "send-weekly-report": {
        "task": "tasks.weekly_report",
        "schedule": crontab(day_of_week="monday", hour=9),
    },
}
```

## Run Workers

```bash
# Worker
celery -A app.worker worker --loglevel=info --concurrency=4

# Beat scheduler (periodic tasks)
celery -A app.worker beat --loglevel=info

# Flower monitoring UI
pip install flower
celery -A app.worker flower --port=5555
```

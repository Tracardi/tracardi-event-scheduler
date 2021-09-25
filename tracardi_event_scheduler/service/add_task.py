import time

import asyncio
from uuid import uuid4

from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.metadata import Metadata
from tracardi.domain.task import Task, TaskEvent
from tracardi.domain.time import Time
from tracardi.service.storage.factory import StorageFor

from tracardi_event_scheduler.service.network import local_ip


async def add_task(event_type, timestamp):
    t = Task(
        timestamp=timestamp,
        event=TaskEvent(
            metadata=Metadata(ip=local_ip, time=Time()),
            id=str(uuid4()),
            type=event_type,
            properties={"a": 1},
            source=Entity(id="a4fb18a2-5406-4190-bd91-e1719bb5202c"),
            session=Entity(id="1"),
            profile=Entity(id="1"),
            context=Context(),
        ),
        event_type="test",
        status='pending'
    )
    await StorageFor(t).index().save()


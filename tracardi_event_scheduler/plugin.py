import time

from tracardi.domain.context import Context
from tracardi.domain.task import Task, TaskEvent
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from uuid import uuid4
from tracardi.domain.metadata import Metadata
from tracardi.domain.time import Time
from tracardi.service.storage.factory import StorageFor
from tracardi_plugin_sdk.domain.result import Result

from tracardi_event_scheduler.model.config import Config
from tracardi_event_scheduler.service.network import local_ip


def validate(config: dict) -> Config:
    return Config(**config)


class EventSchedulerAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)
        self.postpone = self.config.postpone

    async def run(self, payload):
        if self.debug:
            self.console.warning("Running scheduler in DEBUG MODE will not schedule new tasks.")
            return Result(port="payload", value={"message": "Running scheduler in DEBUG MODE will not "
                                                            "schedule new tasks."})

        now = time.time()
        future_time = now + self.postpone

        task = Task(
            timestamp=future_time,
            event=TaskEvent(
                metadata=Metadata(ip=local_ip, time=Time()),
                id=str(uuid4()),
                type=self.config.event_type,
                properties=self.config.properties,
                source=self.event.source,
                session=self.session,
                profile=self.profile,
                context=self.session.context if self.session is not None and self.session.context else Context(),
            ),
            event_type="test",
            status='pending'
        )
        await StorageFor(task).index().save()

        return Result(port="payload", value=task.dict())


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_event_scheduler.plugin',
            className='EventSchedulerAction',
            inputs=["payload"],
            outputs=["payload"],
            version='0.6.0',
            license="MIT",
            author="Risto Kowaczewski",
            manual="event_scheduler_action",
            init={
                "event_type": None,
                "properties": {},
                "postpone": "+1m"
            },
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id="event_type",
                            name="Event type",
                            description="Type event type you would like to schedule.",
                            component=FormComponent(type="text", props={"label": "Event type"})
                        ),
                        FormField(
                            id="properties",
                            name="Properties fo event",
                            description="Provide object as JSON to be injected into properties of scheduled event.",
                            component=FormComponent(type="json", props={"label": "object"})
                        ),
                        FormField(
                            id="postpone",
                            name="Time to postpone event",
                            description="Type how much time you would like the event to be postponed. "
                                        "e.g +1m means 1 minute. +1s means - 1 second, etc.",
                            component=FormComponent(type="text", props={"label": "Time to postpone the event"})
                        ),
                    ]
                ),
            ])

        ),
        metadata=MetaData(
            name='Event scheduler',
            desc='Schedule event to trigger after defined period of time.',
            type='flowNode',
            width=200,
            height=100,
            icon='event',
            group=["Input/Output"]
        )
    )

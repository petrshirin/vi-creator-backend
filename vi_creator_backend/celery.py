import os

from celery import Celery
from django.conf import settings
from django.utils.module_loading import import_string


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vi_creator_backend.settings")

app = Celery("vi_creator_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
app.conf.timezone = settings.TIME_ZONE
app.conf.task_always_eager = getattr(settings, "CELERY_ALWAYS_EAGER", False)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_CREATE_MISSING_QUEUES = True
CELERY_BROKER_TRANSPORT = "redis"
CELERY_RESULT_BACKEND = "django-db"


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from django_celery_beat.models import PeriodicTask, PeriodicTasks

    PeriodicTask.objects.update(last_run_at=None)
    unregistered_tasks_ids_by_name = dict(
        PeriodicTask.objects.filter(task__startswith="vi-creator").values_list("task", "id").iterator()
    )
    PeriodicTasks.update_changed()

    for app_name, options in settings.CELERY_BEAT_SCHEDULE.items():
        if app_name not in settings.INSTALLED_APPS:
            continue

        for func_name, task_kwargs in options.items():
            func_namespace = f"{app_name}.tasks.{func_name}"
            try:
                task = import_string(func_namespace)
                task_name = task_kwargs.pop("name", func_namespace)
                schedule = task_kwargs.pop("schedule")
                sender.add_periodic_task(schedule, task, name=task_name, kwargs=task_kwargs)
                unregistered_tasks_ids_by_name.pop(func_namespace, None)
                print(f"INFO: registry periodic task {func_namespace}")
            except ImportError:
                print(f"WARN: Add periodic task import error {func_namespace}")
            except Exception as e:
                print(f"ERROR: Add periodic task error: {e.args[0]}")

    unregistered_tasks_ids = tuple(unregistered_tasks_ids_by_name.values())
    if unregistered_tasks_ids:
        PeriodicTask.objects.filter(id__in=unregistered_tasks_ids).delete()
        PeriodicTasks.update_changed()
        for task_name in unregistered_tasks_ids_by_name.keys():
            print(f"INFO: Deleted periodic tasks {task_name}")

from celery import shared_task


@shared_task
def my_add(x, y):
    return x + y


@shared_task
def my_mul(x, y):
    return x * y

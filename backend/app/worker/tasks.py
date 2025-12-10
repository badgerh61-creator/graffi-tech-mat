# Celery tasks stub
from celery import Celery
import os
broker = os.getenv('CELERY_BROKER_URL','redis://redis:6379/0')
cel = Celery('graffi', broker=broker)

@cel.task
def generate_thumbnail(asset_id):
    # placeholder: implement thumbnail generation logic
    return {'asset_id': asset_id, 'status': 'ok'}

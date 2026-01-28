from datetime import timedelta
from freezegun import freeze_time

def advance_time(*, seconds: int):
    return freeze_time(timedelta(seconds=seconds))


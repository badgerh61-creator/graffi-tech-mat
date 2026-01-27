from enum import Enum

class StudioMode(str, Enum):
    editing = "editing"
    review = "review"
    read_only = "read_only"


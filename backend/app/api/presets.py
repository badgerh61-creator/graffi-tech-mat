from fastapi import APIRouter
router = APIRouter()

@router.get('/thumbnail-sizes')
def thumbnail_sizes():
    return {'sizes': [64, 128, 256, 512]}

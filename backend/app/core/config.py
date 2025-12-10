from pydantic import BaseSettings
import os, json
class Settings(BaseSettings):
    ENV: str = os.getenv('ENV','development')
    DATABASE_URL: str = os.getenv('DATABASE_URL','sqlite:///./graffi.db')
    AWS_ACCESS_KEY_ID: str | None = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: str | None = os.getenv('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET: str | None = os.getenv('S3_BUCKET')
    S3_ENDPOINT_URL: str | None = os.getenv('S3_ENDPOINT_URL')
    AWS_REGION: str | None = os.getenv('AWS_REGION','us-east-1')
    CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL','redis://redis:6379/0')
    SECRET_KEY: str = os.getenv('SECRET_KEY','')
    CORS_ORIGINS = ['*']

settings = Settings()

def parse_cors(raw=None):
    raw = raw or os.getenv('CORS_ORIGINS')
    if not raw:
        return ['*']
    try:
        raw = raw.strip()
        if raw.startswith('['):
            return json.loads(raw)
        return [r.strip() for r in raw.split(',') if r.strip()]
    except Exception:
        return [raw]

def validate_settings(required_keys=None):
    req = required_keys or ['SECRET_KEY','DATABASE_URL','AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY','S3_BUCKET','CELERY_BROKER_URL']
    missing = [k for k in req if not os.getenv(k)]
    if missing:
        raise RuntimeError('Missing required environment variables: ' + ', '.join(missing))
    return True

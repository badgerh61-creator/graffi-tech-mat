from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    # ================= ENV =================
    ENV: str = os.getenv("ENV", "development")

    # ================= SECURITY =================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "14")
    )

    # ================= DATABASE =================
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./graffi.db"
    )

    # ================= STORAGE (S3 / MINIO) =================
    AWS_ACCESS_KEY_ID: str | None = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    S3_BUCKET: str | None = os.getenv("S3_BUCKET")
    S3_ENDPOINT_URL: str | None = os.getenv("S3_ENDPOINT_URL")

    MINIO_ACCESS_KEY: str | None = AWS_ACCESS_KEY_ID
    MINIO_SECRET_KEY: str | None = AWS_SECRET_ACCESS_KEY
    MINIO_BUCKET: str | None = S3_BUCKET
    MINIO_ENDPOINT: str | None = None
    MINIO_SECURE: bool = False

    # ================= EMAIL (SENDGRID — PHASE C3) =================
    SENDGRID_API_KEY: str | None = os.getenv("SENDGRID_API_KEY")
    EMAIL_FROM: str = os.getenv(
        "EMAIL_FROM",
        "Graffi Studio <no-reply@graffi.app>",
    )
    FRONTEND_BASE_URL: str = os.getenv(
        "FRONTEND_BASE_URL",
        "http://localhost:5173",
    )

    # ================= CELERY =================
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL",
        "redis://localhost:6379/0",
    )

    # ================= CORS =================
    CORS_ORIGINS = ["*"]

    def __init__(self, **values):
        super().__init__(**values)

        if self.S3_ENDPOINT_URL:
            self.MINIO_SECURE = self.S3_ENDPOINT_URL.startswith("https")
            self.MINIO_ENDPOINT = (
                self.S3_ENDPOINT_URL
                .replace("http://", "")
                .replace("https://", "")
            )


settings = Settings()


def validate_settings():
    required = [
        settings.MINIO_ACCESS_KEY,
        settings.MINIO_SECRET_KEY,
        settings.MINIO_BUCKET,
        settings.MINIO_ENDPOINT,
    ]

    if not all(required):
        raise RuntimeError(
            "Missing MinIO / S3 configuration. "
            "Check AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "
            "S3_BUCKET, and S3_ENDPOINT_URL in .env"
        )


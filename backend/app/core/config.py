"""
إعدادات التطبيق الأساسية
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """إعدادات التطبيق"""
    
    # إعدادات التطبيق الأساسية
    app_name: str = "SAMIRMAX AI Studio"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # إعدادات قاعدة البيانات
    database_url: str = "postgresql://user:password@localhost/samirmax_ai"
    redis_url: str = "redis://localhost:6379"
    
    # إعدادات API keys
    openai_api_key: Optional[str] = None
    huggingface_token: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # إعدادات الملفات
    upload_dir: str = "uploads"
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_image_types: list = ["jpg", "jpeg", "png", "webp"]
    allowed_video_types: list = ["mp4", "avi", "mov", "mkv"]
    
    # إعدادات معالجة الذكاء الاصطناعي
    max_generation_time: int = 300  # 5 دقائق
    default_image_size: tuple = (1024, 1024)
    default_video_duration: int = 30  # ثانية
    
    # إعدادات الأمان
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # إعدادات CORS
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ]
    
    # إعدادات Celery للمهام الثقيلة
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# إنشاء كائن الإعدادات
settings = Settings()

# إنشاء مجلدات الرفع إذا لم تكن موجودة
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(f"{settings.upload_dir}/images", exist_ok=True)
os.makedirs(f"{settings.upload_dir}/videos", exist_ok=True)
os.makedirs(f"{settings.upload_dir}/temp", exist_ok=True)
"""
نظام السجلات المتقدم للتطبيق
"""
import sys
from loguru import logger
from typing import Dict, Any
import json


def serialize_record(record: Dict[str, Any]) -> str:
    """تحويل سجل إلى JSON للمعالجة"""
    subset = {
        "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["module"],
        "function": record["function"],
        "line": record["line"]
    }
    return json.dumps(subset, ensure_ascii=False)


def setup_logger():
    """إعداد نظام السجلات"""
    
    # إزالة التكوين الافتراضي
    logger.remove()
    
    # إضافة تسجيل للوحة التحكم مع الألوان
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # إضافة تسجيل للملفات
    logger.add(
        "logs/samirmax_ai.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="50 MB",
        retention="7 days",
        compression="zip"
    )
    
    # إضافة تسجيل للأخطاء
    logger.add(
        "logs/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="10 MB",
        retention="30 days"
    )
    
    # إضافة تسجيل JSON للتحليل
    logger.add(
        "logs/analytics.json",
        format=serialize_record,
        level="INFO",
        rotation="100 MB",
        retention="30 days",
        serialize=True
    )
    
    return logger


# إنشاء مجلد السجلات
import os
os.makedirs("logs", exist_ok=True)
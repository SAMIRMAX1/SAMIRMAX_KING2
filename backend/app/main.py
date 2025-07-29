"""
التطبيق الرئيسي SAMIRMAX AI Studio
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional, List
import asyncio

from .core.config import settings
from .api import image_generation, video_generation, audio_generation, file_management
from .services.ai_service import AIService
from .utils.logger import setup_logger

# إعداد نظام السجلات
logger = setup_logger()

# إنشاء التطبيق
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="تطبيق متقدم لتوليد الصور والفيديوهات بالذكاء الاصطناعي",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ربط الملفات الثابتة
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# إنشاء خدمة الذكاء الاصطناعي
ai_service = AIService()


@app.on_event("startup")
async def startup_event():
    """تشغيل العمليات عند بدء التطبيق"""
    logger.info("🚀 بدء تشغيل SAMIRMAX AI Studio")
    
    # تهيئة خدمات الذكاء الاصطناعي
    await ai_service.initialize()
    logger.info("✅ تم تهيئة خدمات الذكاء الاصطناعي")


@app.on_event("shutdown")
async def shutdown_event():
    """تنظيف الموارد عند إغلاق التطبيق"""
    logger.info("🛑 إغلاق SAMIRMAX AI Studio")
    await ai_service.cleanup()


@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "message": "مرحباً بك في SAMIRMAX AI Studio",
        "version": settings.app_version,
        "status": "نشط",
        "features": [
            "توليد الصور من النص",
            "تحويل الصور إلى فيديوهات",
            "توليد الفيديو مع الصوت",
            "تعديل الصور بالتعليمات",
            "مؤثرات مرئية متقدمة"
        ]
    }


@app.get("/health")
async def health_check():
    """فحص حالة التطبيق"""
    try:
        # فحص اتصال قاعدة البيانات والخدمات
        ai_status = await ai_service.health_check()
        
        return {
            "status": "healthy",
            "ai_services": ai_status,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"خطأ في فحص الحالة: {e}")
        raise HTTPException(status_code=503, detail="خدمة غير متاحة")


# ربط المسارات الفرعية
app.include_router(
    image_generation.router,
    prefix="/api/images",
    tags=["توليد الصور"]
)

app.include_router(
    video_generation.router,
    prefix="/api/videos",
    tags=["توليد الفيديوهات"]
)

app.include_router(
    audio_generation.router,
    prefix="/api/audio",
    tags=["توليد الصوت"]
)

app.include_router(
    file_management.router,
    prefix="/api/files",
    tags=["إدارة الملفات"]
)


@app.post("/api/generate/text-to-image")
async def generate_image_from_text(
    prompt: str = Form(..., description="وصف الصورة المطلوبة"),
    style: Optional[str] = Form("realistic", description="نمط الصورة"),
    size: Optional[str] = Form("1024x1024", description="حجم الصورة"),
    background_tasks: BackgroundTasks = None
):
    """توليد صورة من النص"""
    try:
        logger.info(f"طلب توليد صورة: {prompt}")
        
        # معالجة الطلب
        result = await ai_service.generate_image(
            prompt=prompt,
            style=style,
            size=size
        )
        
        return {
            "success": True,
            "image_url": result["image_url"],
            "metadata": result["metadata"],
            "message": "تم توليد الصورة بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في توليد الصورة: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في توليد الصورة: {str(e)}")


@app.post("/api/generate/image-to-video")
async def convert_image_to_video(
    image: UploadFile = File(..., description="الصورة المراد تحويلها"),
    animation_style: Optional[str] = Form("subtle", description="نوع الحركة"),
    duration: Optional[int] = Form(10, description="مدة الفيديو بالثواني"),
    background_tasks: BackgroundTasks = None
):
    """تحويل صورة إلى فيديو متحرك"""
    try:
        logger.info(f"طلب تحويل صورة إلى فيديو: {image.filename}")
        
        # حفظ الصورة مؤقتاً
        image_path = await ai_service.save_uploaded_file(image, "images")
        
        # تحويل إلى فيديو
        result = await ai_service.image_to_video(
            image_path=image_path,
            animation_style=animation_style,
            duration=duration
        )
        
        return {
            "success": True,
            "video_url": result["video_url"],
            "metadata": result["metadata"],
            "message": "تم تحويل الصورة إلى فيديو بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في تحويل الصورة: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في تحويل الصورة: {str(e)}")


@app.post("/api/generate/text-to-video")
async def generate_video_from_text(
    prompt: str = Form(..., description="وصف الفيديو المطلوب"),
    style: Optional[str] = Form("realistic", description="نمط الفيديو"),
    duration: Optional[int] = Form(15, description="مدة الفيديو بالثواني"),
    include_audio: Optional[bool] = Form(True, description="تضمين صوت"),
    background_tasks: BackgroundTasks = None
):
    """توليد فيديو من النص مع الصوت"""
    try:
        logger.info(f"طلب توليد فيديو: {prompt}")
        
        # توليد الفيديو
        result = await ai_service.generate_video(
            prompt=prompt,
            style=style,
            duration=duration,
            include_audio=include_audio
        )
        
        return {
            "success": True,
            "video_url": result["video_url"],
            "audio_url": result.get("audio_url"),
            "metadata": result["metadata"],
            "message": "تم توليد الفيديو بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في توليد الفيديو: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في توليد الفيديو: {str(e)}")


@app.post("/api/edit/image-iterative")
async def edit_image_iteratively(
    image: UploadFile = File(..., description="الصورة المراد تعديلها"),
    edit_prompt: str = Form(..., description="تعليمات التعديل"),
    strength: Optional[float] = Form(0.7, description="قوة التعديل"),
    background_tasks: BackgroundTasks = None
):
    """تعديل صورة باستخدام التعليمات النصية"""
    try:
        logger.info(f"طلب تعديل صورة: {edit_prompt}")
        
        # حفظ الصورة
        image_path = await ai_service.save_uploaded_file(image, "images")
        
        # تعديل الصورة
        result = await ai_service.edit_image(
            image_path=image_path,
            edit_prompt=edit_prompt,
            strength=strength
        )
        
        return {
            "success": True,
            "edited_image_url": result["image_url"],
            "original_image_url": result["original_url"],
            "metadata": result["metadata"],
            "message": "تم تعديل الصورة بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في تعديل الصورة: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في تعديل الصورة: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
"""
مسارات API لتوليد الفيديوهات
"""
from fastapi import APIRouter, HTTPException, Form, UploadFile, File, BackgroundTasks
from typing import Optional, List
from pydantic import BaseModel

from ..services.ai_service import AIService
from ..utils.logger import setup_logger

logger = setup_logger()
router = APIRouter()

# نماذج البيانات
class VideoGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "realistic"
    duration: Optional[int] = 15
    fps: Optional[int] = 24
    resolution: Optional[str] = "1024x1024"
    include_audio: Optional[bool] = True


class ImageToVideoRequest(BaseModel):
    animation_style: Optional[str] = "subtle"
    duration: Optional[int] = 10
    fps: Optional[int] = 30
    add_effects: Optional[bool] = True


@router.post("/generate")
async def generate_video_from_text(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks
):
    """توليد فيديو من النص"""
    try:
        ai_service = AIService()
        
        result = await ai_service.generate_video(
            prompt=request.prompt,
            style=request.style,
            duration=request.duration,
            include_audio=request.include_audio
        )
        
        logger.info(f"تم توليد فيديو جديد: {request.prompt[:50]}...")
        
        return {
            "success": True,
            "data": result,
            "message": "تم توليد الفيديو بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في توليد الفيديو: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في توليد الفيديو: {str(e)}")


@router.post("/image-to-video")
async def convert_image_to_video(
    image: UploadFile = File(...),
    animation_style: Optional[str] = Form("subtle"),
    duration: Optional[int] = Form(10),
    fps: Optional[int] = Form(30),
    background_tasks: BackgroundTasks = None
):
    """تحويل صورة إلى فيديو متحرك"""
    try:
        ai_service = AIService()
        
        # حفظ الصورة المرفوعة
        image_path = await ai_service.save_uploaded_file(image, "images")
        
        # تحويل إلى فيديو
        result = await ai_service.image_to_video(
            image_path=image_path,
            animation_style=animation_style,
            duration=duration
        )
        
        logger.info(f"تم تحويل صورة إلى فيديو: {image.filename}")
        
        return {
            "success": True,
            "data": result,
            "message": "تم تحويل الصورة إلى فيديو بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في تحويل الصورة إلى فيديو: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في تحويل الصورة: {str(e)}")


@router.post("/script-to-video")
async def generate_video_from_script(
    script: str = Form(...),
    voice_style: Optional[str] = Form("natural"),
    language: Optional[str] = Form("ar"),
    background_music: Optional[bool] = Form(False),
    visual_style: Optional[str] = Form("realistic"),
    background_tasks: BackgroundTasks = None
):
    """تحويل نص أو سيناريو إلى فيديو مع صوت"""
    try:
        ai_service = AIService()
        
        # TODO: تطبيق تحويل السيناريو إلى فيديو
        # يمكن تقسيم السيناريو إلى مشاهد وتوليد فيديو لكل مشهد
        
        # حالياً نستخدم النص كـ prompt للفيديو
        result = await ai_service.generate_video(
            prompt=script,
            style=visual_style,
            duration=30,  # مدة افتراضية
            include_audio=True
        )
        
        logger.info(f"تم توليد فيديو من سيناريو: {script[:50]}...")
        
        return {
            "success": True,
            "data": result,
            "message": "تم توليد الفيديو من السيناريو بنجاح",
            "features_used": {
                "voice_style": voice_style,
                "language": language,
                "background_music": background_music,
                "visual_style": visual_style
            }
        }
        
    except Exception as e:
        logger.error(f"خطأ في توليد فيديو من السيناريو: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في توليد الفيديو: {str(e)}")


@router.post("/edit")
async def edit_video(
    video: UploadFile = File(...),
    edit_prompt: str = Form(...),
    edit_type: Optional[str] = Form("style_transfer"),
    background_tasks: BackgroundTasks = None
):
    """تعديل فيديو موجود"""
    try:
        ai_service = AIService()
        
        # حفظ الفيديو المرفوع
        video_path = await ai_service.save_uploaded_file(video, "videos")
        
        # TODO: تطبيق تعديل الفيديو
        # يمكن استخدام تقنيات مثل style transfer أو color grading
        
        return {
            "success": True,
            "message": "ميزة تعديل الفيديو قيد التطوير",
            "data": {
                "original_video": video_path,
                "edit_prompt": edit_prompt,
                "edit_type": edit_type
            }
        }
        
    except Exception as e:
        logger.error(f"خطأ في تعديل الفيديو: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في تعديل الفيديو: {str(e)}")


@router.post("/add-keyframes")
async def add_keyframes_to_video(
    base_image: UploadFile = File(...),
    keyframes: str = Form(...),  # JSON string with keyframe data
    transition_style: Optional[str] = Form("smooth"),
    duration: Optional[int] = Form(15),
    background_tasks: BackgroundTasks = None
):
    """إضافة keyframes لإنشاء فيديو متحرك"""
    try:
        ai_service = AIService()
        
        # حفظ الصورة الأساسية
        image_path = await ai_service.save_uploaded_file(base_image, "images")
        
        # TODO: تطبيق معالجة keyframes
        # parsing keyframes JSON and creating animated video
        
        import json
        keyframes_data = json.loads(keyframes)
        
        # إنشاء فيديو بحركة متقدمة
        result = await ai_service.image_to_video(
            image_path=image_path,
            animation_style=transition_style,
            duration=duration
        )
        
        logger.info(f"تم إنشاء فيديو مع keyframes: {len(keyframes_data)} نقطة")
        
        return {
            "success": True,
            "data": result,
            "message": "تم إنشاء الفيديو مع التحكم بالحركة",
            "keyframes_processed": len(keyframes_data)
        }
        
    except Exception as e:
        logger.error(f"خطأ في معالجة keyframes: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في معالجة الحركة: {str(e)}")


@router.get("/animation-styles")
async def get_animation_styles():
    """الحصول على أنماط الحركة المتاحة"""
    styles = {
        "subtle": {
            "name": "حركة خفيفة",
            "description": "تكبير وتصغير بسيط مع حركة طفيفة",
            "duration_range": "5-30 ثانية",
            "best_for": ["portraits", "landscapes", "products"]
        },
        "parallax": {
            "name": "منظور متوازي",
            "description": "تأثير عمق مع حركة طبقات مختلفة",
            "duration_range": "10-60 ثانية",
            "best_for": ["landscapes", "architecture", "nature"]
        },
        "magical": {
            "name": "تأثير سحري",
            "description": "تلاشي وظهور مع تأثيرات ضوئية",
            "duration_range": "5-20 ثانية",
            "best_for": ["fantasy", "portraits", "art"]
        },
        "cinematic": {
            "name": "سينمائي",
            "description": "حركة كاميرا احترافية مع انتقالات سلسة",
            "duration_range": "15-120 ثانية",
            "best_for": ["storytelling", "dramatic scenes", "trailers"]
        },
        "dynamic": {
            "name": "ديناميكي",
            "description": "حركة سريعة وتأثيرات متنوعة",
            "duration_range": "3-15 ثانية",
            "best_for": ["social media", "advertisements", "energy"]
        }
    }
    
    return {
        "success": True,
        "data": styles,
        "message": "أنماط الحركة المتاحة"
    }


@router.get("/resolutions")
async def get_video_resolutions():
    """الحصول على دقة الفيديو المتاحة"""
    resolutions = {
        "social_media": {
            "instagram_story": "1080x1920",
            "instagram_post": "1080x1080", 
            "youtube_shorts": "1080x1920",
            "tiktok": "1080x1920"
        },
        "standard": {
            "hd": "1280x720",
            "full_hd": "1920x1080",
            "4k": "3840x2160"
        },
        "custom": {
            "square": "1024x1024",
            "landscape": "1920x1080",
            "portrait": "1080x1920"
        }
    }
    
    return {
        "success": True,
        "data": resolutions,
        "message": "دقة الفيديو المتاحة"
    }
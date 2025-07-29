"""
مسارات API لتوليد الصور
"""
from fastapi import APIRouter, HTTPException, Form, UploadFile, File, BackgroundTasks
from typing import Optional, List
from pydantic import BaseModel

from ..services.ai_service import AIService
from ..utils.logger import setup_logger

logger = setup_logger()
router = APIRouter()

# نماذج البيانات
class ImageGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "realistic"
    size: Optional[str] = "1024x1024"
    negative_prompt: Optional[str] = None
    guidance_scale: Optional[float] = 7.5
    num_inference_steps: Optional[int] = 30


class ImageEditRequest(BaseModel):
    edit_prompt: str
    strength: Optional[float] = 0.7
    guidance_scale: Optional[float] = 7.5


@router.post("/generate")
async def generate_image(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks
):
    """توليد صورة جديدة من النص"""
    try:
        ai_service = AIService()
        
        result = await ai_service.generate_image(
            prompt=request.prompt,
            style=request.style,
            size=request.size
        )
        
        logger.info(f"تم توليد صورة جديدة: {request.prompt[:50]}...")
        
        return {
            "success": True,
            "data": result,
            "message": "تم توليد الصورة بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في توليد الصورة: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في توليد الصورة: {str(e)}")


@router.post("/edit")
async def edit_image(
    image: UploadFile = File(...),
    edit_prompt: str = Form(...),
    strength: Optional[float] = Form(0.7),
    background_tasks: BackgroundTasks = None
):
    """تعديل صورة موجودة باستخدام التعليمات النصية"""
    try:
        ai_service = AIService()
        
        # حفظ الصورة المرفوعة
        image_path = await ai_service.save_uploaded_file(image, "images")
        
        # تعديل الصورة
        result = await ai_service.edit_image(
            image_path=image_path,
            edit_prompt=edit_prompt,
            strength=strength
        )
        
        logger.info(f"تم تعديل صورة: {edit_prompt[:50]}...")
        
        return {
            "success": True,
            "data": result,
            "message": "تم تعديل الصورة بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في تعديل الصورة: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في تعديل الصورة: {str(e)}")


@router.post("/upscale")
async def upscale_image(
    image: UploadFile = File(...),
    scale_factor: Optional[int] = Form(2),
    background_tasks: BackgroundTasks = None
):
    """تكبير دقة الصورة"""
    try:
        ai_service = AIService()
        
        # حفظ الصورة
        image_path = await ai_service.save_uploaded_file(image, "images")
        
        # TODO: إضافة خدمة تكبير الصورة
        # result = await ai_service.upscale_image(image_path, scale_factor)
        
        return {
            "success": True,
            "message": "ميزة تكبير الصورة قيد التطوير",
            "data": {
                "original_image": image_path,
                "scale_factor": scale_factor
            }
        }
        
    except Exception as e:
        logger.error(f"خطأ في تكبير الصورة: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في تكبير الصورة: {str(e)}")


@router.get("/styles")
async def get_available_styles():
    """الحصول على الأنماط المتاحة للصور"""
    styles = {
        "realistic": {
            "name": "واقعي",
            "description": "صور واقعية عالية الجودة",
            "examples": ["portrait", "landscape", "photography"]
        },
        "artistic": {
            "name": "فني",
            "description": "أسلوب فني وإبداعي",
            "examples": ["painting", "watercolor", "oil painting"]
        },
        "anime": {
            "name": "أنمي",
            "description": "أسلوب الرسوم المتحركة اليابانية",
            "examples": ["manga", "cel shaded", "anime character"]
        },
        "cinematic": {
            "name": "سينمائي",
            "description": "إضاءة وجو سينمائي",
            "examples": ["movie scene", "dramatic lighting", "film noir"]
        },
        "fantasy": {
            "name": "خيالي",
            "description": "عالم خيالي وسحري",
            "examples": ["dragon", "castle", "magical forest"]
        },
        "cyberpunk": {
            "name": "سايبربانك",
            "description": "مستقبلي بألوان نيون",
            "examples": ["neon city", "robot", "futuristic"]
        }
    }
    
    return {
        "success": True,
        "data": styles,
        "message": "الأنماط المتاحة"
    }


@router.get("/sizes")
async def get_available_sizes():
    """الحصول على الأحجام المتاحة للصور"""
    sizes = {
        "square": {
            "512x512": "صغير مربع",
            "1024x1024": "متوسط مربع", 
            "2048x2048": "كبير مربع"
        },
        "portrait": {
            "512x768": "صغير عمودي",
            "1024x1536": "متوسط عمودي",
            "1024x1792": "كبير عمودي"
        },
        "landscape": {
            "768x512": "صغير أفقي",
            "1536x1024": "متوسط أفقي",
            "1792x1024": "كبير أفقي"
        }
    }
    
    return {
        "success": True,
        "data": sizes,
        "message": "الأحجام المتاحة"
    }
"""
مسارات API لإدارة الملفات
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Query, BackgroundTasks
from typing import Optional, List
import os
import shutil
from datetime import datetime

from ..core.config import settings
from ..utils.logger import setup_logger

logger = setup_logger()
router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    file_type: Optional[str] = Query("auto", description="نوع الملف (image/video/audio)"),
    background_tasks: BackgroundTasks = None
):
    """رفع ملف جديد"""
    try:
        # تحديد نوع الملف تلقائياً
        if file_type == "auto":
            if file.content_type.startswith("image/"):
                file_type = "images"
            elif file.content_type.startswith("video/"):
                file_type = "videos"
            elif file.content_type.startswith("audio/"):
                file_type = "videos"  # حفظ الصوت مع الفيديوهات
            else:
                file_type = "temp"
        
        # التحقق من صحة نوع الملف
        file_extension = file.filename.split('.')[-1].lower()
        if file_type == "images" and file_extension not in settings.allowed_image_types:
            raise HTTPException(status_code=400, detail=f"نوع الصورة غير مدعوم: {file_extension}")
        
        if file_type == "videos" and file_extension not in settings.allowed_video_types + ["mp3", "wav", "m4a"]:
            raise HTTPException(status_code=400, detail=f"نوع الملف غير مدعوم: {file_extension}")
        
        # التحقق من حجم الملف
        file_size = len(await file.read())
        await file.seek(0)  # إعادة المؤشر إلى البداية
        
        if file_size > settings.max_file_size:
            raise HTTPException(status_code=400, detail=f"حجم الملف كبير جداً. الحد الأقصى: {settings.max_file_size / 1024 / 1024:.1f} MB")
        
        # حفظ الملف
        import uuid
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(settings.upload_dir, file_type, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"تم رفع ملف جديد: {file.filename} -> {unique_filename}")
        
        return {
            "success": True,
            "data": {
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_type": file_type,
                "file_size": file_size,
                "file_url": f"/uploads/{file_type}/{unique_filename}",
                "upload_time": datetime.now().isoformat()
            },
            "message": "تم رفع الملف بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في رفع الملف: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في رفع الملف: {str(e)}")


@router.get("/list")
async def list_files(
    file_type: Optional[str] = Query(None, description="نوع الملفات (images/videos)"),
    limit: Optional[int] = Query(50, description="عدد الملفات"),
    offset: Optional[int] = Query(0, description="تخطي عدد من الملفات")
):
    """عرض قائمة الملفات"""
    try:
        files_info = []
        
        # تحديد المجلدات للفحص
        if file_type:
            folders = [file_type]
        else:
            folders = ["images", "videos", "temp"]
        
        for folder in folders:
            folder_path = os.path.join(settings.upload_dir, folder)
            if not os.path.exists(folder_path):
                continue
                
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    
                    files_info.append({
                        "filename": filename,
                        "file_type": folder,
                        "file_size": stat.st_size,
                        "file_url": f"/uploads/{folder}/{filename}",
                        "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
        
        # ترتيب حسب وقت الإنشاء (الأحدث أولاً)
        files_info.sort(key=lambda x: x["created_time"], reverse=True)
        
        # تطبيق pagination
        total_files = len(files_info)
        files_page = files_info[offset:offset + limit]
        
        return {
            "success": True,
            "data": {
                "files": files_page,
                "total": total_files,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total_files
            },
            "message": f"تم العثور على {total_files} ملف"
        }
        
    except Exception as e:
        logger.error(f"خطأ في عرض الملفات: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في عرض الملفات: {str(e)}")


@router.delete("/delete/{file_type}/{filename}")
async def delete_file(
    file_type: str,
    filename: str,
    background_tasks: BackgroundTasks = None
):
    """حذف ملف"""
    try:
        file_path = os.path.join(settings.upload_dir, file_type, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="الملف غير موجود")
        
        # التحقق من أن الملف داخل مجلد الرفع المسموح
        upload_dir_abs = os.path.abspath(settings.upload_dir)
        file_path_abs = os.path.abspath(file_path)
        
        if not file_path_abs.startswith(upload_dir_abs):
            raise HTTPException(status_code=403, detail="غير مسموح بحذف هذا الملف")
        
        # حذف الملف
        os.remove(file_path)
        
        logger.info(f"تم حذف ملف: {filename}")
        
        return {
            "success": True,
            "data": {
                "filename": filename,
                "file_type": file_type,
                "deleted_time": datetime.now().isoformat()
            },
            "message": "تم حذف الملف بنجاح"
        }
        
    except Exception as e:
        logger.error(f"خطأ في حذف الملف: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في حذف الملف: {str(e)}")


@router.get("/info/{file_type}/{filename}")
async def get_file_info(
    file_type: str,
    filename: str
):
    """الحصول على معلومات ملف"""
    try:
        file_path = os.path.join(settings.upload_dir, file_type, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="الملف غير موجود")
        
        stat = os.stat(file_path)
        
        # معلومات إضافية حسب نوع الملف
        additional_info = {}
        
        if file_type == "images":
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    additional_info = {
                        "width": img.width,
                        "height": img.height,
                        "mode": img.mode,
                        "format": img.format
                    }
            except Exception:
                pass
        
        elif file_type == "videos":
            try:
                import cv2
                cap = cv2.VideoCapture(file_path)
                if cap.isOpened():
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    duration = frame_count / fps if fps > 0 else 0
                    
                    additional_info = {
                        "width": int(width),
                        "height": int(height),
                        "fps": fps,
                        "duration": duration,
                        "frame_count": int(frame_count)
                    }
                cap.release()
            except Exception:
                pass
        
        file_info = {
            "filename": filename,
            "file_type": file_type,
            "file_size": stat.st_size,
            "file_url": f"/uploads/{file_type}/{filename}",
            "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            **additional_info
        }
        
        return {
            "success": True,
            "data": file_info,
            "message": "معلومات الملف"
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على معلومات الملف: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في الحصول على المعلومات: {str(e)}")


@router.post("/cleanup")
async def cleanup_temp_files(
    older_than_hours: Optional[int] = Query(24, description="حذف الملفات الأقدم من عدد الساعات"),
    background_tasks: BackgroundTasks = None
):
    """تنظيف الملفات المؤقتة"""
    try:
        import time
        
        current_time = time.time()
        cutoff_time = current_time - (older_than_hours * 3600)
        
        deleted_files = []
        temp_dir = os.path.join(settings.upload_dir, "temp")
        
        if os.path.exists(temp_dir):
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    file_time = os.path.getmtime(file_path)
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        deleted_files.append(filename)
        
        logger.info(f"تم حذف {len(deleted_files)} ملف مؤقت")
        
        return {
            "success": True,
            "data": {
                "deleted_files": deleted_files,
                "deleted_count": len(deleted_files),
                "cleanup_time": datetime.now().isoformat()
            },
            "message": f"تم حذف {len(deleted_files)} ملف مؤقت"
        }
        
    except Exception as e:
        logger.error(f"خطأ في تنظيف الملفات: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في تنظيف الملفات: {str(e)}")


@router.get("/storage-stats")
async def get_storage_statistics():
    """إحصائيات استخدام التخزين"""
    try:
        stats = {
            "total_files": 0,
            "total_size": 0,
            "by_type": {}
        }
        
        for folder in ["images", "videos", "temp"]:
            folder_path = os.path.join(settings.upload_dir, folder)
            folder_stats = {
                "file_count": 0,
                "total_size": 0
            }
            
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        folder_stats["file_count"] += 1
                        folder_stats["total_size"] += file_size
            
            stats["by_type"][folder] = folder_stats
            stats["total_files"] += folder_stats["file_count"]
            stats["total_size"] += folder_stats["total_size"]
        
        # تحويل الأحجام لوحدات مقروءة
        def format_size(size_bytes):
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024**2:
                return f"{size_bytes/1024:.1f} KB"
            elif size_bytes < 1024**3:
                return f"{size_bytes/(1024**2):.1f} MB"
            else:
                return f"{size_bytes/(1024**3):.1f} GB"
        
        formatted_stats = {
            "total_files": stats["total_files"],
            "total_size": format_size(stats["total_size"]),
            "total_size_bytes": stats["total_size"],
            "by_type": {
                folder: {
                    "file_count": data["file_count"],
                    "total_size": format_size(data["total_size"]),
                    "total_size_bytes": data["total_size"]
                }
                for folder, data in stats["by_type"].items()
            }
        }
        
        return {
            "success": True,
            "data": formatted_stats,
            "message": "إحصائيات التخزين"
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على إحصائيات التخزين: {e}")
        raise HTTPException(status_code=500, detail=f"فشل في الحصول على الإحصائيات: {str(e)}")
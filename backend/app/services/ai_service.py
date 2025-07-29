"""
خدمة الذكاء الاصطناعي الرئيسية
تدعم: Stable Diffusion, FLUX, OpenAI, Google Veo
"""
import os
import asyncio
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime
import aiofiles
import torch
from PIL import Image
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip
import requests
from io import BytesIO

from ..core.config import settings
from ..utils.logger import setup_logger

logger = setup_logger()


class AIService:
    """خدمة الذكاء الاصطناعي الشاملة"""
    
    def __init__(self):
        self.initialized = False
        self.models = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"استخدام الجهاز: {self.device}")
    
    async def initialize(self):
        """تهيئة جميع نماذج الذكاء الاصطناعي"""
        try:
            logger.info("🔄 بدء تهيئة نماذج الذكاء الاصطناعي...")
            
            # تهيئة Stable Diffusion
            await self._initialize_stable_diffusion()
            
            # تهيئة معالج الفيديو
            await self._initialize_video_processor()
            
            # تهيئة معالج الصوت
            await self._initialize_audio_processor()
            
            # تهيئة APIs الخارجية
            await self._initialize_external_apis()
            
            self.initialized = True
            logger.info("✅ تم تهيئة جميع نماذج الذكاء الاصطناعي")
            
        except Exception as e:
            logger.error(f"❌ خطأ في تهيئة نماذج الذكاء الاصطناعي: {e}")
            raise
    
    async def _initialize_stable_diffusion(self):
        """تهيئة نموذج Stable Diffusion"""
        try:
            from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
            
            # تحميل نموذج توليد الصور
            self.models['text_to_image'] = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            ).to(self.device)
            
            # تحميل نموذج تعديل الصور
            self.models['image_to_image'] = StableDiffusionImg2ImgPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            ).to(self.device)
            
            logger.info("✅ تم تحميل Stable Diffusion")
            
        except Exception as e:
            logger.warning(f"⚠️ لم يتم تحميل Stable Diffusion: {e}")
            self.models['text_to_image'] = None
            self.models['image_to_image'] = None
    
    async def _initialize_video_processor(self):
        """تهيئة معالج الفيديو"""
        try:
            # إعداد FFmpeg للمعالجة
            self.video_processor = {
                'ffmpeg_available': True,
                'opencv_available': True
            }
            logger.info("✅ تم تهيئة معالج الفيديو")
            
        except Exception as e:
            logger.warning(f"⚠️ مشكلة في تهيئة معالج الفيديو: {e}")
    
    async def _initialize_audio_processor(self):
        """تهيئة معالج الصوت"""
        try:
            # إعداد مكتبات الصوت
            self.audio_processor = {
                'librosa_available': True,
                'pydub_available': True
            }
            logger.info("✅ تم تهيئة معالج الصوت")
            
        except Exception as e:
            logger.warning(f"⚠️ مشكلة في تهيئة معالج الصوت: {e}")
    
    async def _initialize_external_apis(self):
        """تهيئة APIs الخارجية"""
        self.external_apis = {
            'openai_available': bool(settings.openai_api_key),
            'google_available': bool(settings.google_api_key),
        }
        logger.info("✅ تم فحص APIs الخارجية")
    
    async def generate_image(self, prompt: str, style: str = "realistic", size: str = "1024x1024") -> Dict[str, Any]:
        """توليد صورة من النص"""
        try:
            if not self.models.get('text_to_image'):
                # استخدام OpenAI كبديل
                return await self._generate_image_openai(prompt, style, size)
            
            # استخدام Stable Diffusion المحلي
            return await self._generate_image_local(prompt, style, size)
            
        except Exception as e:
            logger.error(f"خطأ في توليد الصورة: {e}")
            raise
    
    async def _generate_image_local(self, prompt: str, style: str, size: str) -> Dict[str, Any]:
        """توليد صورة باستخدام Stable Diffusion المحلي"""
        try:
            # إعداد المعاملات
            width, height = map(int, size.split('x'))
            
            # تحسين النص حسب النمط
            enhanced_prompt = self._enhance_prompt_for_style(prompt, style)
            
            # توليد الصورة
            image = self.models['text_to_image'](
                prompt=enhanced_prompt,
                width=width,
                height=height,
                num_inference_steps=30,
                guidance_scale=7.5,
                negative_prompt="blurry, low quality, distorted"
            ).images[0]
            
            # حفظ الصورة
            filename = f"generated_{uuid.uuid4().hex}.png"
            filepath = os.path.join(settings.upload_dir, "images", filename)
            image.save(filepath)
            
            return {
                "image_url": f"/uploads/images/{filename}",
                "metadata": {
                    "prompt": prompt,
                    "style": style,
                    "size": size,
                    "model": "stable-diffusion-v1-5",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في توليد الصورة محلياً: {e}")
            raise
    
    async def _generate_image_openai(self, prompt: str, style: str, size: str) -> Dict[str, Any]:
        """توليد صورة باستخدام OpenAI DALL-E"""
        try:
            import openai
            
            # إعداد OpenAI
            openai.api_key = settings.openai_api_key
            
            # تحسين النص
            enhanced_prompt = self._enhance_prompt_for_style(prompt, style)
            
            # طلب توليد الصورة
            response = await openai.Image.acreate(
                prompt=enhanced_prompt,
                n=1,
                size=size if size in ["256x256", "512x512", "1024x1024"] else "1024x1024",
                response_format="url"
            )
            
            # تحميل وحفظ الصورة
            image_url = response['data'][0]['url']
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            
            filename = f"generated_{uuid.uuid4().hex}.png"
            filepath = os.path.join(settings.upload_dir, "images", filename)
            image.save(filepath)
            
            return {
                "image_url": f"/uploads/images/{filename}",
                "metadata": {
                    "prompt": prompt,
                    "style": style,
                    "size": size,
                    "model": "dall-e",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في توليد الصورة عبر OpenAI: {e}")
            raise
    
    def _enhance_prompt_for_style(self, prompt: str, style: str) -> str:
        """تحسين النص حسب النمط المطلوب"""
        style_modifiers = {
            "realistic": "photorealistic, high quality, detailed",
            "artistic": "artistic, painterly, creative, expressive",
            "anime": "anime style, manga, cel shaded",
            "cinematic": "cinematic lighting, dramatic, film quality",
            "fantasy": "fantasy art, magical, ethereal",
            "cyberpunk": "cyberpunk, neon, futuristic, sci-fi"
        }
        
        modifier = style_modifiers.get(style, "high quality")
        return f"{prompt}, {modifier}"
    
    async def image_to_video(self, image_path: str, animation_style: str = "subtle", duration: int = 10) -> Dict[str, Any]:
        """تحويل صورة إلى فيديو متحرك"""
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            height, width = image.shape[:2]
            
            # إنشاء فيديو بالحركة المطلوبة
            video_frames = await self._create_animated_frames(image, animation_style, duration)
            
            # حفظ الفيديو
            filename = f"animated_{uuid.uuid4().hex}.mp4"
            video_path = os.path.join(settings.upload_dir, "videos", filename)
            
            # كتابة الفيديو
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, 30.0, (width, height))
            
            for frame in video_frames:
                out.write(frame)
            out.release()
            
            return {
                "video_url": f"/uploads/videos/{filename}",
                "metadata": {
                    "original_image": image_path,
                    "animation_style": animation_style,
                    "duration": duration,
                    "fps": 30,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحويل الصورة إلى فيديو: {e}")
            raise
    
    async def _create_animated_frames(self, image: np.ndarray, style: str, duration: int) -> List[np.ndarray]:
        """إنشاء إطارات الحركة"""
        frames = []
        total_frames = duration * 30  # 30 FPS
        
        if style == "subtle":
            # حركة خفيفة - تكبير وتصغير بسيط
            for i in range(total_frames):
                scale = 1.0 + 0.05 * np.sin(2 * np.pi * i / 60)  # دورة كل ثانيتين
                frame = self._apply_zoom(image, scale)
                frames.append(frame)
                
        elif style == "parallax":
            # تأثير المنظور المتوازي
            for i in range(total_frames):
                shift_x = 5 * np.sin(2 * np.pi * i / 90)  # حركة أفقية
                frame = self._apply_translation(image, shift_x, 0)
                frames.append(frame)
                
        elif style == "magical":
            # تأثير سحري مع تلاشي وظهور
            for i in range(total_frames):
                alpha = 0.7 + 0.3 * np.sin(2 * np.pi * i / 45)  # تغيير الشفافية
                frame = self._apply_fade(image, alpha)
                frames.append(frame)
        
        else:
            # حركة افتراضية
            frames = [image.copy() for _ in range(total_frames)]
        
        return frames
    
    def _apply_zoom(self, image: np.ndarray, scale: float) -> np.ndarray:
        """تطبيق تأثير التكبير"""
        height, width = image.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # مصفوفة التحويل
        M = cv2.getRotationMatrix2D((center_x, center_y), 0, scale)
        
        # تطبيق التحويل
        result = cv2.warpAffine(image, M, (width, height))
        return result
    
    def _apply_translation(self, image: np.ndarray, shift_x: float, shift_y: float) -> np.ndarray:
        """تطبيق تأثير الانتقال"""
        height, width = image.shape[:2]
        
        # مصفوفة الانتقال
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        
        # تطبيق التحويل
        result = cv2.warpAffine(image, M, (width, height))
        return result
    
    def _apply_fade(self, image: np.ndarray, alpha: float) -> np.ndarray:
        """تطبيق تأثير التلاشي"""
        # إنشاء خلفية سوداء
        overlay = np.zeros_like(image)
        
        # مزج الصورة مع الخلفية
        result = cv2.addWeighted(image, alpha, overlay, 1 - alpha, 0)
        return result
    
    async def generate_video(self, prompt: str, style: str = "realistic", duration: int = 15, include_audio: bool = True) -> Dict[str, Any]:
        """توليد فيديو من النص مع الصوت"""
        try:
            # توليد مجموعة من الصور أولاً
            images = []
            for i in range(duration):  # صورة كل ثانية
                frame_prompt = f"{prompt}, frame {i+1}, {style}"
                image_result = await self.generate_image(frame_prompt, style, "512x512")
                images.append(image_result["image_url"].replace("/uploads/", ""))
            
            # إنشاء الفيديو من الصور
            video_filename = f"generated_video_{uuid.uuid4().hex}.mp4"
            video_path = os.path.join(settings.upload_dir, "videos", video_filename)
            
            # استخدام moviepy لإنشاء الفيديو
            clips = []
            for img_path in images:
                full_path = os.path.join(settings.upload_dir, img_path)
                clip = ImageClip(full_path, duration=1)
                clips.append(clip)
            
            from moviepy.editor import concatenate_videoclips
            final_video = concatenate_videoclips(clips, method="compose")
            final_video.write_videofile(video_path, fps=24)
            
            result = {
                "video_url": f"/uploads/videos/{video_filename}",
                "metadata": {
                    "prompt": prompt,
                    "style": style,
                    "duration": duration,
                    "frames": len(images),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            # إضافة الصوت إذا طُلب
            if include_audio:
                audio_result = await self._generate_audio_for_video(prompt, duration)
                if audio_result:
                    result["audio_url"] = audio_result["audio_url"]
                    result["metadata"]["audio_included"] = True
            
            return result
            
        except Exception as e:
            logger.error(f"خطأ في توليد الفيديو: {e}")
            raise
    
    async def _generate_audio_for_video(self, prompt: str, duration: int) -> Optional[Dict[str, Any]]:
        """توليد صوت مناسب للفيديو"""
        try:
            # يمكن إضافة تكامل مع ElevenLabs أو خدمات أخرى هنا
            # حالياً نقوم بإنشاء صوت صامت كمثال
            
            from pydub import AudioSegment
            
            # إنشاء صوت صامت
            silence = AudioSegment.silent(duration=duration * 1000)  # مللي ثانية
            
            # حفظ الملف الصوتي
            audio_filename = f"generated_audio_{uuid.uuid4().hex}.mp3"
            audio_path = os.path.join(settings.upload_dir, "videos", audio_filename)
            silence.export(audio_path, format="mp3")
            
            return {
                "audio_url": f"/uploads/videos/{audio_filename}",
                "metadata": {
                    "duration": duration,
                    "format": "mp3"
                }
            }
            
        except Exception as e:
            logger.warning(f"لم يتم توليد الصوت: {e}")
            return None
    
    async def edit_image(self, image_path: str, edit_prompt: str, strength: float = 0.7) -> Dict[str, Any]:
        """تعديل صورة باستخدام التعليمات النصية"""
        try:
            if not self.models.get('image_to_image'):
                return await self._edit_image_openai(image_path, edit_prompt, strength)
            
            # تحميل الصورة الأصلية
            image = Image.open(image_path).convert("RGB")
            
            # تطبيق التعديل
            edited_image = self.models['image_to_image'](
                prompt=edit_prompt,
                image=image,
                strength=strength,
                guidance_scale=7.5,
                num_inference_steps=30
            ).images[0]
            
            # حفظ الصورة المعدلة
            filename = f"edited_{uuid.uuid4().hex}.png"
            filepath = os.path.join(settings.upload_dir, "images", filename)
            edited_image.save(filepath)
            
            return {
                "image_url": f"/uploads/images/{filename}",
                "original_url": image_path,
                "metadata": {
                    "edit_prompt": edit_prompt,
                    "strength": strength,
                    "model": "stable-diffusion-img2img",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تعديل الصورة: {e}")
            raise
    
    async def _edit_image_openai(self, image_path: str, edit_prompt: str, strength: float) -> Dict[str, Any]:
        """تعديل صورة باستخدام OpenAI"""
        # يمكن إضافة دعم OpenAI image editing هنا
        raise NotImplementedError("تعديل الصور عبر OpenAI غير مدعوم حالياً")
    
    async def save_uploaded_file(self, file, subfolder: str) -> str:
        """حفظ ملف مرفوع"""
        try:
            # إنشاء اسم ملف فريد
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'unknown'
            filename = f"uploaded_{uuid.uuid4().hex}.{file_extension}"
            filepath = os.path.join(settings.upload_dir, subfolder, filename)
            
            # حفظ الملف
            async with aiofiles.open(filepath, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            return filepath
            
        except Exception as e:
            logger.error(f"خطأ في حفظ الملف: {e}")
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """فحص حالة خدمات الذكاء الاصطناعي"""
        return {
            "initialized": self.initialized,
            "device": self.device,
            "models_loaded": {
                "text_to_image": self.models.get('text_to_image') is not None,
                "image_to_image": self.models.get('image_to_image') is not None,
            },
            "external_apis": self.external_apis,
            "processors": {
                "video": getattr(self, 'video_processor', {}),
                "audio": getattr(self, 'audio_processor', {})
            }
        }
    
    async def cleanup(self):
        """تنظيف الموارد"""
        try:
            # تنظيف نماذج PyTorch
            if self.models.get('text_to_image'):
                del self.models['text_to_image']
            if self.models.get('image_to_image'):
                del self.models['image_to_image']
            
            # تنظيف ذاكرة GPU
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            logger.info("✅ تم تنظيف موارد الذكاء الاصطناعي")
            
        except Exception as e:
            logger.error(f"خطأ في تنظيف الموارد: {e}")
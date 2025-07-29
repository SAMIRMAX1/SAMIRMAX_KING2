# SAMIRMAX AI Studio - استوديو الذكاء الاصطناعي المتقدم

<div align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Python-3.11+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/React-18+-blue.svg" alt="React">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
</div>

**SAMIRMAX AI Studio** هو تطبيق شامل ومتقدم لتوليد الصور والفيديوهات باستخدام أحدث تقنيات الذكاء الاصطناعي. يوفر واجهة عربية حديثة وسهلة الاستخدام مع دعم كامل للميزات المتقدمة.

## ✨ المميزات الرئيسية

### 🎨 توليد المحتوى المرئي
- **توليد الصور من النص**: استخدام Stable Diffusion و OpenAI DALL-E
- **تحويل الصور إلى فيديوهات**: تحريك الصور الثابتة بتأثيرات متنوعة
- **توليد الفيديو من النص**: إنتاج فيديوهات كاملة مع الصوت
- **تعديل الصور التفاعلي**: تعديل الصور باستخدام الأوامر النصية

### 🎞️ تأثيرات الفيديو المتقدمة
- **أنماط الحركة**: خفيف، منظور متوازي، سحري، سينمائي، ديناميكي
- **التحكم بالإطارات الزمنية (Keyframes)**: ضبط دقيق لحركة الكاميرا
- **مؤثرات بصرية جاهزة**: واقعي، فني، أنمي، خيالي، سايبربانك
- **دعم دقة متعددة**: من HD إلى 4K، مع دعم منصات التواصل

### 🎵 توليد ومعالجة الصوت
- **تحويل النص إلى صوت**: أصوات عربية وإنجليزية متنوعة
- **توليد الموسيقى الخلفية**: أنواع مختلفة من الموسيقى
- **تحسين جودة الصوت**: إزالة الضوضاء والتحسين

### 🌐 واجهة مستخدم متقدمة
- **دعم كامل للغة العربية**: من اليمين إلى اليسار
- **تصميم responsive**: يعمل على جميع الأجهزة
- **تأثيرات حركية**: انتقالات سلسة وتفاعلية
- **وضع مظلم**: تجربة مريحة للعين

## 🚀 التشغيل السريع

### استخدام Docker (الطريقة الموصى بها)

```bash
# 1. استنساخ المشروع
git clone https://github.com/your-username/samirmax-ai-studio.git
cd samirmax-ai-studio

# 2. إعداد المتغيرات البيئية
cp .env.example .env
# عدّل ملف .env بمفاتيح API الخاصة بك

# 3. تشغيل التطبيق
./start.sh
```

سيقوم النص بإرشادك خلال اختيار وضع التشغيل والإعداد التلقائي.

### التشغيل اليدوي

```bash
# 1. تشغيل قواعد البيانات
docker-compose up postgres redis -d

# 2. تشغيل الخادم الخلفي
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. تشغيل الواجهة الأمامية
cd frontend
npm install
npm start
```

## 🔑 متطلبات API

للاستفادة الكاملة من التطبيق، ستحتاج إلى:

| الخدمة | المطلوب | الحصول عليه |
|---------|----------|-------------|
| OpenAI | مفتاح API | [platform.openai.com](https://platform.openai.com/api-keys) |
| Hugging Face | رمز Token | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| Google AI | مفتاح API (اختياري) | [console.cloud.google.com](https://console.cloud.google.com/) |

## 📚 واجهات برمجة التطبيقات (APIs)

### توليد الصور
```bash
POST /api/images/generate
{
  "prompt": "منظر طبيعي جميل في الغروب",
  "style": "realistic",
  "size": "1024x1024"
}
```

### تحويل صورة إلى فيديو
```bash
POST /api/videos/image-to-video
Content-Type: multipart/form-data
- image: [ملف الصورة]
- animation_style: "subtle"
- duration: 10
```

### توليد فيديو من النص
```bash
POST /api/videos/generate
{
  "prompt": "رجل يسير في شارع ممطر ليلاً",
  "style": "cinematic",
  "duration": 15,
  "include_audio": true
}
```

## 🏗️ البنية التقنية

```
SAMIRMAX_AI_Studio/
├── 📁 backend/                    # خادم Python FastAPI
│   ├── 📁 app/
│   │   ├── 📁 api/                # نقاط النهاية API
│   │   │   ├── 🐍 image_generation.py
│   │   │   ├── 🐍 video_generation.py
│   │   │   ├── 🐍 audio_generation.py
│   │   │   └── 🐍 file_management.py
│   │   ├── 📁 core/               # إعدادات أساسية
│   │   ├── 📁 services/           # خدمات الذكاء الاصطناعي
│   │   └── 📁 utils/              # أدوات مساعدة
│   ├── 🐳 Dockerfile
│   └── 📄 requirements.txt
├── 📁 frontend/                   # واجهة React TypeScript
│   ├── 📁 src/
│   │   ├── 📁 components/         # مكونات الواجهة
│   │   ├── 📁 pages/              # صفحات التطبيق
│   │   ├── 📁 services/           # خدمات API
│   │   └── 📁 utils/              # أدوات مساعدة
│   ├── 🐳 Dockerfile
│   ├── 📄 package.json
│   └── ⚙️ tailwind.config.js
├── 🐳 docker-compose.yml          # إعداد Docker الشامل
├── 🚀 start.sh                    # ملف التشغيل السريع
├── ⚙️ .env.example                # إعدادات المثال
└── 📖 README.md
```

## 🔧 إعدادات متقدمة

### توليد محلي (بدون إنترنت)
```bash
# تمكين الوضع المحلي في ملف .env
LOCAL_GENERATION=true
STABLE_DIFFUSION_MODEL=runwayml/stable-diffusion-v1-5
```

### تحسين الأداء
```bash
# للأجهزة التي تدعم GPU
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="6.0;6.1;7.0;7.5;8.0"

# للمعالجة المتوازية
CELERY_WORKERS=4
MAX_CONCURRENT_GENERATIONS=2
```

### مراقبة الأداء
```bash
# تشغيل خدمات المراقبة
docker-compose --profile monitoring up -d

# الوصول إلى لوحة Flower
http://localhost:5555
```

## 🛠️ التطوير والمساهمة

### إعداد بيئة التطوير
```bash
# إعداد pre-commit hooks
pip install pre-commit
pre-commit install

# تشغيل الاختبارات
cd backend
pytest

cd frontend
npm test
```

### بنية الكود
- **Backend**: FastAPI + SQLAlchemy + Redis
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **AI Models**: Diffusers + Transformers + OpenAI
- **Database**: PostgreSQL + Redis
- **Infrastructure**: Docker + Nginx

## 📊 أمثلة الاستخدام

### مثال 1: توليد صور احترافية
```python
# مثال برمجي
import requests

response = requests.post('http://localhost:8000/api/images/generate', json={
    "prompt": "شعار شركة تقنية حديثة، تصميم أنيق، ألوان زرقاء وفضية",
    "style": "professional",
    "size": "1024x1024"
})

result = response.json()
print(f"الصورة متاحة على: {result['data']['image_url']}")
```

### مثال 2: إنشاء فيديو تسويقي
```python
# مثال إنشاء فيديو من نص
script = """
مرحباً بكم في منتجنا الجديد
حلول تقنية متطورة
اكتشف المستقبل معنا
"""

response = requests.post('http://localhost:8000/api/videos/script-to-video', data={
    "script": script,
    "visual_style": "professional",
    "voice_style": "confident",
    "background_music": True
})
```

## 🔒 الأمان والخصوصية

- **تشفير البيانات**: جميع البيانات الحساسة مشفرة
- **مصادقة آمنة**: JWT tokens مع انتهاء صلاحية
- **إدارة الملفات**: تحكم صارم في أنواع وأحجام الملفات
- **معالجة محلية**: إمكانية التشغيل بدون إرسال بيانات للخارج

## 📈 الأداء والتحسين

- **تخزين مؤقت ذكي**: Redis للنتائج المتكررة
- **معالجة غير متزامنة**: Celery للمهام الثقيلة
- **ضغط الملفات**: تحسين أحجام الصور والفيديوهات
- **CDN جاهز**: دعم توزيع المحتوى عالمياً

## 🌍 الدعم والمجتمع

- **الوثائق**: وثائق شاملة متاحة على `/docs`
- **الأمثلة**: مكتبة غنية من الأمثلة والقوالب
- **التحديثات**: تحديثات منتظمة وميزات جديدة
- **الدعم**: مجتمع نشط ودعم فني

## 📋 قائمة المهام المستقبلية

- [ ] دمج مع المزيد من نماذج الذكاء الاصطناعي
- [ ] دعم تحرير الفيديو المتقدم
- [ ] تطبيق موبايل (React Native)
- [ ] واجهة برمجة تطبيقات موسعة
- [ ] دعم العديد من اللغات
- [ ] تكامل مع خدمات التخزين السحابي

## 📄 الرخصة

MIT License - مشروع مفتوح المصدر. راجع ملف `LICENSE` للتفاصيل.

## 🤝 المساهمة

نرحب بالمساهمات! يرجى قراءة `CONTRIBUTING.md` للحصول على التفاصيل.

## 📞 التواصل

- **المطور**: SAMIRMAX
- **البريد الإلكتروني**: contact@samirmax.dev
- **الموقع**: https://samirmax.dev
- **Twitter**: [@samirmax_dev](https://twitter.com/samirmax_dev)

---

<div align="center">
  <p>صُنع بـ ❤️ في العالم العربي</p>
  <p>© 2024 SAMIRMAX AI Studio. جميع الحقوق محفوظة.</p>
</div>
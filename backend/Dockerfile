# استخدام Python 3.11 slim كصورة أساسية
FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# تثبيت المتطلبات النظام
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مستخدم غير root
RUN useradd --create-home --shell /bin/bash samirmax
USER samirmax

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY --chown=samirmax:samirmax requirements.txt .

# تثبيت المتطلبات Python
RUN pip install --user --no-warn-script-location -r requirements.txt

# إضافة pip local bin إلى PATH
ENV PATH=/home/samirmax/.local/bin:$PATH

# نسخ كود التطبيق
COPY --chown=samirmax:samirmax . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p uploads/images uploads/videos uploads/temp logs

# تعيين المتغيرات البيئية للتطبيق
ENV PYTHONPATH=/app

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# كشف المنفذ
EXPOSE 8000

# الأمر الافتراضي لتشغيل التطبيق
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
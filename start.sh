#!/bin/bash

# ===================================
# ملف تشغيل SAMIRMAX AI Studio
# ===================================

echo "🚀 مرحباً بك في SAMIRMAX AI Studio"
echo "======================================"

# التحقق من وجود Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker غير مثبت. يرجى تثبيت Docker أولاً"
    echo "📥 تحميل من: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose غير مثبت. يرجى تثبيت Docker Compose أولاً"
    echo "📥 تحميل من: https://docs.docker.com/compose/install/"
    exit 1
fi

# التحقق من وجود ملف .env
if [ ! -f .env ]; then
    echo "⚙️  إنشاء ملف الإعدادات..."
    cp .env.example .env
    echo "✅ تم إنشاء ملف .env من المثال"
    echo "📝 يرجى تعديل ملف .env بمفاتيح API الخاصة بك"
    echo ""
    echo "🔑 ستحتاج إلى:"
    echo "   • مفتاح OpenAI: https://platform.openai.com/api-keys"
    echo "   • رمز Hugging Face: https://huggingface.co/settings/tokens"
    echo "   • مفتاح Google (اختياري): https://console.cloud.google.com/"
    echo ""
    read -p "هل تريد المتابعة بالإعدادات الافتراضية؟ (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "يرجى تعديل ملف .env ثم تشغيل الملف مرة أخرى"
        exit 1
    fi
fi

# إنشاء المجلدات المطلوبة
echo "📁 إنشاء المجلدات المطلوبة..."
mkdir -p logs uploads/images uploads/videos uploads/temp

# اختيار وضع التشغيل
echo ""
echo "اختر وضع التشغيل:"
echo "1. التطوير (Development) - مع إعادة التحميل التلقائي"
echo "2. الإنتاج (Production) - مع جميع الخدمات"
echo "3. فقط قواعد البيانات (Database Only)"
echo "4. التنظيف والإعادة البناء (Clean & Rebuild)"

read -p "اختر الرقم (1-4): " choice

case $choice in
    1)
        echo "🔧 تشغيل وضع التطوير..."
        docker-compose up --build postgres redis backend frontend
        ;;
    2)
        echo "🏭 تشغيل وضع الإنتاج..."
        docker-compose --profile production up --build -d
        ;;
    3)
        echo "💾 تشغيل قواعد البيانات فقط..."
        docker-compose up postgres redis
        ;;
    4)
        echo "🧹 تنظيف وإعادة البناء..."
        docker-compose down -v
        docker system prune -f
        docker-compose build --no-cache
        docker-compose up --build postgres redis backend frontend
        ;;
    *)
        echo "❌ خيار غير صحيح"
        exit 1
        ;;
esac

echo ""
echo "✅ تم تشغيل SAMIRMAX AI Studio بنجاح!"
echo ""
echo "🌐 الروابط المتاحة:"
echo "   • الواجهة الأمامية: http://localhost:3000"
echo "   • API الخلفي: http://localhost:8000"
echo "   • وثائق API: http://localhost:8000/docs"
echo "   • قاعدة البيانات: postgresql://localhost:5432/samirmax_ai"
echo "   • Redis: redis://localhost:6379"

if [[ $choice == 2 ]]; then
    echo "   • مراقبة Celery: http://localhost:5555"
fi

echo ""
echo "📚 للمساعدة:"
echo "   • اقرأ ملف README.md"
echo "   • زر الوثائق على http://localhost:8000/docs"
echo "   • تحقق من ملف docker-compose.yml للتفاصيل"
echo ""
echo "⏹️  لإيقاف التطبيق:"
echo "   docker-compose down"
echo ""
echo "🎉 استمتع بتطوير تطبيقات الذكاء الاصطناعي!"
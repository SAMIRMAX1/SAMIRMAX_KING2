#!/bin/bash

# تجربة أداة إنشاء هياكل التطبيقات
# Demo script for Application Structure Generator

echo "🚀 مرحباً بك في أداة إنشاء هياكل التطبيقات"
echo "Welcome to Application Structure Generator"
echo "========================================"
echo

# عرض القوالب المتاحة
echo "📋 القوالب المتاحة:"
python3 app_generator.py list
echo

# إنشاء مشاريع تجريبية
echo "🔨 إنشاء مشاريع تجريبية..."
echo "Creating demo projects..."
echo

echo "1️⃣ إنشاء تطبيق ويب..."
python3 app_generator.py create demo-web-app web
echo

echo "2️⃣ إنشاء API..."
python3 app_generator.py create demo-api api
echo

echo "3️⃣ إنشاء أداة سطر الأوامر..."
python3 app_generator.py create demo-cli-tool cli
echo

# عرض ما تم إنشاؤه
echo "📁 المشاريع التي تم إنشاؤها:"
echo "Created projects:"
ls -la demo-*/
echo

echo "✅ تمت التجربة بنجاح!"
echo "Demo completed successfully!"
echo
echo "💡 نصيحة: اقرأ ملف README.md في كل مشروع للحصول على تعليمات التشغيل"
echo "Tip: Read the README.md file in each project for running instructions"
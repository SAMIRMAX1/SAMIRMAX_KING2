# مرحلة البناء
FROM node:18-alpine AS builder

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات package
COPY package*.json ./

# تثبيت التبعيات
RUN npm ci --only=production

# نسخ كود المصدر
COPY . .

# بناء التطبيق للإنتاج
RUN npm run build

# مرحلة التشغيل
FROM nginx:alpine

# نسخ ملف إعداد nginx مخصص
COPY nginx.conf /etc/nginx/conf.d/default.conf

# نسخ ملفات البناء من المرحلة السابقة
COPY --from=builder /app/build /usr/share/nginx/html

# إنشاء ملف index.html احتياطي للتوجيه
RUN echo '<!DOCTYPE html><html><head><meta charset="utf-8"><title>SAMIRMAX AI Studio</title></head><body><div id="root">جاري تحميل التطبيق...</div></body></html>' > /usr/share/nginx/html/index.html.backup

# كشف المنفذ
EXPOSE 80

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80 || exit 1

# بدء nginx
CMD ["nginx", "-g", "daemon off;"]
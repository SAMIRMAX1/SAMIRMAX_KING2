# أداة إنشاء هياكل التطبيقات 🚀
## Application Structure Generator

أداة شاملة لإنشاء هياكل أساسية لأنواع مختلفة من التطبيقات والمشاريع البرمجية.

A comprehensive tool for creating basic structures for different types of applications and software projects.

## 🌟 الميزات | Features

- **8 أنواع مختلفة من القوالب** - 8 different project templates
- **دعم كامل للغة العربية** - Full Arabic language support
- **توليد كود جاهز للاستخدام** - Ready-to-use code generation
- **أفضل الممارسات البرمجية** - Best programming practices
- **ملفات التوثيق والإعداد** - Documentation and configuration files

## 📋 أنواع القوالب المتاحة | Available Templates

| النوع | الوصف | التقنيات |
|-------|--------|-----------|
| `web` | تطبيق ويب حديث | React, HTML5, CSS3 |
| `api` | خدمة API | Node.js, Express |
| `desktop` | تطبيق سطح المكتب | Python, Tkinter |
| `mobile` | تطبيق جوال | React Native |
| `cli` | أداة سطر الأوامر | Python, Click, Rich |
| `library` | مكتبة Python | Python, pytest |
| `microservice` | خدمة مصغرة | FastAPI, Docker, Kubernetes |
| `fullstack` | تطبيق شامل | React + Node.js + MongoDB |

## 🚀 كيفية الاستخدام | How to Use

### تثبيت المتطلبات | Install Requirements

```bash
# تأكد من وجود Python 3.7+
python3 --version

# جعل الملف قابل للتنفيذ
chmod +x app_generator.py
```

### عرض القوالب المتاحة | List Available Templates

```bash
python3 app_generator.py list
```

### إنشاء مشروع جديد | Create New Project

```bash
python3 app_generator.py create <اسم_المشروع> <نوع_القالب>
```

### أمثلة | Examples

```bash
# إنشاء تطبيق ويب
python3 app_generator.py create my-website web

# إنشاء API
python3 app_generator.py create my-api api

# إنشاء أداة سطر الأوامر
python3 app_generator.py create my-tool cli

# إنشاء تطبيق شامل
python3 app_generator.py create my-fullstack-app fullstack

# إنشاء في مجلد محدد
python3 app_generator.py create my-project web -o /path/to/output
```

## 📁 هيكل المشاريع المُنشأة | Generated Project Structure

### تطبيق ويب (Web)
```
my-website/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   ├── utils/
│   ├── App.js
│   ├── App.css
│   └── index.js
├── package.json
└── README.md
```

### API
```
my-api/
├── src/
│   ├── routes/
│   ├── models/
│   ├── controllers/
│   ├── middleware/
│   ├── utils/
│   └── server.js
├── tests/
├── package.json
├── .env.example
└── README.md
```

### أداة سطر الأوامر (CLI)
```
my-tool/
├── src/
│   ├── commands/
│   └── utils/
├── tests/
├── main.py
├── setup.py
├── requirements.txt
└── README.md
```

## 🛠 تشغيل المشاريع | Running Projects

### تطبيق ويب | Web App
```bash
cd my-website
npm install
npm start
```

### API
```bash
cd my-api
npm install
npm run dev
```

### أداة سطر الأوامر | CLI Tool
```bash
cd my-tool
pip install -r requirements.txt
python main.py --help
```

### خدمة مصغرة | Microservice
```bash
cd my-microservice
pip install -r requirements.txt
python main.py
# أو استخدم Docker
docker-compose up
```

## 📖 المساعدة | Help

```bash
# عرض المساعدة العامة
python3 app_generator.py --help

# عرض مساعدة أمر الإنشاء
python3 app_generator.py create --help
```

## 🌍 اللغات المدعومة | Supported Languages

- **العربية** - Arabic (primary)
- **English** - English (secondary)

جميع الملفات المُنشأة تحتوي على تعليقات وتوثيق باللغتين العربية والإنجليزية.

All generated files contain comments and documentation in both Arabic and English.

## 🔧 التخصيص | Customization

يمكنك تخصيص القوالب بتعديل الدوال في `app_generator.py`:

You can customize templates by modifying the functions in `app_generator.py`:

- `_web_template()` - لتطبيقات الويب
- `_api_template()` - لخدمات API  
- `_cli_template()` - لأدوات سطر الأوامر
- وغيرها...

## 🤝 المساهمة | Contributing

1. Fork المشروع
2. أنشئ branch جديد للميزة
3. أضف التغييرات
4. أرسل Pull Request

## 📄 الترخيص | License

MIT License - حر للاستخدام والتعديل

## 👨‍💻 المطور | Developer

تم تطوير هذه الأداة لمساعدة المطورين العرب في إنشاء مشاريع احترافية بسرعة وسهولة.

This tool was developed to help Arab developers create professional projects quickly and easily.

---

**نصائح مهمة | Important Tips:**

- ⚡ استخدم القوالب كنقطة بداية وطور عليها
- 📚 اقرأ ملف README لكل مشروع مُنشأ
- 🔄 حدث المتطلبات حسب احتياجاتك
- 🎨 خصص التصميم والألوان
- 🔒 لا تنس إعداد الأمان للمشاريع الإنتاجية

**استمتع بالبرمجة! 🎉**
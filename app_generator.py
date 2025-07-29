#!/usr/bin/env python3
"""
أداة إنشاء هياكل التطبيقات الأساسية
Application Structure Generator Tool

هذه الأداة تقوم بإنشاء هياكل أساسية لأنواع مختلفة من التطبيقات
This tool creates basic structures for different types of applications
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

class AppGenerator:
    def __init__(self):
        self.templates = {
            'web': self._web_template,
            'api': self._api_template,
            'desktop': self._desktop_template,
            'mobile': self._mobile_template,
            'cli': self._cli_template,
            'library': self._library_template,
            'microservice': self._microservice_template,
            'fullstack': self._fullstack_template
        }
    
    def create_project(self, project_name: str, project_type: str, output_dir: str = "."):
        """إنشاء مشروع جديد - Create a new project"""
        if project_type not in self.templates:
            print(f"❌ نوع المشروع غير مدعوم: {project_type}")
            print(f"الأنواع المدعومة: {', '.join(self.templates.keys())}")
            return False
        
        project_path = Path(output_dir) / project_name
        
        if project_path.exists():
            print(f"❌ المجلد موجود بالفعل: {project_path}")
            return False
        
        print(f"🚀 إنشاء مشروع {project_type}: {project_name}")
        
        # إنشاء المجلد الأساسي
        project_path.mkdir(parents=True, exist_ok=True)
        
        # تطبيق القالب
        template_func = self.templates[project_type]
        template_func(project_path, project_name)
        
        print(f"✅ تم إنشاء المشروع بنجاح في: {project_path}")
        return True
    
    def _create_file(self, file_path: Path, content: str):
        """إنشاء ملف مع المحتوى المحدد"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _web_template(self, project_path: Path, project_name: str):
        """قالب تطبيق ويب - Web application template"""
        
        # إنشاء هيكل المجلدات
        folders = [
            'src/components',
            'src/pages',
            'src/styles',
            'src/utils',
            'public/images',
            'public/icons'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # package.json
        package_json = {
            "name": project_name,
            "version": "1.0.0",
            "description": f"تطبيق ويب {project_name}",
            "main": "src/index.js",
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1"
            },
            "browserslist": {
                "production": [
                    ">0.2%",
                    "not dead",
                    "not op_mini all"
                ],
                "development": [
                    "last 1 chrome version",
                    "last 1 firefox version",
                    "last 1 safari version"
                ]
            }
        }
        
        self._create_file(project_path / 'package.json', json.dumps(package_json, indent=2, ensure_ascii=False))
        
        # HTML الأساسي
        html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="تطبيق {project_name}" />
    <title>{project_name}</title>
</head>
<body>
    <noscript>تحتاج إلى تفعيل JavaScript لتشغيل هذا التطبيق.</noscript>
    <div id="root"></div>
</body>
</html>"""
        
        self._create_file(project_path / 'public/index.html', html_content)
        
        # مكون React الأساسي
        app_component = f"""import React from 'react';
import './App.css';

function App() {{
  return (
    <div className="App">
      <header className="App-header">
        <h1>مرحباً بك في {project_name}</h1>
        <p>
          تطبيق ويب حديث باستخدام React
        </p>
      </header>
    </div>
  );
}}

export default App;"""
        
        self._create_file(project_path / 'src/App.js', app_component)
        
        # CSS أساسي
        css_content = """.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}"""
        
        self._create_file(project_path / 'src/App.css', css_content)
        
        # index.js
        index_js = f"""import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);"""
        
        self._create_file(project_path / 'src/index.js', index_js)
        
        # index.css
        self._create_file(project_path / 'src/index.css', css_content)
        
        # README
        readme_content = f"""# {project_name}

تطبيق ويب حديث باستخدام React

## التشغيل

```bash
npm install
npm start
```

## البناء

```bash
npm run build
```

## الميزات

- واجهة مستخدم حديثة
- دعم اللغة العربية
- تصميم متجاوب

## المتطلبات

- Node.js 14+
- npm أو yarn
"""
        
        self._create_file(project_path / 'README.md', readme_content)
    
    def _api_template(self, project_path: Path, project_name: str):
        """قالب API - API template"""
        
        folders = [
            'src/routes',
            'src/models',
            'src/controllers',
            'src/middleware',
            'src/utils',
            'tests'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # package.json لـ Node.js API
        package_json = {
            "name": project_name,
            "version": "1.0.0",
            "description": f"API خدمة {project_name}",
            "main": "src/server.js",
            "scripts": {
                "start": "node src/server.js",
                "dev": "nodemon src/server.js",
                "test": "jest"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "helmet": "^7.0.0",
                "morgan": "^1.10.0",
                "dotenv": "^16.3.1"
            },
            "devDependencies": {
                "nodemon": "^3.0.1",
                "jest": "^29.6.1"
            }
        }
        
        self._create_file(project_path / 'package.json', json.dumps(package_json, indent=2, ensure_ascii=False))
        
        # الخادم الأساسي
        server_js = f"""const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({{ extended: true }}));

// Routes
app.get('/', (req, res) => {{
  res.json({{
    message: 'مرحباً بك في {project_name} API',
    version: '1.0.0',
    status: 'running'
  }});
}});

app.get('/api/health', (req, res) => {{
  res.json({{
    status: 'healthy',
    timestamp: new Date().toISOString()
  }});
}});

// Error handling
app.use((req, res) => {{
  res.status(404).json({{
    error: 'الطريق غير موجود',
    path: req.path
  }});
}});

app.use((err, req, res, next) => {{
  console.error(err.stack);
  res.status(500).json({{
    error: 'خطأ داخلي في الخادم'
  }});
}});

app.listen(PORT, () => {{
  console.log(`🚀 الخادم يعمل على البورت ${{PORT}}`);
}});

module.exports = app;"""
        
        self._create_file(project_path / 'src/server.js', server_js)
        
        # ملف البيئة
        env_content = f"""# {project_name} Environment Variables
PORT=3000
NODE_ENV=development

# Database (إضافة تفاصيل قاعدة البيانات حسب الحاجة)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME={project_name}
# DB_USER=user
# DB_PASSWORD=password

# JWT Secret (في حالة استخدام JWT)
# JWT_SECRET=your_jwt_secret_here
"""
        
        self._create_file(project_path / '.env.example', env_content)
        
        # README
        readme_content = f"""# {project_name} API

API خدمة {project_name}

## التشغيل

```bash
npm install
npm run dev
```

## الإنتاج

```bash
npm start
```

## النقاط الأساسية

- `GET /` - الصفحة الرئيسية
- `GET /api/health` - فحص حالة الخادم

## المتطلبات

- Node.js 16+
- npm أو yarn

## المتغيرات البيئية

انسخ `.env.example` إلى `.env` وحدث القيم حسب الحاجة.
"""
        
        self._create_file(project_path / 'README.md', readme_content)
    
    def _cli_template(self, project_path: Path, project_name: str):
        """قالب تطبيق سطر الأوامر - CLI application template"""
        
        folders = [
            'src/commands',
            'src/utils',
            'tests'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # Python CLI
        requirements_txt = """click>=8.0.0
colorama>=0.4.4
rich>=13.0.0"""
        
        self._create_file(project_path / 'requirements.txt', requirements_txt)
        
        # الملف الرئيسي
        main_py = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''{project_name} - أداة سطر الأوامر
CLI Tool for {project_name}
'''

import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    '''{project_name} - أداة سطر الأوامر قوية ومرنة'''
    pass

@cli.command()
@click.option('--name', prompt='اسمك', help='اسم المستخدم')
def hello(name):
    # تحية المستخدم
    console.print(f"[bold green]مرحباً {{name}}! 👋[/bold green]")

@cli.command()
def status():
    # عرض حالة التطبيق
    table = Table(title="حالة {project_name}")
    
    table.add_column("المكون", style="cyan")
    table.add_column("الحالة", style="magenta")
    
    table.add_row("التطبيق", "✅ يعمل")
    table.add_row("الإصدار", "1.0.0")
    
    console.print(table)

@cli.command()
@click.argument('text')
def echo(text):
    # إعادة طباعة النص
    console.print(f"[bold blue]{{text}}[/bold blue]")

if __name__ == '__main__':
    cli()"""
        
        self._create_file(project_path / 'main.py', main_py)
        
        # setup.py
        setup_py = f"""from setuptools import setup, find_packages

setup(
    name='{project_name}',
    version='1.0.0',
    description='أداة سطر الأوامر {project_name}',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'colorama>=0.4.4',
        'rich>=13.0.0'
    ],
    entry_points={{
        'console_scripts': [
            '{project_name}=main:cli',
        ],
    }},
    python_requires='>=3.7',
)"""
        
        self._create_file(project_path / 'setup.py', setup_py)
        
        # README
        readme_content = f"""# {project_name}

أداة سطر الأوامر {project_name}

## التثبيت

```bash
pip install -r requirements.txt
pip install -e .
```

## الاستخدام

```bash
# عرض المساعدة
python main.py --help

# تحية
python main.py hello

# عرض الحالة
python main.py status

# إعادة طباعة نص
python main.py echo "مرحبا بالعالم"
```

## الميزات

- واجهة سطر أوامر سهلة الاستخدام
- ألوان وتنسيق جميل
- دعم اللغة العربية

## المتطلبات

- Python 3.7+
"""
        
        self._create_file(project_path / 'README.md', readme_content)

    def _desktop_template(self, project_path: Path, project_name: str):
        """قالب تطبيق سطح المكتب - Desktop application template"""
        
        folders = [
            'src/ui',
            'src/core',
            'assets/icons',
            'assets/images'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # Python + Tkinter
        requirements_txt = """tkinter
Pillow>=9.0.0
configparser>=5.0.0"""
        
        self._create_file(project_path / 'requirements.txt', requirements_txt)
        
        # التطبيق الرئيسي
        main_py = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''{project_name} - تطبيق سطح المكتب
Desktop Application for {project_name}
'''

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys

class {project_name.replace('-', '').replace('_', '').title()}App:
    def __init__(self, root):
        self.root = root
        self.root.title("{project_name}")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # إعداد القوائم
        self.create_menus()
        
        # إعداد الواجهة الرئيسية
        self.create_main_interface()
        
        # شريط الحالة
        self.create_status_bar()
    
    def create_menus(self):
        # إنشاء شريط القوائم
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # قائمة الملف
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="جديد", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="فتح", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="حفظ", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.quit_app)
        
        # قائمة المساعدة
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="مساعدة", menu=help_menu)
        help_menu.add_command(label="حول", command=self.show_about)
    
    def create_main_interface(self):
        # إنشاء الواجهة الرئيسية
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # تكوين الشبكة
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # العنوان
        title_label = ttk.Label(main_frame, text="مرحباً بك في {project_name}", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # منطقة النص
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_area = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # الأزرار
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="مسح", command=self.clear_text).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="حفظ", command=self.save_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="فتح", command=self.open_file).pack(side=tk.LEFT)
    
    def create_status_bar(self):
        # إنشاء شريط الحالة
        self.status_var = tk.StringVar()
        self.status_var.set("جاهز")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def new_file(self):
        # إنشاء ملف جديد
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("ملف جديد")
    
    def open_file(self):
        # فتح ملف
        file_path = filedialog.askopenfilename(
            title="فتح ملف",
            filetypes=[("ملفات النص", "*.txt"), ("جميع الملفات", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                self.status_var.set(f"تم فتح: {{os.path.basename(file_path)}}")
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن فتح الملف: {{e}}")
    
    def save_file(self):
        # حفظ الملف
        file_path = filedialog.asksaveasfilename(
            title="حفظ الملف",
            defaultextension=".txt",
            filetypes=[("ملفات النص", "*.txt"), ("جميع الملفات", "*.*")]
        )
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.status_var.set(f"تم حفظ: {{os.path.basename(file_path)}}")
            except Exception as e:
                messagebox.showerror("خطأ", f"لا يمكن حفظ الملف: {{e}}")
    
    def clear_text(self):
        # مسح النص
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("تم مسح النص")
    
    def show_about(self):
        # عرض معلومات التطبيق
        messagebox.showinfo("حول", f"{project_name}\\nالإصدار 1.0.0\\nتطبيق سطح مكتب حديث")
    
    def quit_app(self):
        # إنهاء التطبيق
        if messagebox.askokcancel("خروج", "هل أنت متأكد من إنهاء التطبيق؟"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = {project_name.replace('-', '').replace('_', '').title()}App(root)
    
    # ربط اختصارات لوحة المفاتيح
    root.bind('<Control-n>', lambda e: app.new_file())
    root.bind('<Control-o>', lambda e: app.open_file())
    root.bind('<Control-s>', lambda e: app.save_file())
    
    root.mainloop()

if __name__ == "__main__":
    main()"""
        
        self._create_file(project_path / 'main.py', main_py)
        
        # README
        readme_content = f"""# {project_name}

تطبيق سطح المكتب {project_name}

## التشغيل

```bash
pip install -r requirements.txt
python main.py
```

## الميزات

- واجهة مستخدم بسيطة وجميلة
- دعم اللغة العربية
- إدارة الملفات
- اختصارات لوحة المفاتيح

## اختصارات لوحة المفاتيح

- `Ctrl+N` - ملف جديد
- `Ctrl+O` - فتح ملف
- `Ctrl+S` - حفظ ملف

## المتطلبات

- Python 3.7+
- tkinter (مثبت مع Python عادة)
"""
        
        self._create_file(project_path / 'README.md', readme_content)

    def _mobile_template(self, project_path: Path, project_name: str):
        """قالب تطبيق الجوال - Mobile application template"""
        
        folders = [
            'src/screens',
            'src/components',
            'src/navigation',
            'src/services',
            'src/utils',
            'assets/images',
            'assets/fonts'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # React Native
        package_json = {
            "name": project_name,
            "version": "1.0.0",
            "description": f"تطبيق جوال {project_name}",
            "main": "index.js",
            "scripts": {
                "android": "react-native run-android",
                "ios": "react-native run-ios",
                "start": "react-native start",
                "test": "jest",
                "lint": "eslint ."
            },
            "dependencies": {
                "react": "18.2.0",
                "react-native": "0.72.4",
                "@react-navigation/native": "^6.1.7",
                "@react-navigation/stack": "^6.3.17"
            },
            "devDependencies": {
                "@babel/core": "^7.20.0",
                "@babel/preset-env": "^7.20.0",
                "@babel/runtime": "^7.20.0",
                "babel-jest": "^29.2.1",
                "eslint": "^8.19.0",
                "jest": "^29.2.1",
                "metro-react-native-babel-preset": "0.76.7"
            },
            "jest": {
                "preset": "react-native"
            }
        }
        
        self._create_file(project_path / 'package.json', json.dumps(package_json, indent=2, ensure_ascii=False))
        
        # App.js الرئيسي
        app_js = f"""import React from 'react';
import {{
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Alert,
}} from 'react-native';

const App = () => {{
  const showWelcome = () => {{
    Alert.alert(
      'مرحباً',
      'مرحباً بك في تطبيق {project_name}!',
      [{{text: 'حسناً', style: 'default'}}]
    );
  }};

  return (
    <SafeAreaView style={{flex: 1}}>
      <StatusBar
        barStyle="dark-content"
        backgroundColor="#f8f9fa"
      />
      <ScrollView
        contentInsetAdjustmentBehavior="automatic"
        style={styles.scrollView}>
        <View style={styles.container}>
          <Text style={styles.title}>{project_name}</Text>
          <Text style={styles.subtitle}>تطبيق جوال حديث</Text>
          
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={styles.button}
              onPress={{showWelcome}}>
              <Text style={styles.buttonText}>مرحباً</Text>
            </TouchableOpacity>
          </View>
          
          <View style={styles.infoContainer}>
            <Text style={styles.infoTitle}>الميزات:</Text>
            <Text style={styles.infoText}>• واجهة مستخدم جميلة</Text>
            <Text style={styles.infoText}>• دعم اللغة العربية</Text>
            <Text style={styles.infoText}>• تصميم متجاوب</Text>
            <Text style={styles.infoText}>• أداء عالي</Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}};

const styles = StyleSheet.create({{
  scrollView: {{
    backgroundColor: '#f8f9fa',
  }},
  container: {{
    flex: 1,
    alignItems: 'center',
    padding: 20,
    minHeight: '100%',
  }},
  title: {{
    fontSize: 32,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 50,
    marginBottom: 10,
    textAlign: 'center',
  }},
  subtitle: {{
    fontSize: 18,
    color: '#666',
    marginBottom: 40,
    textAlign: 'center',
  }},
  buttonContainer: {{
    marginVertical: 30,
  }},
  button: {{
    backgroundColor: '#007bff',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {{
      width: 0,
      height: 2,
    }},
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  }},
  buttonText: {{
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  }},
  infoContainer: {{
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    marginTop: 30,
    width: '100%',
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: {{
      width: 0,
      height: 1,
    }},
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
  }},
  infoTitle: {{
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
    textAlign: 'right',
  }},
  infoText: {{
    fontSize: 16,
    color: '#555',
    marginBottom: 8,
    textAlign: 'right',
  }},
}});

export default App;"""
        
        self._create_file(project_path / 'App.js', app_js)
        
        # index.js
        index_js = f"""import {{AppRegistry}} from 'react-native';
import App from './App';
import {{name as appName}} from './app.json';

AppRegistry.registerComponent(appName, () => App);"""
        
        self._create_file(project_path / 'index.js', index_js)
        
        # app.json
        app_json = {
            "name": project_name,
            "displayName": project_name
        }
        
        self._create_file(project_path / 'app.json', json.dumps(app_json, indent=2, ensure_ascii=False))
        
        # README
        readme_content = f"""# {project_name}

تطبيق جوال {project_name} باستخدام React Native

## التشغيل

### الإعداد
```bash
npm install
cd ios && pod install && cd .. # للـ iOS فقط
```

### تشغيل Android
```bash
npm run android
```

### تشغيل iOS
```bash
npm run ios
```

## الميزات

- واجهة مستخدم حديثة
- دعم اللغة العربية
- تصميم متجاوب
- أداء عالي

## المتطلبات

- Node.js 16+
- React Native CLI
- Android Studio (للـ Android)
- Xcode (للـ iOS)

## البناء

```bash
# Android
cd android && ./gradlew assembleRelease

# iOS
cd ios && xcodebuild -configuration Release
```
"""
        
        self._create_file(project_path / 'README.md', readme_content)

    def _library_template(self, project_path: Path, project_name: str):
        """قالب مكتبة - Library template"""
        
        folders = [
            'src',
            'tests',
            'docs',
            'examples'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # setup.py للمكتبة
        setup_py = f"""from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{project_name}",
    version="1.0.0",
    author="اسمك",
    author_email="email@example.com",
    description="مكتبة {project_name}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/username/{project_name}",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        # إضافة المتطلبات هنا
    ],
    extras_require={{
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    }},
)"""
        
        self._create_file(project_path / 'setup.py', setup_py)
        
        # الملف الرئيسي للمكتبة
        init_py = f'''# -*- coding: utf-8 -*-
\'\'\'{project_name} - مكتبة Python مفيدة
{project_name} - A useful Python library

هذه مكتبة توفر وظائف مفيدة للمطورين
This library provides useful functions for developers
\'\'\'

__version__ = "1.0.0"
__author__ = "اسمك"
__email__ = "email@example.com"

from .core import {project_name.replace('-', '_').replace(' ', '_').title()}

__all__ = ["{project_name.replace('-', '_').replace(' ', '_').title()}"]'''
        
        self._create_file(project_path / f'src/{project_name.replace("-", "_")}/__init__.py', init_py)
        
        # الملف الأساسي
        core_py = f'''# -*- coding: utf-8 -*-
\'\'\'الوحدة الأساسية لمكتبة {project_name}
Core module for {project_name} library
\'\'\'

class {project_name.replace('-', '_').replace(' ', '_').title()}:
    # الفئة الرئيسية لمكتبة {project_name}
    # Main class for {project_name} library
    
    def __init__(self, name: str = "مستخدم"):
        # إنشاء كائن جديد - Initialize a new instance
        # Args: name (str): اسم المستخدم / User name
        self.name = name
    
    def greet(self) -> str:
        # إرجاع تحية - Return a greeting
        # Returns: str: رسالة ترحيب / Welcome message
        return f"مرحباً {{self.name}}! أهلاً بك في {project_name}"
    
    def calculate(self, x: float, y: float) -> float:
        # دالة حسابية بسيطة - Simple calculation function
        # Args: x (float): العدد الأول / First number
        #       y (float): العدد الثاني / Second number
        # Returns: float: النتيجة / Result
        return x + y
    
    def process_data(self, data: list) -> dict:
        # معالجة البيانات - Process data
        # Args: data (list): قائمة البيانات / Data list
        # Returns: dict: النتائج المعالجة / Processed results
        return {{
            "count": len(data),
            "sum": sum(data) if all(isinstance(x, (int, float)) for x in data) else 0,
            "first": data[0] if data else None,
            "last": data[-1] if data else None
        }}


def helper_function(text: str) -> str:
    # دالة مساعدة - Helper function
    # Args: text (str): النص المدخل / Input text
    # Returns: str: النص المعالج / Processed text
    return text.strip().title()'''
        
        self._create_file(project_path / f'src/{project_name.replace("-", "_")}/core.py', core_py)
        
        # اختبارات
        test_py = f'''# -*- coding: utf-8 -*-
\'\'\'اختبارات مكتبة {project_name}
Tests for {project_name} library
\'\'\'

import pytest
from {project_name.replace("-", "_")} import {project_name.replace('-', '_').replace(' ', '_').title()}

def test_greet():
    # اختبار دالة التحية
    lib = {project_name.replace('-', '_').replace(' ', '_').title()}("أحمد")
    result = lib.greet()
    assert "أحمد" in result
    assert "مرحباً" in result

def test_calculate():
    # اختبار دالة الحساب
    lib = {project_name.replace('-', '_').replace(' ', '_').title()}()
    result = lib.calculate(5, 3)
    assert result == 8

def test_process_data():
    # اختبار معالجة البيانات
    lib = {project_name.replace('-', '_').replace(' ', '_').title()}()
    data = [1, 2, 3, 4, 5]
    result = lib.process_data(data)
    
    assert result["count"] == 5
    assert result["sum"] == 15
    assert result["first"] == 1
    assert result["last"] == 5

def test_empty_data():
    # اختبار البيانات الفارغة
    lib = {project_name.replace('-', '_').replace(' ', '_').title()}()
    result = lib.process_data([])
    
    assert result["count"] == 0
    assert result["sum"] == 0
    assert result["first"] is None
    assert result["last"] is None'''
        
        self._create_file(project_path / f'tests/test_{project_name.replace("-", "_")}.py', test_py)
        
        # مثال للاستخدام
        example_py = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\'\'\'مثال على استخدام مكتبة {project_name}
Example usage of {project_name} library
\'\'\'

from {project_name.replace("-", "_")} import {project_name.replace('-', '_').replace(' ', '_').title()}

def main():
    # إنشاء كائن من المكتبة
    lib = {project_name.replace('-', '_').replace(' ', '_').title()}("محمد")
    
    # تحية
    print(lib.greet())
    
    # حساب
    result = lib.calculate(10, 20)
    print(f"10 + 20 = {{result}}")
    
    # معالجة البيانات
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    processed = lib.process_data(data)
    print(f"البيانات المعالجة: {{processed}}")

if __name__ == "__main__":
    main()'''
        
        self._create_file(project_path / 'examples/basic_usage.py', example_py)
        
        # README للمكتبة
        readme_content = f"""# {project_name}

مكتبة Python مفيدة ومرنة

## التثبيت

```bash
pip install {project_name}
```

## الاستخدام السريع

```python
from {project_name.replace("-", "_")} import {project_name.replace('-', '_').replace(' ', '_').title()}

# إنشاء كائن
lib = {project_name.replace('-', '_').replace(' ', '_').title()}("اسمك")

# تحية
print(lib.greet())

# حساب
result = lib.calculate(5, 3)
print(result)  # 8

# معالجة البيانات
data = [1, 2, 3, 4, 5]
processed = lib.process_data(data)
print(processed)
```

## الميزات

- سهولة الاستخدام
- دعم اللغة العربية
- موثقة بالكامل
- اختبارات شاملة

## التطوير

```bash
# تثبيت متطلبات التطوير
pip install -e ".[dev]"

# تشغيل الاختبارات
pytest

# فحص الكود
flake8 src/
black src/
mypy src/
```

## الأمثلة

انظر مجلد `examples/` للمزيد من الأمثلة.

## الترخيص

MIT License - انظر ملف LICENSE للتفاصيل.
"""
        
        self._create_file(project_path / 'README.md', readme_content)

    def _microservice_template(self, project_path: Path, project_name: str):
        """قالب الخدمات المصغرة - Microservice template"""
        
        folders = [
            'src/handlers',
            'src/models',
            'src/services',
            'src/middleware',
            'src/utils',
            'tests',
            'docker',
            'k8s'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # FastAPI microservice
        requirements_txt = """fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
alembic>=1.11.0
redis>=4.6.0
httpx>=0.24.0
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-dotenv>=1.0.0"""
        
        self._create_file(project_path / 'requirements.txt', requirements_txt)
        
        # main.py
        main_py = f'''# -*- coding: utf-8 -*-
\'\'\'{project_name} Microservice
خدمة {project_name} المصغرة
\'\'\'

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime

# إنشاء التطبيق
app = FastAPI(
    title="{project_name} API",
    description="خدمة {project_name} المصغرة",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج، حدد النطاقات المسموحة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# النماذج
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str

class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    message: str
    timestamp: datetime
    processed: bool

# قاعدة بيانات وهمية في الذاكرة
messages_db = []

# النقاط الأساسية
@app.get("/")
async def root():
    # الصفحة الرئيسية
    return {{
        "service": "{project_name}",
        "message": "مرحباً بك في خدمة {project_name}",
        "version": "1.0.0",
        "docs": "/docs"
    }}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    # فحص حالة الخدمة
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        service="{project_name}",
        version="1.0.0"
    )

@app.post("/messages", response_model=MessageResponse)
async def create_message(message_request: MessageRequest):
    # إنشاء رسالة جديدة
    message_id = f"msg_{{len(messages_db) + 1}}"
    
    new_message = {{
        "id": message_id,
        "message": message_request.message,
        "user_id": message_request.user_id,
        "timestamp": datetime.now(),
        "processed": True
    }}
    
    messages_db.append(new_message)
    
    return MessageResponse(**new_message)

@app.get("/messages", response_model=List[MessageResponse])
async def get_messages(limit: int = 10, offset: int = 0):
    # الحصول على قائمة الرسائل
    return [
        MessageResponse(**msg) 
        for msg in messages_db[offset:offset + limit]
    ]

@app.get("/messages/{{message_id}}", response_model=MessageResponse)
async def get_message(message_id: str):
    # الحصول على رسالة محددة
    message = next((msg for msg in messages_db if msg["id"] == message_id), None)
    
    if not message:
        raise HTTPException(status_code=404, detail="الرسالة غير موجودة")
    
    return MessageResponse(**message)

@app.delete("/messages/{{message_id}}")
async def delete_message(message_id: str):
    # حذف رسالة
    global messages_db
    messages_db = [msg for msg in messages_db if msg["id"] != message_id]
    
    return {{"message": "تم حذف الرسالة بنجاح", "id": message_id}}

# معالج الأخطاء
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={{"detail": "خطأ داخلي في الخادم", "error": str(exc)}}
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )'''
        
        self._create_file(project_path / 'main.py', main_py)
        
        # Dockerfile
        dockerfile = f"""FROM python:3.11-slim

WORKDIR /app

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إعداد المتغيرات البيئية
ENV PYTHONPATH=/app
ENV PORT=8000

# فتح البورت
EXPOSE 8000

# تشغيل التطبيق
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]"""
        
        self._create_file(project_path / 'Dockerfile', dockerfile)
        
        # docker-compose.yml
        docker_compose = f"""version: '3.8'

services:
  {project_name.replace('_', '-')}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://user:password@postgres:5432/{project_name}
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB={project_name}
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:"""
        
        self._create_file(project_path / 'docker-compose.yml', docker_compose)
        
        # Kubernetes deployment
        k8s_deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {project_name.replace('_', '-')}
  labels:
    app: {project_name.replace('_', '-')}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {project_name.replace('_', '-')}
  template:
    metadata:
      labels:
        app: {project_name.replace('_', '-')}
    spec:
      containers:
      - name: {project_name.replace('_', '-')}
        image: {project_name.replace('_', '-')}:latest
        ports:
        - containerPort: 8000
        env:
        - name: PORT
          value: "8000"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: {project_name.replace('_', '-')}-service
spec:
  selector:
    app: {project_name.replace('_', '-')}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer"""
        
        self._create_file(project_path / 'k8s/deployment.yaml', k8s_deployment)
        
        # README
        readme_content = f"""# {project_name} Microservice

خدمة {project_name} المصغرة باستخدام FastAPI

## التشغيل المحلي

```bash
pip install -r requirements.txt
python main.py
```

التطبيق سيعمل على: http://localhost:8000

## التشغيل باستخدام Docker

```bash
docker build -t {project_name} .
docker run -p 8000:8000 {project_name}
```

## التشغيل باستخدام Docker Compose

```bash
docker-compose up -d
```

## النشر على Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## النقاط الأساسية

- `GET /` - الصفحة الرئيسية
- `GET /health` - فحص الحالة
- `POST /messages` - إنشاء رسالة
- `GET /messages` - قائمة الرسائل
- `GET /messages/{{id}}` - رسالة محددة
- `DELETE /messages/{{id}}` - حذف رسالة

## الميزات

- FastAPI مع التوثيق التلقائي
- دعم Docker و Kubernetes
- معالجة الأخطاء
- CORS support
- Health checks
- دعم اللغة العربية

## التطوير

```bash
# تشغيل مع إعادة التحميل التلقائي
uvicorn main:app --reload

# تشغيل الاختبارات
pytest

# فحص الكود
flake8 .
black .
```
"""
        
        self._create_file(project_path / 'README.md', readme_content)

    def _fullstack_template(self, project_path: Path, project_name: str):
        """قالب التطبيق الشامل - Full-stack application template"""
        
        folders = [
            'frontend/src/components',
            'frontend/src/pages',
            'frontend/src/services',
            'frontend/public',
            'backend/src/routes',
            'backend/src/models',
            'backend/src/controllers',
            'backend/src/middleware',
            'database/migrations',
            'database/seeds',
            'docker'
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # Frontend package.json
        frontend_package = {
            "name": f"{project_name}-frontend",
            "version": "1.0.0",
            "description": f"واجهة {project_name}",
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1",
                "axios": "^1.4.0",
                "react-router-dom": "^6.14.0",
                "@mui/material": "^5.14.0",
                "@emotion/react": "^11.11.0",
                "@emotion/styled": "^11.11.0"
            }
        }
        
        self._create_file(project_path / 'frontend/package.json', 
                         json.dumps(frontend_package, indent=2, ensure_ascii=False))
        
        # Frontend App.js
        frontend_app = f"""import React, {{ useState, useEffect }} from 'react';
import {{ BrowserRouter as Router, Routes, Route, Link }} from 'react-router-dom';
import {{ 
  AppBar, 
  Toolbar, 
  Typography, 
  Container, 
  Button, 
  Box,
  Card,
  CardContent
}} from '@mui/material';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Home() {{
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    fetchData();
  }}, []);

  const fetchData = async () => {{
    try {{
      const response = await axios.get(`${{API_URL}}/api/status`);
      setData(response.data);
    }} catch (error) {{
      console.error('Error fetching data:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <Container maxWidth="lg" sx={{{{ mt: 4 }}}}>
      <Card>
        <CardContent>
          <Typography variant="h4" component="h1" gutterBottom>
            مرحباً بك في {project_name}
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            تطبيق شامل حديث
          </Typography>
          
          {{loading ? (
            <Typography>جاري التحميل...</Typography>
          ) : (
            <Box sx={{{{ mt: 3 }}}}>
              <Typography variant="h6">حالة الخادم:</Typography>
              <pre>{{JSON.stringify(data, null, 2)}}</pre>
            </Box>
          )}}
        </CardContent>
      </Card>
    </Container>
  );
}}

function About() {{
  return (
    <Container maxWidth="lg" sx={{{{ mt: 4 }}}}>
      <Card>
        <CardContent>
          <Typography variant="h4" component="h1" gutterBottom>
            حول {project_name}
          </Typography>
          <Typography variant="body1">
            هذا تطبيق شامل يضم:
          </Typography>
          <ul>
            <li>واجهة مستخدم حديثة باستخدام React</li>
            <li>خادم API باستخدام Node.js/Express</li>
            <li>قاعدة بيانات</li>
            <li>دعم Docker</li>
          </ul>
        </CardContent>
      </Card>
    </Container>
  );
}}

function App() {{
  return (
    <Router>
      <Box sx={{{{ flexGrow: 1 }}}}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{{{ flexGrow: 1 }}}}>
              {project_name}
            </Typography>
            <Button color="inherit" component={{Link}} to="/">
              الرئيسية
            </Button>
            <Button color="inherit" component={{Link}} to="/about">
              حول
            </Button>
          </Toolbar>
        </AppBar>

        <Routes>
          <Route path="/" element={{<Home />}} />
          <Route path="/about" element={{<About />}} />
        </Routes>
      </Box>
    </Router>
  );
}}

export default App;"""
        
        self._create_file(project_path / 'frontend/src/App.js', frontend_app)
        
        # Backend package.json
        backend_package = {
            "name": f"{project_name}-backend",
            "version": "1.0.0",
            "description": f"خادم {project_name}",
            "main": "src/server.js",
            "scripts": {
                "start": "node src/server.js",
                "dev": "nodemon src/server.js",
                "test": "jest"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "helmet": "^7.0.0",
                "morgan": "^1.10.0",
                "dotenv": "^16.3.1",
                "mongoose": "^7.4.0",
                "bcryptjs": "^2.4.3",
                "jsonwebtoken": "^9.0.1"
            },
            "devDependencies": {
                "nodemon": "^3.0.1",
                "jest": "^29.6.1"
            }
        }
        
        self._create_file(project_path / 'backend/package.json', 
                         json.dumps(backend_package, indent=2, ensure_ascii=False))
        
        # Backend server.js
        backend_server = f"""const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({{ extended: true }}));

// Routes
app.get('/', (req, res) => {{
  res.json({{
    message: 'مرحباً بك في {project_name} API',
    version: '1.0.0',
    status: 'running'
  }});
}});

app.get('/api/status', (req, res) => {{
  res.json({{
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: '{project_name}',
    version: '1.0.0',
    database: 'connected',
    features: [
      'RESTful API',
      'دعم CORS',
      'أمان محسن',
      'توثيق تلقائي'
    ]
  }});
}});

app.get('/api/users', (req, res) => {{
  // مثال على قائمة المستخدمين
  res.json([
    {{ id: 1, name: 'أحمد محمد', email: 'ahmed@example.com' }},
    {{ id: 2, name: 'فاطمة أحمد', email: 'fatima@example.com' }},
    {{ id: 3, name: 'محمد علي', email: 'mohamed@example.com' }}
  ]);
}});

app.post('/api/users', (req, res) => {{
  const {{ name, email }} = req.body;
  
  if (!name || !email) {{
    return res.status(400).json({{
      error: 'الاسم والإيميل مطلوبان'
    }});
  }}
  
  const newUser = {{
    id: Date.now(),
    name,
    email,
    createdAt: new Date().toISOString()
  }};
  
  res.status(201).json(newUser);
}});

// Serve static files from React app
if (process.env.NODE_ENV === 'production') {{
  app.use(express.static(path.join(__dirname, '../frontend/build')));
  
  app.get('*', (req, res) => {{
    res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
  }});
}}

// Error handling
app.use((req, res) => {{
  res.status(404).json({{
    error: 'الطريق غير موجود',
    path: req.path
  }});
}});

app.use((err, req, res, next) => {{
  console.error(err.stack);
  res.status(500).json({{
    error: 'خطأ داخلي في الخادم'
  }});
}});

app.listen(PORT, () => {{
  console.log(`🚀 الخادم يعمل على البورت ${{PORT}}`);
  console.log(`📱 الواجهة: http://localhost:${{PORT}}`);
  console.log(`🔗 API: http://localhost:${{PORT}}/api`);
}});

module.exports = app;"""
        
        self._create_file(project_path / 'backend/src/server.js', backend_server)
        
        # Docker Compose للتطبيق الشامل
        docker_compose_full = f"""version: '3.8'

services:
  frontend:
    build: 
      context: ./frontend
      dockerfile: ../docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

  backend:
    build:
      context: ./backend  
      dockerfile: ../docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - NODE_ENV=development
      - MONGODB_URI=mongodb://mongo:27017/{project_name}
    depends_on:
      - mongo
    volumes:
      - ./backend:/app
      - /app/node_modules

  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_DATABASE={project_name}
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:"""
        
        self._create_file(project_path / 'docker-compose.yml', docker_compose_full)
        
        # Dockerfile للـ Frontend
        dockerfile_frontend = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]"""
        
        self._create_file(project_path / 'docker/Dockerfile.frontend', dockerfile_frontend)
        
        # Dockerfile للـ Backend
        dockerfile_backend = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8000

CMD ["npm", "run", "dev"]"""
        
        self._create_file(project_path / 'docker/Dockerfile.backend', dockerfile_backend)
        
        # README شامل
        readme_content = f"""# {project_name}

تطبيق شامل (Full-Stack) حديث

## البنية

```
{project_name}/
├── frontend/          # واجهة المستخدم (React)
├── backend/           # الخادم (Node.js/Express)
├── database/          # قاعدة البيانات
├── docker/            # ملفات Docker
└── docker-compose.yml # إعداد الحاويات
```

## التشغيل السريع

### باستخدام Docker (الطريقة المفضلة)

```bash
docker-compose up -d
```

الوصول للتطبيق:
- الواجهة: http://localhost:3000
- API: http://localhost:8000
- قاعدة البيانات: localhost:27017

### التشغيل المحلي

#### الخادم (Backend)
```bash
cd backend
npm install
npm run dev
```

#### الواجهة (Frontend)
```bash
cd frontend
npm install
npm start
```

## الميزات

### الواجهة (Frontend)
- React 18 مع Hooks
- Material-UI للتصميم
- React Router للتنقل
- Axios للـ API calls
- دعم اللغة العربية

### الخادم (Backend)
- Express.js
- MongoDB مع Mongoose
- JWT للمصادقة
- CORS support
- Security headers
- Error handling

### البنية التحتية
- Docker containerization
- MongoDB database
- Environment configuration
- Hot reload للتطوير

## API Endpoints

- `GET /` - معلومات الخادم
- `GET /api/status` - حالة الخادم
- `GET /api/users` - قائمة المستخدمين
- `POST /api/users` - إنشاء مستخدم جديد

## التطوير

### إضافة ميزة جديدة

1. إضافة Route في الخادم (`backend/src/routes/`)
2. إضافة Component في الواجهة (`frontend/src/components/`)
3. تحديث التنقل (`frontend/src/App.js`)

### نشر التطبيق

```bash
# بناء الواجهة
cd frontend && npm run build

# تشغيل في وضع الإنتاج
NODE_ENV=production npm start
```

## المتطلبات

- Node.js 18+
- Docker & Docker Compose
- MongoDB (اختياري للتطوير المحلي)

## المساهمة

1. Fork المشروع
2. إنشاء branch جديد
3. إضافة التغييرات
4. إرسال Pull Request

## الترخيص

MIT License
"""
        
        self._create_file(project_path / 'README.md', readme_content)

    def list_templates(self):
        """عرض قائمة القوالب المتاحة"""
        print("📋 القوالب المتاحة:")
        print("================")
        
        template_descriptions = {
            'web': 'تطبيق ويب حديث (React)',
            'api': 'API REST (Node.js/Express)',
            'desktop': 'تطبيق سطح المكتب (Python/Tkinter)',
            'mobile': 'تطبيق جوال (React Native)',
            'cli': 'أداة سطر الأوامر (Python/Click)',
            'library': 'مكتبة Python',
            'microservice': 'خدمة مصغرة (FastAPI)',
            'fullstack': 'تطبيق شامل (React + Node.js)'
        }
        
        for template_type, description in template_descriptions.items():
            print(f"  🔹 {template_type:<12} - {description}")

def main():
    parser = argparse.ArgumentParser(
        description="أداة إنشاء هياكل التطبيقات الأساسية",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  %(prog)s create my-web-app web
  %(prog)s create my-api api  
  %(prog)s create my-tool cli
  %(prog)s list
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='الأوامر المتاحة')
    
    # أمر الإنشاء
    create_parser = subparsers.add_parser('create', help='إنشاء مشروع جديد')
    create_parser.add_argument('name', help='اسم المشروع')
    create_parser.add_argument('type', help='نوع المشروع', 
                              choices=['web', 'api', 'desktop', 'mobile', 'cli', 'library', 'microservice', 'fullstack'])
    create_parser.add_argument('-o', '--output', default='.', help='مجلد الإخراج (افتراضي: .)')
    
    # أمر القائمة
    list_parser = subparsers.add_parser('list', help='عرض القوالب المتاحة')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    generator = AppGenerator()
    
    if args.command == 'create':
        success = generator.create_project(args.name, args.type, args.output)
        if success:
            print(f"\n🎉 تم إنشاء المشروع بنجاح!")
            print(f"📁 المسار: {Path(args.output) / args.name}")
            print(f"📖 اقرأ ملف README.md للحصول على تعليمات التشغيل")
        else:
            print(f"\n❌ فشل في إنشاء المشروع")
            sys.exit(1)
    
    elif args.command == 'list':
        generator.list_templates()

if __name__ == "__main__":
    main()
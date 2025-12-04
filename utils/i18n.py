"""
نظام الترجمة والدعم متعدد اللغات
"""
import json
import streamlit as st
from pathlib import Path


class TranslationManager:
    """مدير الترجمات"""
    
    def __init__(self, translations_file: str = "translations.json"):
        """
        تهيئة مدير الترجمات
        
        Args:
            translations_file: مسار ملف الترجمات
        """
        self.translations_file = translations_file
        self.translations = self._load_translations()
        
        # تهيئة اللغة في session_state
        if 'language' not in st.session_state:
            st.session_state.language = 'ar'  # اللغة الافتراضية
    
    def _load_translations(self) -> dict:
        """تحميل ملف الترجمات"""
        try:
            file_path = Path(self.translations_file)
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                st.error(f"ملف الترجمات غير موجود: {self.translations_file}")
                return {'ar': {}, 'en': {}}
        except Exception as e:
            st.error(f"خطأ في تحميل الترجمات: {str(e)}")
            return {'ar': {}, 'en': {}}
    
    def get(self, key: str, lang: str = None) -> str:
        """
        الحصول على نص مترجم
        
        Args:
            key: مفتاح الترجمة (يدعم النقاط للمفاتيح المتداخلة، مثل 'nav.dashboard')
            lang: اللغة (إذا لم تحدد، يستخدم اللغة الحالية من session_state)
            
        Returns:
            النص المترجم أو المفتاح نفسه إذا لم يتم العثور على الترجمة
        """
        if lang is None:
            lang = st.session_state.get('language', 'ar')
        
        # التعامل مع المفاتيح المتداخلة
        keys = key.split('.')
        value = self.translations.get(lang, {})
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)
            else:
                return key
        
        return value if value else key
    
    def t(self, key: str) -> str:
        """اختصار لـ get()"""
        return self.get(key)
    
    def switch_language(self):
        """تبديل اللغة"""
        current = st.session_state.get('language', 'ar')
        st.session_state.language = 'en' if current == 'ar' else 'ar'
    
    def get_current_language(self) -> str:
        """الحصول على اللغة الحالية"""
        return st.session_state.get('language', 'ar')
    
    def is_rtl(self) -> bool:
        """التحقق من أن الاتجاه من اليمين لليسار"""
        return st.session_state.get('language', 'ar') == 'ar'
    
    def get_direction(self) -> str:
        """الحصول على اتجاه النص"""
        return 'rtl' if self.is_rtl() else 'ltr'
    
    def get_text_align(self) -> str:
        """الحصول على محاذاة النص"""
        return 'right' if self.is_rtl() else 'left'


def create_language_switcher(tm: TranslationManager):
    """
    إنشاء مبدل اللغة في الشريط الجانبي
    
    Args:
        tm: مدير الترجمات
    """
    current_lang = tm.get_current_language()
    lang_text = tm.get('buttons.change_language')
    
    # زر تبديل اللغة
    if st.sidebar.button(f"🌐 {lang_text}", use_container_width=True):
        tm.switch_language()
        st.rerun()


def get_dynamic_css(tm: TranslationManager) -> str:
    """
    إنشاء CSS ديناميكي حسب اللغة
    
    Args:
        tm: مدير الترجمات
        
    Returns:
        كود CSS
    """
    direction = tm.get_direction()
    text_align = tm.get_text_align()
    font = "Tajawal" if tm.is_rtl() else "Inter"
    
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&family=Inter:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {{
        font-family: '{font}', sans-serif;
        direction: {direction};
        text-align: {text_align};
    }}
    
    .stApp {{
        direction: {direction};
    }}
    
    /* تنسيق الأزرار */
    .stButton>button {{
        background-color: #1976D2;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background-color: #0D47A1;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    /* تنسيق البطاقات الصغيرة */
    .metric-card-small {{
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        min-height: 100px;
    }}
    
    /* العناوين */
    h1, h2, h3, h4 {{
        color: #0D47A1;
        direction: {direction};
        text-align: {text_align};
    }}
    
    /* الجداول */
    .dataframe {{
        direction: {direction};
        font-size: 14px;
    }}
    
    /* النافذة المنبثقة */
    .modal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .modal-content {{
        background: white;
        border-radius: 10px;
        max-width: 90%;
        max-height: 90%;
        overflow-y: auto;
        padding: 20px;
        direction: {direction};
    }}
    
    /* تحسينات عامة */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 10px 20px;
        border-radius: 5px;
    }}
    </style>
    """


# إنشاء مثيل عام من مدير الترجمات
tm = TranslationManager()

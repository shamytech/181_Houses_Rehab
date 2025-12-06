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
# إنشاء مثيل عام من مدير الترجمات
tm = TranslationManager()

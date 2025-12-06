"""
نظام الشريط الجانبي مع دعم RTL/LTR
"""
import streamlit as st
from utils.i18n import TranslationManager


def create_language_switcher(tm: TranslationManager):
    """
    إنشاء مبدل اللغة في الشريط الجانبي
    
    Args:
        tm: مدير الترجمات
    """
    current_lang = tm.get_current_language()
    lang_text = tm.get('buttons.change_language')
    
    # زر تبديل اللغة
    if st.sidebar.button(f"🌐 {lang_text}", use_container_width=True, key="lang_switcher"):
        tm.switch_language()
        st.rerun()


def get_sidebar_css(tm: TranslationManager) -> str:
    """
    إنشاء CSS للشريط الجانبي حسب اللغة
    
    Args:
        tm: مدير الترجمات
        
    Returns:
        كود CSS و JavaScript للشريط الجانبي
    """
    is_rtl = tm.is_rtl()
    direction = tm.get_direction()
    text_align = tm.get_text_align()
    current_lang = tm.get_current_language()
    
    # CSS الأساسي للشريط الجانبي
    css = f"""
    <style>
    /* ===== الشريط الجانبي عند الطي ===== */
    /* إخفاء العناصر عند الطي */
    [data-testid="stSidebar"][aria-expanded="false"] .element-container:not(:has(.stButton)),
    [data-testid="stSidebar"][aria-expanded="false"] img,
    [data-testid="stSidebar"][aria-expanded="false"] hr,
    [data-testid="stSidebar"][aria-expanded="false"] h3,
    [data-testid="stSidebar"][aria-expanded="false"] .stMarkdown,
    [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"] {{
        display: none !important;
    }}
    
    /* إخفاء النص في الأزرار عند الطي */
    [data-testid="stSidebar"][aria-expanded="false"] .stButton > button span {{
        display: none !important;
    }}
    
    /* توسيط الأزرار عند الطي */
    [data-testid="stSidebar"][aria-expanded="false"] .stButton {{
        display: flex !important;
        justify-content: center !important;
        margin: 0.5rem 0 !important;
    }}
    
    [data-testid="stSidebar"][aria-expanded="false"] .stButton > button {{
        width: 50px !important;
        padding: 0.75rem !important;
    }}
    
    /* ===== محاذاة النص عند الفتح ===== */
    [data-testid="stSidebar"][aria-expanded="true"] {{
        direction: {direction} !important;
        text-align: {text_align} !important;
    }}
    
    [data-testid="stSidebar"][aria-expanded="true"] * {{
        direction: {direction} !important;
        text-align: {text_align} !important;
    }}
    </style>
    """
    
    # إضافة CSS خاص بـ RTL
    if is_rtl:
        css += """
    <style>
    /* ===== موضع الشريط الجانبي في RTL ===== */
    [data-testid="stSidebar"] {
        right: 0 !important;
        left: auto !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        right: 0 !important;
        left: auto !important;
        transform: translateX(0) !important;
    }
    
    /* موضع زر الطي/الفتح */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        right: auto !important;
        left: 0.5rem !important;
    }
    
    /* إصلاح هامش المحتوى الرئيسي */
    .main .block-container {
        margin-left: 0 !important;
        margin-right: auto !important;
    }
    </style>
    """
    else:
        # CSS للغة الإنجليزية (LTR) - إصلاح زر الطي/الفتح
        css += """
    <style>
    /* ===== LTR - إصلاح زر طي/فتح الشريط الجانبي ===== */
    
    /* تثبيت زر الطي/الفتح في مكان ثابت حتى لا يختفي مع الشريط الجانبي */
    [data-testid="stSidebarCollapseButton"] {
        position: fixed !important;
        left: 0.5rem !important;
        top: 0.5rem !important;
        z-index: 999999 !important;
        background: white !important;
        border-radius: 0.375rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24) !important;
    }
    
    [data-testid="stSidebarCollapseButton"] button {
        background: white !important;
        border: none !important;
        padding: 0.5rem !important;
    }
    
    /* عند الطي - الشريط الجانبي يختفي لكن الزر يبقى */
    [data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(-100%) !important;
    }
    
    /* إذا كان هناك عنصر stSidebarCollapsedControl فنثبته أيضاً */
    [data-testid="stSidebarCollapsedControl"] {
        position: fixed !important;
        left: 0.5rem !important;
        top: 0.5rem !important;
        z-index: 999999 !important;
    }
    </style>
    """
    
    # إضافة JavaScript لترجمة التبويبات
    js_code = f"""
    <script>
    (function() {{
        const lang = '{current_lang}';
        const isRTL = {'true' if is_rtl else 'false'};
        
        // ترجمة التبويبات
        const translations = {{
            'ar': {{
                'Beneficiaries': '👥 المستفيدون',
                'Interactive_Map': '📍 الخريطة التفاعلية',
                'Statistics': '📊 الإحصائيات',
                'Work_Items': '🔧 البنود والأعمال',
                'app': '🏠 الرئيسية'
            }},
            'en': {{
                'المستفيدون': '👥 Beneficiaries',
                'الخريطة التفاعلية': '📍 Interactive Map',
                'الإحصائيات': '📊 Statistics',
                # 'البنود والأعمال': '🔧 Work Items',
                'الرئيسية': '🏠 Home'
            }}
        }};
        
        function translateTabs() {{
            const navLinks = document.querySelectorAll('[data-testid="stSidebarNav"] a span');
            navLinks.forEach(link => {{
                const text = link.textContent.trim();
                // تنظيف النص للمقارنة (إزالة المسافات الزائدة فقط)
                const cleanText = text.split(' ').filter(w => w.length > 1).join(' ');
                
                if (translations[lang]) {{
                    for (const [key, value] of Object.entries(translations[lang])) {{
                        if (cleanText.includes(key.replace(/_/g, ' ')) || cleanText.includes(key)) {{
                            link.textContent = value;
                            break;
                        }}
                    }}
                }}
            }});
        }}
        
        function init() {{
            translateTabs();
        }}
        
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', init);
        }} else {{
            init();
        }}
        
        setTimeout(init, 500);
        setTimeout(init, 1000);
        
        const observer = new MutationObserver(init);
        observer.observe(document.body, {{ childList: true, subtree: true }});
    }})();
    </script>
    """
    
    return css + js_code

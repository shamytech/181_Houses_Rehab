"""
نظام التنسيقات العامة للتطبيق مع دعم RTL/LTR
"""
from utils.i18n import TranslationManager


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
    
    /* إخفاء شريط Streamlit العلوي */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* إخفاء شريط Deploy و File change */
    .stDeployButton {{
        display: none !important;
    }}
    
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    
    [data-testid="stToolbar"] {{
        display: none !important;
    }}
    
    /* إزالة الفراغ العلوي */
    .stApp > header {{
        display: none !important;
    }}
    
    .main .block-container {{
        padding: 0 1rem 1rem 1rem !important;
        margin-top: 0 !important;
    }}
    
    /* إزالة الـ padding من جميع عناصر Streamlit الديناميكية */
    [class*="st-emotion-cache"] {{
        padding-top: 0 !important;
    }}
    
    .stApp [data-testid="stAppViewContainer"] > .main {{
        padding-top: 0 !important;
    }}
    
    .stApp [data-testid="stAppViewContainer"] > .main > div {{
        padding-top: 0 !important;
    }}
    
    .stApp [data-testid="stAppViewContainer"] > .main > div > div {{
        padding: 0 1rem 1rem 1rem !important;
    }}
    
    /* استهداف block-container مباشرة */
    .stApp [data-testid="block-container"] {{
        padding: 0 1rem 1rem 1rem !important;
    }}
    
    /* استهداف الـ class الديناميكي */
    div[class*="st-emotion-cache"][style*="width: 100%"] {{
        padding-top: 0 !important;
    }}
    
    .stMain > div:first-child {{
        padding-top: 0 !important;
    }}
    
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



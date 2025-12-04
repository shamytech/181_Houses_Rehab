"""
ملف الإعدادات والألوان الخاص بلوحة تحكم UNDP
"""

# ألوان العلامة التجارية UNDP
PRIMARY_BLUE = "#1976D2"
PRIMARY_DARK = "#0D47A1"
PRIMARY_LIGHT = "#42A5F5"

# ألوان الحالات
SUCCESS_GREEN = "#4CAF50"   # مكتمل / ضرر خفيف
WARNING_YELLOW = "#FFC107"  # قيد التنفيذ / ضرر متوسط
DANGER_RED = "#F44336"      # معلق / ضرر شديد
INFO_BLUE = "#2196F3"       # معلومات

# ألوان محايدة
GRAY_50 = "#FAFAFA"
GRAY_100 = "#F5F5F5"
GRAY_200 = "#EEEEEE"
GRAY_700 = "#616161"
GRAY_900 = "#212121"

# خلفيات
BG_MAIN = "#F8F9FA"
BG_CARD = "#FFFFFF"

# إعدادات الصفحة
PAGE_CONFIG = {
    "page_title": "UNDP - لوحة تحكم إعادة تأهيل المنازل",
    "page_icon": "🏠",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# إعدادات الخريطة الافتراضية
DEFAULT_MAP_CENTER = [33.5138, 36.2765]  # دمشق
DEFAULT_ZOOM = 11

# مسارات البيانات
DATA_PATH = "data/raw/181-UNDP-Houses Rehab Tracker.xlsx"
IMAGES_PATH = "assets/images/"

# حالات الضرر
DAMAGE_STATUS = {
    "ضرر خفيف": {"color": SUCCESS_GREEN, "icon": "✓"},
    "ضرر متوسط": {"color": WARNING_YELLOW, "icon": "⚠"},
    "ضرر شديد": {"color": DANGER_RED, "icon": "✗"},
}

# Custom CSS للتنسيق
CUSTOM_CSS = """
<style>
/* خط عربي احترافي - Tajawal */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
}

/* تنسيق البطاقات */
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    text-align: center;
}

/* تنسيق الجداول */
.dataframe {
    font-size: 14px;
}

/* ألوان الأزرار */
.stButton>button {
    background-color: #1976D2;
    color: white;
    border-radius: 5px;
}

.stButton>button:hover {
    background-color: #0D47A1;
}

/* العناوين */
h1, h2, h3 {
    color: #0D47A1;
}
</style>
"""

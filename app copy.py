"""
لوحة تحكم UNDP - إعادة تأهيل المنازل
الصفحة الرئيسية - الإحصائيات والتقارير
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# إضافة مسار المشروع
sys.path.append(str(Path(__file__).parent))

from config import *
from utils.data_loader import (
    load_houses_data,
    load_main_items,
    load_sub_items,
    get_damage_status_counts,
    get_location_counts,
    get_house_type_counts,
    get_demographic_stats
)
from utils.charts import (
    create_damage_pie_chart,
    create_location_bar_chart,
    create_demographic_bar_chart,
    create_house_type_pie_chart
)
from utils.i18n import tm
from utils.styles import get_dynamic_css
from utils.sidebar import get_sidebar_css, create_language_switcher
from utils.header import create_header

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)

# ================================
# CSS المحسّن للتخطيط الديناميكي
# ================================
ENHANCED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Inter:wght@400;500;700;800&display=swap');

/* المتغيرات الأساسية */
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #3b82f6;
    --dark: #1e293b;
    --light: #f8fafc;
}

/* شبكة 8 أعمدة */
.grid-8 {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 10px;
    margin: 15px 0;
}

/* شبكة مختلطة */
.mixed-grid {
    display: grid;
    gap: 15px;
    margin: 20px 0;
}

.grid-2-1 {
    grid-template-columns: 2fr 1fr;
}

.grid-1-2 {
    grid-template-columns: 1fr 2fr;
}

.grid-3-cols {
    grid-template-columns: repeat(3, 1fr);
}

.grid-4-cols {
    grid-template-columns: repeat(4, 1fr);
}

/* بطاقة صغيرة للمؤشرات */
.mini-card {
    background: white;
    border-radius: 10px;
    padding: 12px 8px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    border-top: 3px solid var(--border-color, var(--primary));
    transition: all 0.2s ease;
}

.mini-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.mini-value {
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--text-color, var(--dark));
    margin: 4px 0;
}

.mini-label {
    font-size: 0.65rem;
    color: #64748b;
    font-weight: 500;
}

.mini-icon {
    font-size: 1.2rem;
    margin-bottom: 4px;
}

/* بطاقة عمودية كبيرة */
.vertical-card {
    background: linear-gradient(135deg, white, #f1f5f9);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.vertical-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--gradient-start, var(--primary)), var(--gradient-end, var(--secondary)));
}

.vc-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--dark);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.vc-content {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.vc-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: white;
    border-radius: 8px;
    border-right: 3px solid var(--item-color, #e2e8f0);
}

.vc-item-label {
    font-size: 0.85rem;
    color: #475569;
}

.vc-item-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--item-color, var(--dark));
}

/* بطاقة التكلفة المميزة */
.cost-highlight {
    background: linear-gradient(135deg, var(--dark) 0%, #334155 100%);
    border-radius: 16px;
    padding: 20px;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.cost-highlight::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
}

.ch-icon {
    font-size: 2rem;
    margin-bottom: 10px;
    color: #4ade80;
}

.ch-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #4ade80;
    margin: 8px 0;
}

.ch-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

/* جدول مؤشرات مدمج */
.stats-table {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.st-header {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--dark);
    padding: 8px 12px;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 12px;
}

.st-row {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    padding: 10px 12px;
    border-bottom: 1px solid #f1f5f9;
    transition: background 0.2s;
}

.st-row:hover {
    background: #f8fafc;
}

.st-icon {
    font-size: 1.2rem;
    margin-left: 12px;
}

.st-label {
    font-size: 0.85rem;
    color: #64748b;
}

.st-value {
    font-size: 1rem;
    font-weight: 700;
    color: var(--value-color, var(--dark));
    text-align: left;
}

/* بطاقة مخطط مدمجة */
.chart-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    height: 100%;
}

.cc-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.cc-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--dark);
}

.cc-badge {
    background: var(--badge-bg, #f0f9ff);
    color: var(--badge-color, var(--info));
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* بطاقة التقدم */
.progress-card {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.progress-item {
    margin-bottom: 16px;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.progress-label {
    font-size: 0.85rem;
    color: #64748b;
}

.progress-value {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--dark);
}

.progress-bar {
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--progress-start, var(--primary)), var(--progress-end, var(--secondary)));
    border-radius: 4px;
    transition: width 0.3s ease;
}

/* عنوان القسم المحسن */
.section-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--dark);
    margin: 30px 0 20px 0;
    padding: 12px 0;
    border-bottom: 2px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, #e2e8f0, transparent);
}

/* تكيف مع اللغات */
[dir="rtl"] {
    font-family: 'Tajawal', sans-serif;
}

[dir="ltr"] {
    font-family: 'Inter', sans-serif;
}

/* تعديلات RTL للجدول */
[dir="rtl"] .st-row {
    direction: rtl;
}

[dir="rtl"] .st-icon {
    margin-left: 12px;
    margin-right: 0;
}

[dir="rtl"] .st-value {
    text-align: right;
}

/* للشاشات المتوسطة */
@media (max-width: 1200px) {
    .grid-8 { grid-template-columns: repeat(4, 1fr); }
    .grid-2-1, .grid-1-2 { grid-template-columns: 1fr; }
}

/* للشاشات الصغيرة */
@media (max-width: 768px) {
    .grid-8 { grid-template-columns: repeat(2, 1fr); }
    .grid-3-cols { grid-template-columns: 1fr; }
    .grid-4-cols { grid-template-columns: repeat(2, 1fr); }
}

/* ألوان المؤشرات */
.indicator-primary { --border-color: var(--primary); --text-color: var(--primary); }
.indicator-success { --border-color: var(--success); --text-color: var(--success); }
.indicator-warning { --border-color: var(--warning); --text-color: var(--warning); }
.indicator-danger { --border-color: var(--danger); --text-color: var(--danger); }
.indicator-info { --border-color: var(--info); --text-color: var(--info); }
.indicator-purple { --border-color: #8b5cf6; --text-color: #8b5cf6; }
.indicator-pink { --border-color: #ec4899; --text-color: #ec4899; }
.indicator-cyan { --border-color: #06b6d4; --text-color: #06b6d4; }
</style>
"""

# تطبيق CSS
st.markdown(ENHANCED_CSS, unsafe_allow_html=True)
st.markdown(get_dynamic_css(tm), unsafe_allow_html=True)
st.markdown(get_sidebar_css(tm), unsafe_allow_html=True)

# الهيدر الموحد
create_header(page_title=f"📊 {tm.t('statistics.title')}")

# الشريط الجانبي
with st.sidebar:
    st.image("https://www.undp.org/themes/custom/undp/logo.svg", width=180)
    st.markdown("---")
    create_language_switcher(tm)

# تحميل البيانات
@st.cache_data
def load_all_data():
    file_path = Path(DATA_PATH)
    if not file_path.exists():
        return None, None, None, None
    
    houses = load_houses_data(str(file_path))
    main_items = load_main_items(str(file_path))
    sub_items = load_sub_items(str(file_path))
    
    try:
        nominated = pd.read_excel(str(file_path), sheet_name='Nominated Houses')
    except:
        nominated = pd.DataFrame()
    
    return houses, main_items, sub_items, nominated

df, main_items_df, sub_items_df, nominated_df = load_all_data()

if df is not None and not df.empty:
    
    # حساب جميع الإحصائيات
    nominated_count = len(nominated_df) if nominated_df is not None and not nominated_df.empty else 0
    evaluated_count = len(df)
    zamalka_count = len(df[df['القرية'] == 'زملكا']) if 'القرية' in df.columns else 0
    maarat_count = len(df[df['القرية'] == 'مركز معرة النعمان']) if 'القرية' in df.columns else 0
    
    ownership_col = 'هل لديك وثيقة اثبات ملكية حديث؟'
    safe_access_col = 'هل يتوفر وصول آمن إلى المنزل؟'
    has_doc = len(df[df[ownership_col] == 'نعم']) if ownership_col in df.columns else 0
    no_doc = len(df[df[ownership_col] == 'لا']) if ownership_col in df.columns else 0
    safe_yes = len(df[df[safe_access_col] == 'نعم']) if safe_access_col in df.columns else 0
    safe_no = len(df[df[safe_access_col] == 'لا']) if safe_access_col in df.columns else 0
    
    damage_col = 'وصف حالة الضرر من وجهة نظرك كمالك للمنزل'
    damage_counts_series = df[damage_col].value_counts() if damage_col in df.columns else pd.Series()
    light = damage_counts_series.get('ضرر خفيف', 0)
    medium = damage_counts_series.get('ضرر متوسط', 0)
    severe = damage_counts_series.get('ضرر شديد', 0)
    
    house_type_col = 'نوع المنزل'
    house_types = df[house_type_col].value_counts() if house_type_col in df.columns else pd.Series()
    
    cost_col = 'Grand Total'
    if cost_col in df.columns:
        costs = pd.to_numeric(df[cost_col], errors='coerce').dropna()
        total_cost = costs.sum()
        avg_cost = costs.mean() if len(costs) > 0 else 0
        max_cost = costs.max() if len(costs) > 0 else 0
        min_cost = costs.min() if len(costs) > 0 else 0
    else:
        total_cost, avg_cost, max_cost, min_cost = 0, 0, 0, 0
    
    demo_stats = get_demographic_stats(df)
    
    # ================================
    # صف 1: المؤشرات الرئيسية (8 أعمدة)
    # ================================
    dir_attr = 'dir="rtl"' if tm.get_current_language() == 'ar' else 'dir="ltr"'
    
    st.markdown(f"""
    <div {dir_attr}>
        <div class="section-title">
            🎯 {tm.t('sections.key_indicators')}
        </div>
        <div class="grid-8">
            <div class="mini-card indicator-purple">
                <div class="mini-icon">🏆</div>
                <div class="mini-value">{nominated_count}</div>
                <div class="mini-label">{tm.t('dashboard.nominated_houses')}</div>
            </div>
            <div class="mini-card indicator-info">
                <div class="mini-icon">📋</div>
                <div class="mini-value">{evaluated_count}</div>
                <div class="mini-label">{tm.t('dashboard.houses_under_evaluation')}</div>
            </div>
            <div class="mini-card indicator-success">
                <div class="mini-icon">🟢</div>
                <div class="mini-value">{light}</div>
                <div class="mini-label">{tm.t('metrics.light_damage')}</div>
            </div>
            <div class="mini-card indicator-warning">
                <div class="mini-icon">🟡</div>
                <div class="mini-value">{medium}</div>
                <div class="mini-label">{tm.t('metrics.medium_damage')}</div>
            </div>
            <div class="mini-card indicator-danger">
                <div class="mini-icon">🔴</div>
                <div class="mini-value">{severe}</div>
                <div class="mini-label">{tm.t('metrics.severe_damage')}</div>
            </div>
            <div class="mini-card indicator-cyan">
                <div class="mini-icon">🏘️</div>
                <div class="mini-value">{zamalka_count}</div>
                <div class="mini-label">{tm.t('dashboard.zamalka')}</div>
            </div>
            <div class="mini-card indicator-pink">
                <div class="mini-icon">🏘️</div>
                <div class="mini-value">{maarat_count}</div>
                <div class="mini-label">{tm.t('dashboard.maarat')}</div>
            </div>
            <div class="mini-card indicator-primary">
                <div class="mini-icon">👥</div>
                <div class="mini-value">{demo_stats.get('إجمالي الأفراد', 0)}</div>
                <div class="mini-label">{tm.t('metrics.total_individuals')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ================================
    # صف 2: التكاليف + الديموغرافيا (2-1)
    # ================================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # بطاقة التكاليف
        st.markdown(f"""
        <div class="vertical-card" style="--gradient-start: #667eea; --gradient-end: #764ba2;">
            <div class="vc-title">💰 {tm.t('dashboard.costs')}</div>
            <div class="vc-content">
                <div class="cost-highlight">
                    <div class="ch-icon">💵</div>
                    <div class="ch-value">${total_cost:,.0f}</div>
                    <div class="ch-label">{tm.t('dashboard.total_cost')}</div>
                </div>
                <div class="vc-item" style="--item-color: #10b981;">
                    <span class="vc-item-label">{tm.t('dashboard.average_cost')}</span>
                    <span class="vc-item-value">${avg_cost:,.0f}</span>
                </div>
                <div class="vc-item" style="--item-color: #f59e0b;">
                    <span class="vc-item-label">{tm.t('dashboard.max_cost')}</span>
                    <span class="vc-item-value">${max_cost:,.0f}</span>
                </div>
                <div class="vc-item" style="--item-color: #ef4444;">
                    <span class="vc-item-label">{tm.t('dashboard.min_cost')}</span>
                    <span class="vc-item-value">${min_cost:,.0f}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # بطاقة الديموغرافيا
        st.markdown(f"""
        <div class="stats-table" dir="rtl">
            <div class="st-header">👥 {tm.t('sections.demographics')}</div>
            <div class="st-row">
                <span class="st-icon">👨‍👩‍👧‍👦</span>
                <span class="st-label">{tm.t('metrics.total_families')}</span>
                <span class="st-value" style="--value-color: #667eea;">{demo_stats.get('إجمالي الأسر', 0)}</span>
            </div>
            <div class="st-row">
                <span class="st-icon">👨</span>
                <span class="st-label">{tm.t('fields.men')}</span>
                <span class="st-value" style="--value-color: #3b82f6;">{demo_stats.get('الرجال', 0)}</span>
            </div>
            <div class="st-row">
                <span class="st-icon">👩</span>
                <span class="st-label">{tm.t('fields.women')}</span>
                <span class="st-value" style="--value-color: #ec4899;">{demo_stats.get('النساء', 0)}</span>
            </div>
            <div class="st-row">
                <span class="st-icon">👶</span>
                <span class="st-label">{tm.t('fields.child_boys')} + {tm.t('fields.child_girls')}</span>
                <span class="st-value" style="--value-color: #f59e0b;">{demo_stats.get('الأطفال الذكور', 0) + demo_stats.get('الأطفال الإناث', 0)}</span>
            </div>
            <div class="st-row">
                <span class="st-icon">♿</span>
                <span class="st-label">{tm.t('metrics.disabled_persons')}</span>
                <span class="st-value" style="--value-color: #ef4444;">{demo_stats.get('ذوي الإعاقة', 0)}</span>
            </div>
            <div class="st-row">
                <span class="st-icon">👴</span>
                <span class="st-label">{tm.t('metrics.elderly')}</span>
                <span class="st-value" style="--value-color: #8b5cf6;">{demo_stats.get('كبار السن', 0)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ================================
    # صف 3: أنواع المنازل + الملكية والوصول
    # ================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # بطاقة أنواع المنازل
        st.markdown(f"""
        <div class="progress-card">
            <div class="vc-title">🏠 {tm.t('dashboard.house_type')}</div>
            <div class="progress-item">
                <div class="progress-header">
                    <span class="progress-label">منزل مستقل</span>
                    <span class="progress-value">{house_types.get('منزل مستقل', 0)}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(house_types.get('منزل مستقل', 0) / evaluated_count * 100) if evaluated_count > 0 else 0}%; --progress-start: #3b82f6; --progress-end: #06b6d4;"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-header">
                    <span class="progress-label">شقة طابقية</span>
                    <span class="progress-value">{house_types.get('شقة طابقية', 0)}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(house_types.get('شقة طابقية', 0) / evaluated_count * 100) if evaluated_count > 0 else 0}%; --progress-start: #8b5cf6; --progress-end: #a855f7;"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-header">
                    <span class="progress-label">ملحق</span>
                    <span class="progress-value">{house_types.get('ملحق', 0)}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(house_types.get('ملحق', 0) / evaluated_count * 100) if evaluated_count > 0 else 0}%; --progress-start: #f59e0b; --progress-end: #fbbf24;"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-header">
                    <span class="progress-label">أخرى</span>
                    <span class="progress-value">{house_types.get('أخرى', 0)}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(house_types.get('أخرى', 0) / evaluated_count * 100) if evaluated_count > 0 else 0}%; --progress-start: #10b981; --progress-end: #34d399;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # بطاقة الملكية
        st.markdown(f"""
        <div class="vertical-card" style="--gradient-start: #10b981; --gradient-end: #059669;">
            <div class="vc-title">📄 {tm.t('fields.ownership_doc')}</div>
            <div class="vc-content">
                <div class="vc-item" style="--item-color: #10b981;">
                    <span class="vc-item-label">✅ {tm.t('dashboard.has_ownership_doc')}</span>
                    <span class="vc-item-value">{has_doc}</span>
                </div>
                <div class="vc-item" style="--item-color: #ef4444;">
                    <span class="vc-item-label">❌ {tm.t('dashboard.no_ownership_doc')}</span>
                    <span class="vc-item-value">{no_doc}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # بطاقة الوصول الآمن
        st.markdown(f"""
        <div class="vertical-card" style="--gradient-start: #3b82f6; --gradient-end: #1e40af;">
            <div class="vc-title">🚪 {tm.t('fields.safe_access')}</div>
            <div class="vc-content">
                <div class="vc-item" style="--item-color: #10b981;">
                    <span class="vc-item-label">🟢 {tm.t('dashboard.safe_access_yes')}</span>
                    <span class="vc-item-value">{safe_yes}</span>
                </div>
                <div class="vc-item" style="--item-color: #f59e0b;">
                    <span class="vc-item-label">🔴 {tm.t('dashboard.safe_access_no')}</span>
                    <span class="vc-item-value">{safe_no}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ================================
    # المخططات التفاعلية
    # ================================
    st.markdown(f'<div class="section-title">📈 {tm.t("sections.cost_analysis")}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # مخطط حالة الضرر
        damage_counts = get_damage_status_counts(df)
        if damage_counts:
            fig = create_damage_pie_chart(damage_counts)
            fig.update_layout(
                title=tm.t('sections.damage_distribution'),
                height=350,
                font=dict(
                    family="Tajawal, Cairo, sans-serif" if tm.get_current_language() == 'ar' else "Inter, sans-serif",
                    size=14
                )
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # مخطط التوزيع الجغرافي
        location_counts = get_location_counts(df)
        if location_counts:
            fig = create_location_bar_chart(location_counts)
            fig.update_layout(
                title=tm.t('sections.geographic_distribution'),
                height=350,
                font=dict(
                    family="Tajawal, Cairo, sans-serif" if tm.get_current_language() == 'ar' else "Inter, sans-serif",
                    size=14
                )
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ================================
    # إحصائيات البنود
    # ================================
    if main_items_df is not None and not main_items_df.empty:
        st.markdown(f'<div class="section-title">🔧 {tm.t("sections.items_analysis")}</div>', unsafe_allow_html=True)
        
        if '_parent_index' in main_items_df.columns and 'البند الرئيسي' in main_items_df.columns:
            main_counts = main_items_df.groupby('البند الرئيسي').size().reset_index(name='العدد')
            main_counts = main_counts.nlargest(10, 'العدد')
            
            fig = px.bar(
                main_counts,
                x='العدد',
                y='البند الرئيسي',
                text='العدد',
                orientation='h',
                color='العدد',
                color_continuous_scale='Viridis'
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                title=tm.t('sections.most_requested_items'),
                showlegend=False,
                height=400,
                xaxis_title=tm.t('metrics.houses_count'),
                yaxis_title="",
                font=dict(
                    family="Tajawal, Cairo, sans-serif" if tm.get_current_language() == 'ar' else "Inter, sans-serif",
                    size=14
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # ================================
    # زر التصدير
    # ================================
    st.markdown(f'<div class="section-title">📥 {tm.t("statistics.export_reports")}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        summary_data = {
            tm.t('metrics.total_applications'): evaluated_count,
            tm.t('metrics.total_families'): demo_stats.get('إجمالي الأسر', 0),
            tm.t('metrics.total_individuals'): demo_stats.get('إجمالي الأفراد', 0),
            tm.t('dashboard.total_cost'): f"${total_cost:,.0f}",
            tm.t('dashboard.average_cost'): f"${avg_cost:,.0f}"
        }
        
        summary_df = pd.DataFrame(list(summary_data.items()), columns=['Indicator', 'Value'])
        
        csv = summary_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label=f"📄 {tm.t('buttons.export_summary_csv')}",
            data=csv,
            file_name="statistics_summary.csv",
            mime="text/csv"
        )
    
    with col2:
        from io import BytesIO
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            df.to_excel(writer, sheet_name='All Data', index=False)
        
        output.seek(0)
        
        st.download_button(
            label=f"📊 {tm.t('buttons.export_full_report')}",
            data=output,
            file_name="full_statistics_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.error(f"⚠️ {tm.t('messages.no_data')}")

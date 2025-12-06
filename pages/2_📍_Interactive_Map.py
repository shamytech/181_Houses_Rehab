"""
صفحة الخريطة التفاعلية
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from streamlit_folium import st_folium

# إضافة مسار المشروع
sys.path.append(str(Path(__file__).parent.parent))

from config import *
from utils.data_loader import load_houses_data, filter_houses
from utils.maps import create_houses_map, add_map_legend
from utils.i18n import tm
from utils.styles import get_dynamic_css
from utils.sidebar import get_sidebar_css, create_language_switcher
from utils.header import create_header

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)

# CSS ديناميكي حسب اللغة
st.markdown(get_dynamic_css(tm), unsafe_allow_html=True)
st.markdown(get_sidebar_css(tm), unsafe_allow_html=True)

# الهيدر الموحد
create_header(page_title=f"📍 {tm.t('map.title')}")

# الشريط الجانبي
with st.sidebar:
    st.image("https://www.undp.org/themes/custom/undp/logo.svg", width=180)
    st.markdown("---")
    create_language_switcher(tm)
    st.markdown("---")

# تحميل البيانات
@st.cache_data
def load_data():
    file_path = Path(__file__).parent.parent / DATA_PATH
    if not file_path.exists():
        st.error(f"⚠️ {tm.t('messages.no_data')}")
        return None
    return load_houses_data(str(file_path))

df = load_data()

if df is not None and not df.empty:
    
    # أدوات الفلترة
    st.markdown(f"### 🔍 {tm.t('map.filter_points')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # فلترة حسب المحافظة
        governorates = [tm.t('beneficiaries.all')] + sorted(df['المحافظة'].dropna().unique().tolist())
        selected_gov = st.selectbox(f"📍 {tm.t('beneficiaries.filter_governorate')}", governorates)
    
    with col2:
        # فلترة حسب حالة الضرر
        damage_statuses = [tm.t('beneficiaries.all')] + sorted(df['حالة الضرر'].dropna().unique().tolist())
        selected_damage = st.selectbox(f"⚠️ {tm.t('beneficiaries.filter_damage')}", damage_statuses)
    
    with col3:
        # فلترة حسب نوع المنزل
        house_types = [tm.t('beneficiaries.all')] + sorted(df['نوع المنزل'].dropna().unique().tolist())
        selected_type = st.selectbox(f"🏘️ {tm.t('beneficiaries.filter_house_type')}", house_types)
    
    # تطبيق الفلاتر
    all_text = tm.t('beneficiaries.all')
    filtered_df = filter_houses(
        df,
        governorate=selected_gov if selected_gov != all_text else None,
        damage_status=selected_damage if selected_damage != all_text else None,
        house_type=selected_type if selected_type != all_text else None
    )
    
    # فلترة المنازل التي لديها إحداثيات
    map_df = filtered_df[filtered_df['latitude'].notna() & filtered_df['longitude'].notna()]
    
    # عرض الإحصائيات
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(f"📋 {tm.t('map.total_houses')}", len(filtered_df))
    
    with col2:
        st.metric(f"📍 {tm.t('map.houses_on_map')}", len(map_df))
    
    with col3:
        missing = len(filtered_df) - len(map_df)
        st.metric(f"⚠️ {tm.t('map.without_coordinates')}", missing)
    
    st.markdown("---")
    
    # عرض الخريطة
    if len(map_df) > 0:
        st.markdown(f"### 🗺️ {tm.t('nav.map')}")
        
        # إنشاء الخريطة مع تمرير مدير الترجمات
        houses_map = create_houses_map(map_df, tm=tm)
        houses_map = add_map_legend(houses_map, tm=tm)
        
        # عرض الخريطة
        st_folium(houses_map, width=None, height=600)
        
        # معلومات إضافية
        st.markdown("---")
        st.markdown(f"### ℹ️ {tm.t('map.map_info')}")
        
        st.info(f"""
            **{tm.t('map.how_to_use')}:**
            - {tm.t('map.click_info')}
            - {tm.t('map.zoom_info')}
            - {tm.t('map.drag_info')}
            
            **{tm.t('map.colors')}:**
            - 🟢 {tm.t('map.green_light')}
            - 🟡 {tm.t('map.yellow_medium')}
            - 🔴 {tm.t('map.red_severe')}
        """)
    
    else:
        st.warning(f"⚠️ {tm.t('messages.no_coordinates')}")

else:
    st.error(f"⚠️ {tm.t('messages.no_data')}")

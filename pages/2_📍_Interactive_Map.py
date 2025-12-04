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

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# العنوان
st.markdown("""
    <h1 style='text-align: center; color: #0D47A1;'>
        📍 الخريطة التفاعلية
    </h1>
    <hr style='margin: 20px 0;'>
""", unsafe_allow_html=True)

# تحميل البيانات
@st.cache_data
def load_data():
    file_path = Path(__file__).parent.parent / DATA_PATH
    if not file_path.exists():
        st.error(f"⚠️ لم يتم العثور على ملف البيانات")
        return None
    return load_houses_data(str(file_path))

df = load_data()

if df is not None and not df.empty:
    
    # أدوات الفلترة
    st.markdown("### 🔍 فلترة النقاط")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # فلترة حسب المحافظة
        governorates = ['الكل'] + sorted(df['المحافظة'].dropna().unique().tolist())
        selected_gov = st.selectbox("📍 المحافظة", governorates)
    
    with col2:
        # فلتRة حسب حالة الضرر
        damage_statuses = ['الكل'] + sorted(df['حالة الضرر'].dropna().unique().tolist())
        selected_damage = st.selectbox("⚠️ حالة الضرر", damage_statuses)
    
    with col3:
        # فلترة حسب نوع المنزل
        house_types = ['الكل'] + sorted(df['نوع المنزل'].dropna().unique().tolist())
        selected_type = st.selectbox("🏘️ نوع المنزل", house_types)
    
    # تطبيق الفلاتر
    filtered_df = filter_houses(
        df,
        governorate=selected_gov if selected_gov != 'الكل' else None,
        damage_status=selected_damage if selected_damage != 'الكل' else None,
        house_type=selected_type if selected_type != 'الكل' else None
    )
    
    # فلترة المنازل التي لديها إحداثيات
    map_df = filtered_df[filtered_df['latitude'].notna() & filtered_df['longitude'].notna()]
    
    # عرض الإحصائيات
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📋 إجمالي المنازل", len(filtered_df))
    
    with col2:
        st.metric("📍 منازل على الخريطة", len(map_df))
    
    with col3:
        missing = len(filtered_df) - len(map_df)
        st.metric("⚠️ بدون إحداثيات", missing)
    
    st.markdown("---")
    
    # عرض الخريطة
    if len(map_df) > 0:
        st.markdown("### 🗺️ الخريطة")
        
        # إنشاء الخريطة
        houses_map = create_houses_map(map_df)
        houses_map = add_map_legend(houses_map)
        
        # عرض الخريطة
        st_folium(houses_map, width=None, height=600)
        
        # معلومات إضافية
        st.markdown("---")
        st.markdown("### ℹ️ معلومات الخريطة")
        
        st.info("""
            **كيفية استخدام الخريطة:**
            - انقر على أي نقطة لعرض معلومات المنزل
            - استخدم عجلة الماوس للتقريب والتبعيد
            - اسحب الخريطة للتنقل بين المناطق
            
            **الألوان:**
            - 🟢 الأخضر: ضرر خفيف
            - 🟡 الأصفر: ضرر متوسط
            - 🔴 الأحمر: ضرر شديد
        """)
    
    else:
        st.warning("⚠️ لا توجد منازل بإحداثيات جغرافية متاحة حسب الفلاتر المحددة")

else:
    st.error("⚠️ لا توجد بيانات لعرضها")

# الشريط الجانبي
with st.sidebar:
    st.markdown("### 📍 الخريطة التفاعلية")
    st.markdown("""
        هذه الصفحة تعرض جميع المنازل على خريطة تفاعلية.
        
        **الميزات:**
        - 🗺️ عرض جميع المواقع
        - 🎨 تلوين حسب حالة الضرر
        - 💬 نوافذ منبثقة بالمعلومات
        - 🔍 فلترة المواقع
        - 🖼️ عرض الصور
    """)

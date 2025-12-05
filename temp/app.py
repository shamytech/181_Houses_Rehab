"""
لوحة تحكم UNDP - إعادة تأهيل المنازل
الصفحة الرئيسية المعاد تصميمها - مع دعم ثنائي اللغة
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# إضافة مسار utils
sys.path.append(str(Path(__file__).parent))

from config import *
from utils.i18n import tm, create_language_switcher, get_dynamic_css
from utils.header import create_header
from utils.data_loader import (
    load_houses_data,
    load_sub_items,
    get_damage_status_counts,
    get_location_counts,
    get_house_type_counts,
    get_demographic_stats
)
from utils.costs import get_total_project_cost, calculate_all_houses_costs_simple, get_cost_statistics

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)

# CSS ديناميكي حسب اللغة
st.markdown(get_dynamic_css(tm), unsafe_allow_html=True)

# الهيدر الموحد
create_header(page_title=f"🏠 {tm.t('app_title')}")

# تحميل البيانات
@st.cache_data
def load_all_data():
    """تحميل جميع البيانات"""
    file_path = Path(DATA_PATH)
    if not file_path.exists():
        return None, None
    
    houses_df = load_houses_data(str(file_path))
    sub_items_df = load_sub_items(str(file_path))
    
    return houses_df, sub_items_df

df, sub_items_df = load_all_data()

# الشريط الجانبي
with st.sidebar:
    st.image("https://www.undp.org/themes/custom/undp/logo.svg", width=180)
    st.markdown("---")
    
    # مبدل اللغة
    create_language_switcher(tm)
    
    st.markdown("---")
    
    # معلومات المشروع
    st.markdown(f"### {tm.t('sections.key_indicators')}")
    st.markdown("""
        **UNDP 2025**  
        Rural Damascus Housing Rehabilitation
        
        ---
        
        📧 info@undp.org  
        📞 +XXX XXX XXXX
    """)

if df is not None and not df.empty:
    
    # القسم 1: البطاقات الصغيرة (صف واحد)
    total_houses = len(df)
    damage_counts = get_damage_status_counts(df)
    demo_stats = get_demographic_stats(df)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label=f"📋 {tm.t('metrics.total_applications')}",
            value=total_houses
        )
    
    with col2:
        light_damage = damage_counts.get('ضرر خفيف', 0)
        st.metric(
            label=f"✅ {tm.t('metrics.light_damage')}",
            value=light_damage,
            delta=f"{(light_damage/total_houses*100):.0f}%" if total_houses > 0 else "0%"
        )
    
    with col3:
        medium_damage = damage_counts.get('ضرر متوسط', 0)
        st.metric(
            label=f"⚠️ {tm.t('metrics.medium_damage')}",
            value=medium_damage,
            delta=f"{(medium_damage/total_houses*100):.0f}%" if total_houses > 0 else "0%"
        )
    
    with col4:
        severe_damage = damage_counts.get('ضرر شديد', 0)
        st.metric(
            label=f"🔴 {tm.t('metrics.severe_damage')}",
            value=severe_damage,
            delta=f"{(severe_damage/total_houses*100):.0f}%" if total_houses > 0 else "0%"
        )
    
    
    with col5:
        if sub_items_df is not None and not sub_items_df.empty:
            # حساب التكلفة الإجمالية مباشرة من البنود
            total_cost = get_total_project_cost(sub_items_df)
            st.metric(
                label=f"💰 {tm.t('metrics.estimated_cost')}",
                value=f"${total_cost/1000:.1f}K" if total_cost > 0 else "$0"
            )
        else:
            st.metric(
                label=f"💰 {tm.t('metrics.estimated_cost')}",
                value="-"
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # القسم 2: شبكة المخططات 2x2
    col1, col2 = st.columns(2)
    
    with col1:
        # مخطط توزيع الضرر
        st.markdown(f"#### {tm.t('sections.damage_distribution')}")
        
        if damage_counts:
            damage_df = pd.DataFrame(
                list(damage_counts.items()),
                columns=['Status', 'Count']
            )
            
            # ترجمة التسميات
            if tm.get_current_language() == 'en':
                damage_df['Status'] = damage_df['Status'].map({
                    'ضرر خفيف': 'Light Damage',
                    'ضرر متوسط': 'Medium Damage',
                    'ضرر شديد': 'Severe Damage'
                })
            
            color_map = {
                'ضرر خفيف': SUCCESS_GREEN,
                'Light Damage': SUCCESS_GREEN,
                'ضرر متوسط': WARNING_YELLOW,
                'Medium Damage': WARNING_YELLOW,
                'ضرر شديد': DANGER_RED,
                'Severe Damage': DANGER_RED
            }
            
            colors = [color_map.get(status, INFO_BLUE) for status in damage_df['Status']]
            
            fig = go.Figure(data=[go.Pie(
                labels=damage_df['Status'],
                values=damage_df['Count'],
                marker=dict(colors=colors),
                textinfo='label+percent',
                textposition='auto',
                hole=0.4
            )])
            
            fig.update_layout(
                showlegend=True,
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                font=dict(family="Tajawal" if tm.is_rtl() else "Inter", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="damage_chart")
    
    with col2:
        # مخطط أنواع المنازل
        st.markdown(f"#### {tm.t('sections.house_types')}")
        
        house_type_counts = get_house_type_counts(df)
        
        if house_type_counts:
            house_type_df = pd.DataFrame(
                list(house_type_counts.items()),
                columns=['Type', 'Count']
            )
            
            # ترجمة التسميات
            if tm.get_current_language() == 'en':
                house_type_df['Type'] = house_type_df['Type'].map({
                    'منزل مستقل': 'Detached House',
                    'شقة طابقية': 'Apartment'
                }).fillna(house_type_df['Type'])
            
            fig = go.Figure(data=[go.Pie(
                labels=house_type_df['Type'],
                values=house_type_df['Count'],
                marker=dict(colors=[PRIMARY_BLUE, PRIMARY_LIGHT, INFO_BLUE]),
                textinfo='label+percent',
                textposition='auto',
                hole=0.4
            )])
            
            fig.update_layout(
                showlegend=True,
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                font=dict(family="Tajawal" if tm.is_rtl() else "Inter", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="house_type_chart")
    
    # الصف الثاني من المخططات
    col1, col2 = st.columns(2)
    
    with col1:
        # التوزيع الجغرافي
        st.markdown(f"#### {tm.t('sections.geographic_distribution')}")
        
        location_counts = get_location_counts(df)
        
        if location_counts:
            location_df = pd.DataFrame(
                list(location_counts.items()),
                columns=['Location', 'Count']
            )
            
            fig = px.bar(
                location_df,
                x='Location',
                y='Count',
                text='Count',
                color='Count',
                color_continuous_scale='Blues'
            )
            
            fig.update_traces(textposition='outside', textfont_size=12)
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis_title="",
                yaxis_title="",
                font=dict(family="Tajawal" if tm.is_rtl() else "Inter", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="location_chart")
    
    with col2:
        # الديموغرافيا
        st.markdown(f"#### {tm.t('sections.demographics')}")
        
        demo_data = {
            'Category': ['Men', 'Women', 'Boys', 'Girls'] if tm.get_current_language() == 'en' else ['رجال', 'نساء', 'أطفال ذكور', 'أطفال إناث'],
            'Count': [
                demo_stats.get('الرجال', 0),
                demo_stats.get('النساء', 0),
                demo_stats.get('الأطفال الذكور', 0),
                demo_stats.get('الأطفال الإناث', 0)
            ]
        }
        
        demo_df = pd.DataFrame(demo_data)
        
        fig = px.bar(
            demo_df,
            x='Category',
            y='Count',
            text='Count',
            color='Category',
            color_discrete_sequence=[PRIMARY_BLUE, PRIMARY_LIGHT, SUCCESS_GREEN, INFO_BLUE]
        )
        
        fig.update_traces(textposition='outside', textfont_size=12)
        fig.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="",
            font=dict(family="Tajawal" if tm.is_rtl() else "Inter", size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="demo_chart")
    
    # معلومات إضافية مضغوطة
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(f"👨‍👩‍👧‍👦 {tm.t('metrics.total_families')}", demo_stats.get('إجمالي الأسر', 0))
    
    with col2:
        st.metric(f"👤 {tm.t('metrics.total_individuals')}", demo_stats.get('إجمالي الأفراد', 0))
    
    with col3:
        st.metric(f"♿ {tm.t('metrics.disabled_persons')}", demo_stats.get('ذوي الإعاقة', 0))
    
    with col4:
        st.metric(f"👴 {tm.t('metrics.elderly')}", demo_stats.get('كبار السن', 0))

else:
    st.error(tm.t('messages.no_data'))

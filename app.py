"""
لوحة تحكم UNDP - إعادة تأهيل المنازل
الصفحة الرئيسية - Dashboard المحسنة
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
from utils.data_loader import (
    load_houses_data,
    get_damage_status_counts,
    get_location_counts,
    get_house_type_counts,
    get_demographic_stats
)
from utils.boqs import load_boqs_data, calculate_total_cost, get_cost_by_category
from utils.data_loader import load_sub_items
from utils.charts import create_damage_pie_chart, create_house_type_pie_chart

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)

# CSS مخصص
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1976D2 0%, #0D47A1 100%); border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0; font-size: 2.5em;'>
            🏠 لوحة تحكم إعادة تأهيل المنازل
        </h1>
        <p style='color: #E3F2FD; margin: 10px 0 0 0; font-size: 1.2em;'>
            برنامج الأمم المتحدة الإنمائي (UNDP) - ريف دمشق
        </p>
    </div>
""", unsafe_allow_html=True)

# تحميل البيانات
@st.cache_data
def load_all_data():
    """تحميل جميع البيانات"""
    file_path = Path(DATA_PATH)
    if not file_path.exists():
        st.error(f"⚠️ لم يتم العثور على ملف البيانات: {DATA_PATH}")
        return None, None, None
    
    houses_df = load_houses_data(str(file_path))
    boqs_df = load_boqs_data(str(file_path))
    sub_items_df = load_sub_items(str(file_path))
    
    return houses_df, boqs_df, sub_items_df

df, boqs_df, sub_items_df = load_all_data()

if df is not None and not df.empty:
    
    # قسم 1: المقاييس الرئيسية في بطاقات ملونة
    st.markdown("## 📊 المؤشرات الرئيسية")
    
    # الصف الأول - مقاييس المنازل
    col1, col2, col3, col4 = st.columns(4)
    
    total_houses = len(df)
    damage_counts = get_damage_status_counts(df)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>📋</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{total_houses}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>إجمالي الطلبات</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        light_damage = damage_counts.get('ضرر خفيف', 0)
        percentage = (light_damage/total_houses*100) if total_houses > 0 else 0
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #66BB6A 0%, #4CAF50 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>✅</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{light_damage}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>ضرر خفيف ({percentage:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        medium_damage = damage_counts.get('ضرر متوسط', 0)
        percentage = (medium_damage/total_houses*100) if total_houses > 0 else 0
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FFCA28 0%, #FFC107 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>⚠️</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{medium_damage}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>ضرر متوسط ({percentage:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        severe_damage = damage_counts.get('ضرر شديد', 0)
        percentage = (severe_damage/total_houses*100) if total_houses > 0 else 0
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #EF5350 0%, #F44336 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🔴</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{severe_damage}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>ضرر شديد ({percentage:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # الصف الثاني - المقاييس الديموغرافية والتكاليف
    demo_stats = get_demographic_stats(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        families = demo_stats.get('إجمالي الأسر', 0)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #AB47BC 0%, #9C27B0 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>👨‍👩‍👧‍👦</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{families}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>إجمالي الأسر</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        individuals = demo_stats.get('إجمالي الأفراد', 0)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #26C6DA 0%, #00BCD4 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>👤</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{individuals}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>إجمالي الأفراد</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        disabled = demo_stats.get('ذوي الإعاقة', 0)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FF7043 0%, #FF5722 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>♿</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{disabled}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>ذوي الإعاقة</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # التكلفة الإجمالية من BOQs
        if boqs_df is not None and not boqs_df.empty and sub_items_df is not None and not sub_items_df.empty:
            total_cost = calculate_total_cost(sub_items_df, boqs_df)
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #26A69A 0%, #009688 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='font-size: 3em; margin-bottom: 10px;'>💰</div>
                <div style='font-size: 2.5em; font-weight: bold;'>${total_cost:,.0f}</div>
                <div style='font-size: 1.1em; opacity: 0.9;'>التكلفة التقديرية</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #78909C 0%, #607D8B 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='font-size: 3em; margin-bottom: 10px;'>💰</div>
                <div style='font-size: 2.5em; font-weight: bold;'>-</div>
                <div style='font-size: 1.1em; opacity: 0.9;'>التكلفة غير متوفرة</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # قسم 2: المخططات في تبويبات
    st.markdown("## 📈 التحليلات والإحصائيات")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 توزيع المنازل", "👥 الديموغرافيا", "📍 التوزيع الجغرافي", "💰 التكاليف"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### توزيع حالة الضرر")
            if damage_counts:
                fig = create_damage_pie_chart(damage_counts)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### أنواع المنازل")
            house_type_counts = get_house_type_counts(df)
            if house_type_counts:
                fig = create_house_type_pie_chart(house_type_counts)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### التوزيع الديموغرافي")
        
        demo_data = {
            'الفئة': ['الرجال', 'النساء', 'الأطفال الذكور', 'الأطفال الإناث'],
            'العدد': [
                demo_stats.get('الرجال', 0),
                demo_stats.get('النساء', 0),
                demo_stats.get('الأطفال الذكور', 0),
                demo_stats.get('الأطفال الإناث', 0)
            ]
        }
        
        demo_df = pd.DataFrame(demo_data)
        
        fig = px.bar(
            demo_df,
            x='الفئة',
            y='العدد',
            text='العدد',
            color='الفئة',
            color_discrete_sequence=[PRIMARY_BLUE, PRIMARY_LIGHT, SUCCESS_GREEN, INFO_BLUE]
        )
        
        fig.update_traces(textposition='outside', textfont_size=14)
        fig.update_layout(
            showlegend=False,
            height=450,
            xaxis_title="",
            yaxis_title="العدد",
            font=dict(family="Tajawal, sans-serif", size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # الحالات الخاصة
        st.markdown("### الحالات الخاصة")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            elderly = demo_stats.get('كبار السن', 0)
            st.metric("👴 كبار السن (60+)", elderly)
        
        with col2:
            disabled = demo_stats.get('ذوي الإعاقة', 0)
            st.metric("♿ ذوي الإعاقة", disabled)
        
        with col3:
            widows = df['عدد النساء الأرامل'].sum() if 'عدد النساء الأرامل' in df.columns else 0
            st.metric("👩 النساء الأرامل", int(widows))
    
    with tab3:
        st.markdown("### التوزيع الجغرافي")
        
        location_counts = get_location_counts(df)
        
        if location_counts:
            location_df = pd.DataFrame(
                list(location_counts.items()),
                columns=['المحافظة', 'العدد']
            )
            
            fig = px.bar(
                location_df,
                x='المحافظة',
                y='العدد',
                text='العدد',
                color='العدد',
                color_continuous_scale='Blues'
            )
            
            fig.update_traces(textposition='outside', textfont_size=14)
            fig.update_layout(
                showlegend=False,
                height=450,
                xaxis_title="",
                yaxis_title="عدد المنازل",
                font=dict(family="Tajawal, sans-serif", size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        if boqs_df is not None and not boqs_df.empty:
            st.markdown("### توزيع التكاليف")
            
            # التكلفة حسب الفئة
            if sub_items_df is not None and not sub_items_df.empty:
                cost_by_category = get_cost_by_category(sub_items_df, boqs_df)
            else:
                cost_by_category = {}
            
            if cost_by_category:
                cost_df = pd.DataFrame(
                    list(cost_by_category.items()),
                    columns=['الفئة', 'التكلفة (USD)']
                )
                
                cost_df = cost_df.sort_values('التكلفة (USD)', ascending=False)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(
                        cost_df,
                        x='التكلفة (USD)',
                        y='الفئة',
                        text='التكلفة (USD)',
                        orientation='h',
                        color='التكلفة (USD)',
                        color_continuous_scale='Greens'
                    )
                    
                    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside', textfont_size=13)
                    fig.update_layout(
                        showlegend=False,
                        height=400,
                        xaxis_title="التكلفة (USD)",
                        yaxis_title="",
                        font=dict(family="Tajawal, sans-serif", size=14)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### ملخص التكاليف")
                    for category, cost in cost_df.values:
                        percentage = (cost / cost_df['التكلفة (USD)'].sum() * 100)
                        st.markdown(f"""
                        <div style='background: {BG_CARD}; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-right: 4px solid {PRIMARY_BLUE};'>
                            <div style='font-weight: bold; margin-bottom: 5px;'>{category}</div>
                            <div style='font-size: 1.3em; color: {PRIMARY_BLUE};'>${cost:,.0f}</div>
                            <div style='font-size: 0.9em; color: {GRAY_700};'>{percentage:.1f}% من الإجمالي</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("⚠️ بيانات التكاليف غير متوفرة")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # قسم 3: معلومات المشروع
    st.markdown("## ℹ️ معلومات المشروع")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background: {BG_CARD}; padding: 25px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: {PRIMARY_DARK}; margin-top: 0;'>📍 المناطق المستهدفة</h3>
            <ul style='font-size: 1.1em; line-height: 1.8;'>
                <li>ريف دمشق</li>
                <li>عربين</li>
                <li>زملكا</li>
                <li>مناطق أخرى</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: {BG_CARD}; padding: 25px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: {PRIMARY_DARK}; margin-top: 0;'>📊 ملخص المشروع</h3>
            <ul style='font-size: 1.1em; line-height: 1.8;'>
                <li><strong>{total_houses}</strong> منزل قيد التقييم</li>
                <li><strong>{families}</strong> أسرة مستفيدة</li>
                <li><strong>{individuals}</strong> فرد</li>
                <li>مرحلة التنفيذ: <span style='color: {WARNING_YELLOW}; font-weight: bold;'>التقييم</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("⚠️ لا توجد بيانات لعرضها. يرجى التحقق من ملف Excel.")

# الشريط الجانبي
with st.sidebar:
    st.image("https://www.undp.org/themes/custom/undp/logo.svg", width=200)
    st.markdown("---")
    
    st.markdown("### 🏠 حول المشروع")
    st.markdown("""
        مشروع إعادة تأهيل المنازل المتضررة في ريف دمشق
        
        **الممول:** UNDP  
        **الفترة:** 2025
        
        **الأهداف:**
        - ✅ تقييم المنازل المتضررة
        - 📋 إعداد خطط إعادة التأهيل
        - 🔧 تنفيذ أعمال الترميم
        - 👨‍👩‍👧‍👦 دعم الأسر المتضررة
    """)
    
    st.markdown("---")
    
    st.markdown("### 📱 التواصل")
    st.markdown("""
        **للاستفسارات:**
        - 📧 info@undp.org
        - 📞 +XXX XXX XXXX
    """)

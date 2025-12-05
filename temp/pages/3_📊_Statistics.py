"""
صفحة الإحصائيات والتقارير
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# إضافة مسار المشروع
sys.path.append(str(Path(__file__).parent.parent))

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
from utils.i18n import tm, create_language_switcher, get_dynamic_css
from utils.header import create_header

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)

# CSS ديناميكي حسب اللغة
st.markdown(get_dynamic_css(tm), unsafe_allow_html=True)

# الهيدر الموحد
create_header(page_title="📊 الإحصائيات والتقارير")

# الشريط الجانبي
with st.sidebar:
    st.image("https://www.undp.org/themes/custom/undp/logo.svg", width=180)
    st.markdown("---")
    create_language_switcher(tm)
    st.markdown("---")
    st.markdown("### 📊 الإحصائيات والتقارير")
    st.markdown("""
        هذه الصفحة تعرض تحليلات شاملة للمشروع.
        
        **الأقسام:**
        - 👥 إحصائيات ديموغرافية
        - 🏠 إحصائيات المنازل
        - 📍 توزيع جغرافي
        - 📄 حالة الملكية
        - 🔧 تحليلات البنود
        - 📥 تصدير التقارير
    """)

# تحميل البيانات
@st.cache_data
def load_all_data():
    file_path = Path(__file__).parent.parent / DATA_PATH
    if not file_path.exists():
        return None, None, None
    
    houses = load_houses_data(str(file_path))
    main_items = load_main_items(str(file_path))
    sub_items = load_sub_items(str(file_path))
    
    return houses, main_items, sub_items

df, main_items_df, sub_items_df = load_all_data()

if df is not None and not df.empty:
    
    # قسم الإحصائيات الديموغرافية
    st.markdown("## 👥 الإحصائيات الديموغرافية")
    
    demo_stats = get_demographic_stats(df)
    
    # المقاييس الرئيسية
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👨‍👩‍👧‍👦 الأسر", demo_stats.get('إجمالي الأسر', 0))
    
    with col2:
        st.metric("👤 الأفراد", demo_stats.get('إجمالي الأفراد', 0))
    
    with col3:
        st.metric("👨 الرجال", demo_stats.get('الرجال', 0))
    
    with col4:
        st.metric("👩 النساء", demo_stats.get('النساء', 0))
    
    with col5:
        total_children = demo_stats.get('الأطفال الذكور', 0) + demo_stats.get('الأطفال الإناث', 0)
        st.metric("👶 الأطفال", total_children)
    
    # مخططات ديموغرافية
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### التوزيع الديموغرافي")
        fig = create_demographic_bar_chart(demo_stats)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### الحالات الخاصة")
        
        special_cases = {
            'ذوو الإعاقة': demo_stats.get('ذوي الإعاقة', 0),
            'كبار السن': demo_stats.get('كبار السن', 0),
            'النساء الأرامل': df['عدد النساء الأرامل'].sum() if 'عدد النساء الأرامل' in df.columns else 0,
            'النساء المطلقات': df['عدد النساء المطلقات'].sum() if 'عدد النساء المطلقات' in df.columns else 0
        }
        
        special_df = pd.DataFrame(
            list(special_cases.items()),
            columns=['الفئة', 'العدد']
        )
        
        fig = px.bar(
            special_df,
            x='الفئة',
            y='العدد',
            text='العدد',
            color='العدد',
            color_continuous_scale='Oranges'
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="",
            yaxis_title="العدد",
            font=dict(family="Cairo, sans-serif", size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # قسم إحصائيات المنازل
    st.markdown("## 🏠 إحصائيات المنازل")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### توزيع حالة الضرر")
        damage_counts = get_damage_status_counts(df)
        if damage_counts:
            fig = create_damage_pie_chart(damage_counts)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### أنواع المنازل")
        house_type_counts = get_house_type_counts(df)
        if house_type_counts:
            fig = create_house_type_pie_chart(house_type_counts)
            st.plotly_chart(fig, use_container_width=True)
    
    # التوزيع الجغرافي
    st.markdown("### 📍 التوزيع الجغرافي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### حسب المحافظة")
        location_counts = get_location_counts(df)
        if location_counts:
            fig = create_location_bar_chart(location_counts)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### حسب المنطقة")
        if 'المنطقة' in df.columns:
            region_counts = df['المنطقة'].value_counts().to_dict()
            region_df = pd.DataFrame(
                list(region_counts.items()),
                columns=['المنطقة', 'العدد']
            )
            
            fig = px.bar(
                region_df,
                x='المنطقة',
                y='العدد',
                text='العدد',
                color='العدد',
                color_continuous_scale='Greens'
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="",
                yaxis_title="عدد المنازل",
                font=dict(family="Cairo, sans-serif", size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # قسم إحصائيات الملكية
    st.markdown("## 📄 إحصائيات الملكية والإقامة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### حالة الإقامة")
        if 'حالة الاقامة في المنزل' in df.columns:
            residence_counts = df['حالة الاقامة في المنزل'].value_counts().to_dict()
            residence_df = pd.DataFrame(
                list(residence_counts.items()),
                columns=['الحالة', 'العدد']
            )
            
            fig = go.Figure(data=[go.Pie(
                labels=residence_df['الحالة'],
                values=residence_df['العدد'],
                textinfo='label+percent',
                textposition='auto'
            )])
            
            fig.update_layout(
                showlegend=True,
                height=400,
                font=dict(family="Cairo, sans-serif", size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### حالة الإقامة في المنطقة")
        if 'ما هي حالة إقامتك في المنطقة؟' in df.columns:
            status_counts = df['ما هي حالة إقامتك في المنطقة؟'].value_counts().to_dict()
            status_df = pd.DataFrame(
                list(status_counts.items()),
                columns=['الحالة', 'العدد']
            )
            
            fig = px.bar(
                status_df,
                x='الحالة',
                y='العدد',
                text='العدد',
                color='العدد',
                color_continuous_scale='Purples'
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="",
                yaxis_title="العدد",
                font=dict(family="Cairo, sans-serif", size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # قسم تحليلات البنود
    if main_items_df is not None and not main_items_df.empty:
        st.markdown("## 🔧 تحليلات البنود والأعمال")
        
        # البنود الرئيسية الأكثر شيوعاً
        if '_parent_index' in main_items_df.columns and 'البند الرئيسي' in main_items_df.columns:
            main_counts = main_items_df.groupby('البند الرئيسي').size().reset_index(name='العدد')
            main_counts = main_counts.sort_values('العدد', ascending=True)
            
            fig = px.bar(
                main_counts,
                x='العدد',
                y='البند الرئيسي',
                text='العدد',
                orientation='h',
                color='العدد',
                color_continuous_scale='Blues'
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="عدد المنازل",
                yaxis_title="",
                font=dict(family="Cairo, sans-serif", size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # زر التصدير
    st.markdown("---")
    st.markdown("### 📥 تصدير التقارير")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # تصدير ملخص الإحصائيات
        summary_data = {
            'المؤشر': list(demo_stats.keys()),
            'القيمة': list(demo_stats.values())
        }
        summary_df = pd.DataFrame(summary_data)
        
        csv = summary_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 تصدير ملخص الإحصائيات (CSV)",
            data=csv,
            file_name="statistics_summary.csv",
            mime="text/csv"
        )
    
    with col2:
        # تصدير التقرير الشامل
        from io import BytesIO
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # ملخص ديموغرافي
            summary_df.to_excel(writer, sheet_name='الملخص', index=False)
            
            # توزيع حالة الضرر
            if damage_counts:
                damage_df = pd.DataFrame(
                    list(damage_counts.items()),
                    columns=['حالة الضرر', 'العدد']
                )
                damage_df.to_excel(writer, sheet_name='حالة الضرر', index=False)
            
            # التوزيع الجغرافي
            if location_counts:
                location_df = pd.DataFrame(
                    list(location_counts.items()),
                    columns=['الموقع', 'العدد']
                )
                location_df.to_excel(writer, sheet_name='التوزيع الجغرافي', index=False)
        
        output.seek(0)
        
        st.download_button(
            label="📥 تصدير التقرير الشامل (Excel)",
            data=output,
            file_name="full_statistics_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.error("⚠️ لا توجد بيانات لعرضها")

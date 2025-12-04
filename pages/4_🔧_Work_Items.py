"""
صفحة البنود والأعمال المحسنة مع حسابات التكلفة
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# إضافة مسار المشروع
sys.path.append(str(Path(__file__).parent.parent))

from config import *
from utils.data_loader import load_main_items, load_sub_items
from utils.boqs import (
    load_boqs_with_mapping,
    calculate_all_houses_costs,
    calculate_house_cost,
    get_cost_statistics
)

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# العنوان
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #26A69A 0%, #009688 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>
            🔧 البنود والأعمال
        </h1>
        <p style='color: #E0F2F1; margin: 10px 0 0 0;'>
            تفاصيل أعمال إعادة التأهيل مع التكاليف التقديرية
        </p>
    </div>
""", unsafe_allow_html=True)

# تحميل البيانات
@st.cache_data
def load_data():
    file_path = Path(__file__).parent.parent / DATA_PATH
    if not file_path.exists():
        return None, None, None
    
    main_items = load_main_items(str(file_path))
    sub_items = load_sub_items(str(file_path))
    boqs = load_boqs_with_mapping(str(file_path))
    
    return main_items, sub_items, boqs

main_items_df, sub_items_df, boqs_df = load_data()

if main_items_df is not None and not main_items_df.empty:
    
    # حساب تكاليف جميع المنازل
    if sub_items_df is not None and boqs_df is not None and not boqs_df.empty:
        costs_df = calculate_all_houses_costs(sub_items_df, boqs_df)
        cost_stats = get_cost_statistics(costs_df)
    else:
        costs_df = None
        cost_stats = {}
    
    # ملخص البنود والتكاليف
    st.markdown("## 📊 ملخص المشروع")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_main = len(main_items_df)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #42A5F5 0%, #2196F3 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🔧</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{total_main}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>البنود الرئيسية</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if sub_items_df is not None:
            total_sub = len(sub_items_df)
        else:
            total_sub = 0
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #66BB6A 0%, #4CAF50 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>📝</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{total_sub}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>البنود الفرعية</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_houses = main_items_df['_parent_index'].nunique() if '_parent_index' in main_items_df.columns else 0
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FFA726 0%, #FF9800 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🏠</div>
            <div style='font-size: 2.5em; font-weight: bold;'>{unique_houses}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>المنازل</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_cost = cost_stats.get('الإجمالي', 0)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #26A69A 0%, #009688 100%); padding: 25px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <div style='font-size: 3em; margin-bottom: 10px;'>💰</div>
            <div style='font-size: 2.5em; font-weight: bold;'>${total_cost:,.0f}</div>
            <div style='font-size: 1.1em; opacity: 0.9;'>التكلفة الإجمالية</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # التبويبات
    tab1, tab2, tab3, tab4 = st.tabs(["📋 البنود الرئيسية", "📝 البنود الفرعية", "💰 التكاليف", "📊 التحليلات"])
    
    with tab1:
        st.markdown("### 🔧 البنود الرئيسية")
        
        # تجميع البنود الرئيسية
        if 'البند الرئيسي' in main_items_df.columns:
            main_summary = main_items_df.groupby('البند الرئيسي').agg({
                '_parent_index': 'count'
            }).reset_index()
            main_summary.columns = ['البند الرئيسي', 'عدد المنازل']
            main_summary = main_summary.sort_values('عدد المنازل', ascending=False)
            
            # عرض الجدول
            st.dataframe(
                main_summary,
                use_container_width=True,
                hide_index=True,
                height=350
            )
            
            # مخطط البنود الرئيسية
            st.markdown("#### 📊 توزيع البنود الرئيسية")
            
            fig = px.bar(
                main_summary,
                y='البند الرئيسي',
                x='عدد المنازل',
                text='عدد المنازل',
                orientation='h',
                color='عدد المنازل',
                color_continuous_scale='Teal'
            )
            
            fig.update_traces(textposition='outside', textfont_size=14)
            fig.update_layout(
                showlegend=False,
                height=500,
                xaxis_title="عدد المنازل",
                yaxis_title="",
                font=dict(family="Tajawal, sans-serif", size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 📝 البنود الفرعية")
        
        if sub_items_df is not None and not sub_items_df.empty:
            # فلترة حسب البند الرئيسي
            if 'البند الرئيسي' in sub_items_df.columns:
                main_items_list = ['الكل'] + sorted(sub_items_df['البند الرئيسي'].dropna().unique().tolist())
                selected_main_item = st.selectbox("🔍 اختر البند الرئيسي", main_items_list, key="main_filter")
                
                # فلترة البيانات
                if selected_main_item != 'الكل':
                    filtered_sub = sub_items_df[sub_items_df['البند الرئيسي'] == selected_main_item]
                else:
                    filtered_sub = sub_items_df
                
                # عرض الإحصائيات
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📝 عدد البنود", len(filtered_sub))
                
                with col2:
                    if 'الكمية' in filtered_sub.columns:
                        total_quantity = filtered_sub['الكمية'].sum()
                        st.metric("📊 إجمالي الكميات", f"{total_quantity:,.0f}")
                
                with col3:
                    unique_types = filtered_sub['البند الفرعي'].nunique() if 'البند الفرعي' in filtered_sub.columns else 0
                    st.metric("🔢 أنواع البنود", unique_types)
                
                # جدول البنود الفرعية
                if len(filtered_sub) > 0:
                    display_cols = []
                    if 'البند الرئيسي' in filtered_sub.columns:
                        display_cols.append('البند الرئيسي')
                    if 'البند الفرعي' in filtered_sub.columns:
                        display_cols.append('البند الفرعي')
                    if 'الكمية' in filtered_sub.columns:
                        display_cols.append('الكمية')
                    
                    if display_cols:
                        display_df = filtered_sub[display_cols].copy()
                        
                        st.markdown("#### جدول البنود الفرعية")
                        st.dataframe(
                            display_df,
                            use_container_width=True,
                            hide_index=True,
                            height=400
                        )
        else:
            st.info("لا توجد بيانات للبنود الفرعية")
    
    with tab3:
        st.markdown("### 💰 التكاليف التقديرية")
        
        if costs_df is not None and not costs_df.empty:
            # إحصائيات التكاليف
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_cost = cost_stats.get('المتوسط', 0)
                st.metric("📊 متوسط التكلفة", f"${avg_cost:,.0f}")
            
            with col2:
                min_cost = cost_stats.get('الأدنى', 0)
                st.metric("⬇️ أدنى تكلفة", f"${min_cost:,.0f}")
            
            with col3:
                max_cost = cost_stats.get('الأعلى', 0)
                st.metric("⬆️ أعلى تكلفة", f"${max_cost:,.0f}")
            
            with col4:
                houses_count = cost_stats.get('عدد المنازل', 0)
                st.metric("🏠 المنازل المقيّمة", houses_count)
            
            st.markdown("---")
            
            # جدول التكاليف
            st.markdown("#### جدول تكاليف المنازل")
            
            # ترتيب حسب الكلفة
            sorted_costs = costs_df.sort_values('التكلفة التقديرية (USD)', ascending=False)
            
            st.dataframe(
                sorted_costs,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # مخطط التكاليف
            st.markdown("#### 📊 توزيع التكاليف")
            
            fig = px.histogram(
                costs_df,
                x='التكلفة التقديرية (USD)',
                nbins=20,
                color_discrete_sequence=['#009688']
            )
            
            fig.update_layout(
                height=400,
                xaxis_title="التكلفة التقديرية (USD)",
                yaxis_title="عدد المنازل",
                font=dict(family="Tajawal, sans-serif", size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # تصدير التكاليف
            st.markdown("---")
            st.markdown("### 📥 تصدير البيانات")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = sorted_costs.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 تصدير التكاليف (CSV)",
                    data=csv,
                    file_name="houses_costs.csv",
                    mime="text/csv"
                )
            
            with col2:
                from io import BytesIO
                output = BytesIO()
                
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    sorted_costs.to_excel(writer, index=False, sheet_name='التكاليف')
                
                output.seek(0)
                
                st.download_button(
                    label="📥 تصدير التكاليف (Excel)",
                    data=output,
                    file_name="houses_costs.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.info("⚠️ بيانات التكاليف غير متوفرة. تأكد من وجود ورقة BOQs2 في ملف Excel.")
    
    with tab4:
        st.markdown("### 📊 التحليلات")
        
        if sub_items_df is not None and 'البند الفرعي' in sub_items_df.columns and 'الكمية' in sub_items_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # أكثر البنود طلباً
                st.markdown("#### أكثر البنود طلباً")
                
                top_items = sub_items_df.groupby('البند الفرعي').size().reset_index(name='عدد المنازل')
                top_items = top_items.sort_values('عدد المنازل', ascending=False).head(10)
                
                fig = px.bar(
                    top_items,
                    x='عدد المنازل',
                    y='البند الفرعي',
                    text='عدد المنازل',
                    orientation='h',
                    color='عدد المنازل',
                    color_continuous_scale='Purples'
                )
                
                fig.update_traces(textposition='outside', textfont_size=12)
                fig.update_layout(
                    showlegend=False,
                    height=500,
                    xaxis_title="عدد المنازل",
                    yaxis_title="",
                    font=dict(family="Tajawal, sans-serif", size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # أعلى الكميات
                st.markdown("#### أعلى الكميات")
                
                quantities = sub_items_df.groupby('البند الفرعي')['الكمية'].sum().reset_index()
                quantities = quantities.sort_values('الكمية', ascending=False).head(10)
                
                fig = px.bar(
                    quantities,
                    x='الكمية',
                    y='البند الفرعي',
                    text='الكمية',
                    orientation='h',
                    color='الكمية',
                    color_continuous_scale='Oranges'
                )
                
                fig.update_traces(textposition='outside', textfont_size=12)
                fig.update_layout(
                    showlegend=False,
                    height=500,
                    xaxis_title="الكمية الإجمالية",
                    yaxis_title="",
                    font=dict(family="Tajawal, sans-serif", size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)

else:
    st.error("⚠️ لا توجد بيانات للبنود الرئيسية")

# الشريط الجانبي
with st.sidebar:
    st.markdown("### 🔧 البنود والأعمال")
    st.markdown("""
        هذه الصفحة تعرض تفاصيل أعمال إعادة التأهيل مع التكاليف.
        
        **الأقسام:**
        - 📋 البنود الرئيسية
        - 📝 البنود الفرعية
        -💰 التكاليف التقديرية
        - 📊 التحليلات
        
        **المطابقة:**
        يتم مطابقة البنود تلقائياً مع جدول BOQs لحساب التكاليف.
    """)

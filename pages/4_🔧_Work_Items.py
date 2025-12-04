"""
صفحة البنود والأعمال
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

#ضافة مسار المشروع
sys.path.append(str(Path(__file__).parent.parent))

from config import *
from utils.data_loader import load_main_items, load_sub_items

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# العنوان
st.markdown("""
    <h1 style='text-align: center; color: #0D47A1;'>
        🔧 البنود والأعمال
    </h1>
    <hr style='margin: 20px 0;'>
""", unsafe_allow_html=True)

# تحميل البيانات
@st.cache_data
def load_data():
    file_path = Path(__file__).parent.parent / DATA_PATH
    if not file_path.exists():
        return None, None
    
    main_items = load_main_items(str(file_path))
    sub_items = load_sub_items(str(file_path))
    
    return main_items, sub_items

main_items_df, sub_items_df = load_data()

if main_items_df is not None and not main_items_df.empty:
    
    # ملخص البنود
    st.markdown("### 📋 ملخص البنود")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_main = len(main_items_df)
        st.metric("🔧 إجمالي البنود الرئيسية", total_main)
    
    with col2:
        if sub_items_df is not None:
            total_sub = len(sub_items_df)
            st.metric("📝 إجمالي البنود الفرعية", total_sub)
        else:
            st.metric("📝 إجمالي البنود الفرعية", 0)
    
    with col3:
        unique_houses = main_items_df['_parent_index'].nunique() if '_parent_index' in main_items_df.columns else 0
        st.metric("🏠 عدد المنازل", unique_houses)
    
    st.markdown("---")
    
    # جدول البنود الرئيسية
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
            height=300
        )
        
        # مخطط البنود الرئيسية
        st.markdown("#### 📊 توزيع البنود الرئيسية")
        
        import plotly.express as px
        
        fig = px.bar(
            main_summary,
            x='البند الرئيسي',
            y='عدد المنازل',
            text='عدد المنازل',
            color='عدد المنازل',
            color_continuous_scale='Blues'
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="",
            yaxis_title="عدد المنازل",
            font=dict(family="Cairo, sans-serif", size=14),
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # البنود الفرعية
    if sub_items_df is not None and not sub_items_df.empty:
        st.markdown("### 📝 البنود الفرعية")
        
        # فلترة حسب البند الرئيسي
        if 'البند الرئيسي' in sub_items_df.columns:
            main_items_list = ['الكل'] + sorted(sub_items_df['البند الرئيسي'].dropna().unique().tolist())
            selected_main_item = st.selectbox("🔍 اختر البند الرئيسي", main_items_list)
            
            # فلترة البيانات
            if selected_main_item != 'الكل':
                filtered_sub = sub_items_df[sub_items_df['البند الرئيسي'] == selected_main_item]
            else:
                filtered_sub = sub_items_df
            
            # عرض الإحصائيات
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📝 عدد البنود الفرعية", len(filtered_sub))
            
            with col2:
                if 'الكمية' in filtered_sub.columns:
                    total_quantity = filtered_sub['الكمية'].sum()
                    st.metric("📊 إجمالي الكميات", f"{total_quantity:,.0f}")
            
            # جدول البنود الفرعية
            if len(filtered_sub) > 0:
                
                # اختيار الأعمدة للعرض
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
                
                # عرض الصور التوضيحية
                st.markdown("---")
                st.markdown("### 📸 الصور التوضيحية للبنود")
                
                # عرض البنود مع صورها
                for idx, row in filtered_sub.iterrows():
                    sub_item_name = row.get('البند الفرعي', 'غير محدد')
                    quantity = row.get('الكمية', 'غير محدد')
                    image_url = row.get('صورة توضيحية للبند_URL', '')
                    
                    with st.expander(f"📝 {sub_item_name} (الكمية: {quantity})"):
                        
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.markdown(f"""
                            **البند الرئيسي:** {row.get('البند الرئيسي', 'غير محدد')}
                            
                            **البند الفرعي:** {sub_item_name}
                            
                            **الكمية:** {quantity}
                            """)
                        
                        with col2:
                            if image_url:
                                try:
                                    st.image(image_url, caption=f"صورة توضيحية - {sub_item_name}", use_container_width=True)
                                except:
                                    st.warning("لم يتم تحميل الصورة")
                            else:
                                st.info("لا توجد صورة توضيحية")
                
                # تصدير البيانات
                st.markdown("---")
                st.markdown("### 📥 تصدير البيانات")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # تصدير إلى CSV
                    csv = display_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 تصدير إلى CSV",
                        data=csv,
                        file_name=f"sub_items_{selected_main_item}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # تصدير إلى Excel
                    from io import BytesIO
                    output = BytesIO()
                    
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        display_df.to_excel(writer, index=False, sheet_name='البنود الفرعية')
                    
                    output.seek(0)
                    
                    st.download_button(
                        label="📥 تصدير إلى Excel",
                        data=output,
                        file_name=f"sub_items_{selected_main_item}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            else:
                st.info("لا توجد بنود فرعية لهذا البند الرئيسي")
    
    else:
        st.info("لا توجد بيانات للبنود الفرعية")
    
    # تحليلات إضافية
    st.markdown("---")
    st.markdown("### 📊 تحليلات إضافية")
    
    if sub_items_df is not None and 'البند الفرعي' in sub_items_df.columns and 'الكمية' in sub_items_df.columns:
        
        col1, col2 = st.columns(2)
        
        with col1:
            # أكثر البنود الفرعية طلباً
            st.markdown("#### أكثر البنود الفرعية طلباً")
            
            top_sub_items = sub_items_df.groupby('البند الفرعي').size().reset_index(name='عدد الطلبات')
            top_sub_items = top_sub_items.sort_values('عدد الطلبات', ascending=False).head(10)
            
            import plotly.express as px
            
            fig = px.bar(
                top_sub_items,
                x='عدد الطلبات',
                y='البند الفرعي',
                text='عدد الطلبات',
                orientation='h',
                color='عدد الطلبات',
                color_continuous_scale='Greens'
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=500,
                xaxis_title="عدد الطلبات",
                yaxis_title="",
                font=dict(family="Cairo, sans-serif", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # إجمالي الكميات حسب البند الفرعي
            st.markdown("#### إجمالي الكميات حسب البند")
            
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
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=500,
                xaxis_title="الكمية الإجمالية",
                yaxis_title="",
                font=dict(family="Cairo, sans-serif", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)

else:
    st.error("⚠️ لا توجد بيانات للبنود الرئيسية")

# الشريط الجانبي
with st.sidebar:
    st.markdown("### 🔧 البنود والأعمال")
    st.markdown("""
        هذه الصفحة تعرض تفاصيل أعمال إعادة التأهيل.
        
        **الميزات:**
        - 🔧 البنود الرئيسية
        - 📝 البنود الفرعية
        - 📸 الصور التوضيحية
        - 📊 التحليلات والإحصائيات
        - 📥 تصدير البيانات
    """)

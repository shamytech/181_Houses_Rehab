"""
صفحة المستفيدين مع نافذة منبثقة شاملة للتفاصيل
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from config import *
from utils.i18n import tm, create_language_switcher, get_dynamic_css
from utils.header import create_header
from utils.data_loader import (
    load_houses_data,
    load_main_items,
    load_sub_items,
    filter_houses,
    search_houses
)
from utils.beneficiary_modal import create_beneficiary_modal

st.set_page_config(**PAGE_CONFIG)
st.markdown(get_dynamic_css(tm), unsafe_allow_html=True)
create_header(page_title=f"👥 {tm.t('beneficiaries.title')}")

with st.sidebar:
    st.markdown("---")
    create_language_switcher(tm)


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
    # فلاتر البحث
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_term = st.text_input(f"🔎 {tm.t('beneficiaries.search')}", "", key="search")
    with col2:
        govs = [tm.t('beneficiaries.all')] + sorted(df['المحافظة'].dropna().unique().tolist())
        sel_gov = st.selectbox(f"📍 {tm.t('beneficiaries.filter_governorate')}", govs, key="gov")
    with col3:
        damages = [tm.t('beneficiaries.all')] + sorted(df['حالة الضرر'].dropna().unique().tolist())
        sel_damage = st.selectbox(f"⚠️ {tm.t('beneficiaries.filter_damage')}", damages, key="damage")
    with col4:
        types = [tm.t('beneficiaries.all')] + sorted(df['نوع المنزل'].dropna().unique().tolist())
        sel_type = st.selectbox(f"🏘️ {tm.t('beneficiaries.filter_house_type')}", types, key="type")
    
    # تطبيق الفلاتر
    all_text = tm.t('beneficiaries.all')
    filtered_df = df.copy()
    if search_term:
        filtered_df = search_houses(filtered_df, search_term)
    filtered_df = filter_houses(
        filtered_df,
        governorate=sel_gov if sel_gov != all_text else None,
        damage_status=sel_damage if sel_damage != all_text else None,
        house_type=sel_type if sel_type != all_text else None
    )
    
    # عنوان النتائج مع زر عرض التفاصيل
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 📊 {tm.t('beneficiaries.results')}: ({len(filtered_df)} {tm.t('beneficiaries.beneficiary')})")
    with col2:
        view_btn = st.button(f"👁️ {tm.t('buttons.view_details')}", type="primary", use_container_width=True)
    
    if len(filtered_df) > 0:
        # تحضير الجدول
        display_cols = ['الاسم الكامل', 'المحافظة', 'المنطقة', 'حالة الضرر', '_index']
        available = [c for c in display_cols if c in filtered_df.columns]
        display_df = filtered_df[available].copy()
        
        # عرض الجدول مع إمكانية التحديد
        selected = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        # تحديد المستفيد المختار
        selected_idx = None
        if selected and selected.selection and selected.selection.rows:
            selected_idx = selected.selection.rows[0]
        
        # فتح التفاصيل عند الضغط على الزر
        if view_btn:
            if selected_idx is not None:
                row_data = filtered_df.iloc[selected_idx]
            else:
                row_data = filtered_df.iloc[0]  # أول عنصر
            
            beneficiary_name = f"{row_data.get('الاسم الأول', '')} {row_data.get('اسم الأب', '')} {row_data.get('الكنية', '')}"
            
            @st.dialog(f"{tm.t('beneficiaries.title')}: {beneficiary_name}", width="large")
            def show_details():
                create_beneficiary_modal(row_data, main_items_df, sub_items_df)
            
            show_details()
    else:
        st.warning(tm.t('messages.no_data'))
else:
    st.error(tm.t('messages.no_data'))

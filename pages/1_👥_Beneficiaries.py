"""
صفحة المستفيدين مع نافذة منبثقة للتفاصيل
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# إضافة مسار المشروع
sys.path.append(str(Path(__file__).parent.parent))

from config import *
from utils.i18n import tm, create_language_switcher, get_dynamic_css
from utils.data_loader import (
    load_houses_data,
    load_main_items,
    load_sub_items,
    filter_houses,
    search_houses
)
from utils.boqs import (
    load_boqs_with_mapping,
    calculate_house_cost
)
from utils.image_utils import display_image_safe, create_image_gallery

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)
st.markdown(get_dynamic_css(tm), unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.image("https://www.undp.org/themes/custom/undp/logo.svg", width=180)
    st.markdown("---")
    create_language_switcher(tm)

# العنوان
direction = tm.get_direction()

st.markdown(f"""
    <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #26A69A 0%, #009688 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0; direction: {direction};'>
            👥 {tm.t('beneficiaries.title')}
        </h1>
    </div>
""", unsafe_allow_html=True)

# تحميل البيانات
@st.cache_data
def load_all_data():
    file_path = Path(__file__).parent.parent / DATA_PATH
    if not file_path.exists():
        return None, None, None
    
    houses = load_houses_data(str(file_path))
    main_items = load_main_items(str(file_path))
    sub_items = load_sub_items(str(file_path))
    boqs = load_boqs_with_mapping(str(file_path))
    
    return houses, main_items, sub_items, boqs

df, main_items_df, sub_items_df, boqs_df = load_all_data()

if df is not None and not df.empty:
    
    # أدوات البحث والفلترة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_term = st.text_input(
            f"🔎 {tm.t('beneficiaries.search')}",
            "",
            key="search_input"
        )
    
    with col2:
        governorates = [tm.t('beneficiaries.all')] + sorted(df['المحافظة'].dropna().unique().tolist())
        selected_gov = st.selectbox(
            f"📍 {tm.t('beneficiaries.filter_governorate')}",
            governorates,
            key="gov_filter"
        )
    
    with col3:
        damage_statuses = [tm.t('beneficiaries.all')] + sorted(df['حالة الضرر'].dropna().unique().tolist())
        selected_damage = st.selectbox(
            f"⚠️ {tm.t('beneficiaries.filter_damage')}",
            damage_statuses,
            key="damage_filter"
        )
    
    with col4:
        house_types = [tm.t('beneficiaries.all')] + sorted(df['نوع المنزل'].dropna().unique().tolist())
        selected_type = st.selectbox(
            f"🏘️ {tm.t('beneficiaries.filter_house_type')}",
            house_types,
            key="type_filter"
        )
    
    # تطبيق الف لاتر
    filtered_df = df.copy()
    
    if search_term:
        filtered_df = search_houses(filtered_df, search_term)
    
    all_text = tm.t('beneficiaries.all')
    filtered_df = filter_houses(
        filtered_df,
        governorate=selected_gov if selected_gov != all_text else None,
        damage_status=selected_damage if selected_damage != all_text else None,
        house_type=selected_type if selected_type != all_text else None
    )
    
    # عرض النتائج
    st.markdown(f"### 📋 {tm.t('beneficiaries.results')} ({len(filtered_df)} {tm.t('beneficiaries.beneficiary')})")
    
    if len(filtered_df) > 0:
        
        # إعداد الجدول
        display_cols = {
            'الاسم الكامل': tm.t('fields.full_name'),
            'المحافظة': tm.t('fields.governorate'),
            'المنطقة': tm.t('fields.district'),
            'حالة الضرر': tm.t('fields.damage_status'),
            'عدد أفراد الأسرة (بما فيهم مالك المنزل)': tm.t('fields.family_size'),
            '_index': 'ID'
        }
        
        # فلترة الأعمدة الموجودة
        available_cols = [col for col in display_cols.keys() if col in filtered_df.columns]
        display_df = filtered_df[available_cols].copy()
        
        # إعادة تسمية الأعمدة
        rename_map = {col: display_cols[col] for col in available_cols}
        display_df = display_df.rename(columns=rename_map)
        
        # عرض الجدول
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        st.markdown("---")
        
        # اختيار مستفيد لعرض التفاصيل
        st.markdown(f"### 📝 {tm.t('buttons.view_details')}")
        
        # قائمة منسدلة للاختيار
        beneficiary_options = {}
        for idx, row in filtered_df.iterrows():
            name = row.get('الاسم الكامل', 'غير محدد')
            house_idx = row.get('_index', idx)
            beneficiary_options[f"{name} (#{house_idx})"] = house_idx
        
        selected_beneficiary = st.selectbox(
            tm.t('beneficiaries.beneficiary'),
            options=list(beneficiary_options.keys()),
            key="beneficiary_select"
        )
        
        if selected_beneficiary and st.button(f"👁️ {tm.t('buttons.view_details')}", type="primary"):
            # الحصول على معرف المستفيد
            beneficiary_id = beneficiary_options[selected_beneficiary]
            
            # الحصول على بيانات المستفيد
            beneficiary_data = filtered_df[filtered_df['_index'] == beneficiary_id].iloc[0]
            
            # إنشاء نافذة منبثقة باستخدام dialog
            @st.dialog(f"{tm.t('modal.personal_info')} - {beneficiary_data.get('الاسم الكامل', '')}", width="large")
            def show_details():
                tabs = st.tabs([
                    f"📋 {tm.t('modal.personal_info')}",
                    f"📍 {tm.t('modal.address_info')}",
                    f"⚠️ {tm.t('modal.assessment')}",
                    f"📸 {tm.t('modal.photos')}",
                    f"💰 {tm.t('modal.work_items')}"
                ])
                
                with tabs[0]:  # معلومات شخصية
                    st.markdown("#### 👤 معلومات المالك")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        - **{tm.t('fields.full_name')}:** {beneficiary_data.get('الاسم الكامل', 'غير محدد')}
                        - **{tm.t('fields.gender')}:** {beneficiary_data.get('الجنس', 'غير محدد')}
                        - **{tm.t('fields.birth_date')}:** {beneficiary_data.get('تاريخ الميلاد كما هو مذكور في الهوية', 'غير محدد')}
                        - **{tm.t('fields.marital_status')}:** {beneficiary_data.get('الحالة الاجتماعية', 'غير محدد')}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        - **{tm.t('fields.id_type')}:** {beneficiary_data.get('نوع الوثيقة الشخصية', 'غير محدد')}
                        - **{tm.t('fields.id_number')}:** {beneficiary_data.get('رقم الوثيقة الشخصية (الرقم الوطني)', 'غير محدد')}
                        - **{tm.t('fields.phone')}:** {beneficiary_data.get('رقم الهاتف الرئيسي (واتساب إن أمكن)', 'غير محدد')}
                        """)
                    
                    st.markdown("#### 👨‍👩‍👧‍👦 معلومات الأسرة")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            tm.t('fields.family_size'),
                            beneficiary_data.get('عدد أفراد الأسرة (بما فيهم مالك المنزل)', 0)
                        )
                    
                    with col2:
                        st.metric(
                            "رجال",
                            beneficiary_data.get('عدد الرجال (العمر أكبر من 18 سنة)', 0)
                        )
                    
                    with col3:
                        st.metric(
                            "نساء",
                            beneficiary_data.get('عدد النساء (العمر أكبر من 18 سنة)', 0)
                        )
                    
                    with col4:
                        children = int(beneficiary_data.get('عدد الأطفال الذكور (دون سن 12 سنة)', 0)) + \
                                  int(beneficiary_data.get('عدد الأطفال الإناث (دون سن 12 سنة)', 0))
                        st.metric("أطفال", children)
                
                with tabs[1]:  # معلومات العنوان
                    st.markdown("#### 📍 الموقع")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        - **{tm.t('fields.governorate')}:** {beneficiary_data.get('المحافظة', 'غير محدد')}
                        - **{tm.t('fields.district')}:** {beneficiary_data.get('المنطقة', 'غير محدد')}
                        - **{tm.t('fields.subdistrict')}:** {beneficiary_data.get('الناحية', 'غير محدد')}
                        - **{tm.t('fields.village')}:** {beneficiary_data.get('القرية', 'غير محدد')}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        - **{tm.t('fields.address')}:** {beneficiary_data.get('عنوان المنزل الكامل', 'غير محدد')}
                        """)
                        
                        lat = beneficiary_data.get('latitude')
                        lon = beneficiary_data.get('longitude')
                        
                        if pd.notna(lat) and pd.notna(lon):
                            st.markdown(f"**GPS:** {lat}, {lon}")
                
                with tabs[2]:  # التقييم
                    st.markdown("#### ⚠️ حالة الضرر")
                    
                    damage_status = beneficiary_data.get('حالة الضرر', 'غير محدد')
                    status_color = DAMAGE_STATUS.get(damage_status, {}).get('color', INFO_BLUE)
                    
                    st.markdown(f"""
                    <div style='background: {status_color}; color: white; padding: 15px; border-radius: 8px; text-align: center; font-size: 1.3em; font-weight: bold;'>
                        {damage_status}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        - **{tm.t('fields.house_type')}:** {beneficiary_data.get('نوع المنزل', 'غير محدد')}
                        - **{tm.t('fields.rooms')}:** {beneficiary_data.get('عدد الغرف (بما فيها الصالون)', 'غير محدد')}
                        - **{tm.t('fields.area')}:** {beneficiary_data.get('مساحة المنزل بالمتر المربع', 'غير محدد')} م²
                        - **{tm.t('fields.floor')}:** {beneficiary_data.get('رقم الطابق الذي يقع فيه المنزل', 'غير محدد')}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        - **الجدران الخارجية:** {beneficiary_data.get('هل يملك المنزل أو الشقة جدرانًا خارجية سليمة ولا يحتاج إلى أعمال بناء (بلوك) خارجية؟', 'غير محدد')}
                        - **الجدران الداخلية:** {beneficiary_data.get('هل يملك المنزل أو الشقة جدرانًا داخلية مكتملة ولا يحتاج إلى أعمال بناء (بلوك) داخلية؟', 'غير محدد')}
                        - **السقف:** {beneficiary_data.get('هل يملك المنزل أو الشقة سقفًا وسلالم (أدراج) سليمة؟', 'غير محدد')}
                        - **المرافق:** {beneficiary_data.get('هل المرافق (المياه والصرف) عاملة أم مجرد بناء؟', 'غير محدد')}
                        """)
                
                with tabs[3]:  # الصور
                    st.markdown(f"#### 📸 {tm.t('modal.photos')}")
                    
                    # جمع روابط الصور
                    image_data = [
                        ('صورة الواجهة الأمامية للمنزل_URL', 'الواجهة الأمامية'),
                        ('صورة للمنزل من الداخل_URL', 'من الداخل'),
                        ('صورة توضح حالة الجدران_URL', 'الجدران'),
                        ('صورة توضح حالة الأعمدة_URL', 'الأعمدة'),
                        ('صورة توضح حالة السقف_URL', 'السقف'),
                        ('صورة توضح حالة المرافق (المطبخ)_URL', 'المطبخ'),
                        ('صورة توضح حالة المرافق (الحمام)_URL', 'الحمام'),
                        ('صورة توضح حالة المرافق (التواليت)_URL', 'التواليت')
                    ]
                    
                    image_urls = [beneficiary_data.get(col, '') for col, _ in image_data if beneficiary_data.get(col, '')]
                    captions = [caption for col, caption in image_data if beneficiary_data.get(col, '')]
                    
                    if image_urls:
                        create_image_gallery(image_urls, captions, columns=3, max_width=500)
                    else:
                        st.info("لا توجد صور متوفرة")
                
                with tabs[4]:  # البنود والتكاليف
                    st.markdown(f"#### 💰 {tm.t('modal.work_items')}")
                    
                    if sub_items_df is not None and boqs_df is not None:
                        # حساب تكلفة المنزل
                        cost_info = calculate_house_cost(beneficiary_id, sub_items_df, boqs_df)
                        
                        # عرض التكلفة الإجمالية
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #26A69A 0%, #009688 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
                            <h2 style='margin: 0; color: white;'>${cost_info['total_cost']:,.2f}</h2>
                            <p style='margin: 5px 0 0 0; font-size: 0.9em;'>{tm.t('fields.estimated_cost')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # جدول البنود
                        if cost_info['items']:
                            items_df = pd.DataFrame(cost_info['items'])
                            
                            st.dataframe(
                                items_df[['البند', 'الكمية', 'السعر الإفرادي', 'التكلفة']],
                                use_container_width=True,
                                hide_index=True
                            )
                        else:
                            st.info("لا توجد بنود متوفرة لهذا المنزل")
                    else:
                        st.warning("بيانات التكلفة غير متوفرة")
            
            # عرض النافذة
            show_details()
    
    else:
        st.warning(f"⚠️ {tm.t('messages.no_data')}")

else:
    st.error(tm.t('messages.no_data'))

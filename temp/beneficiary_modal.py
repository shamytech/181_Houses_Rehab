"""
نافذة منبثقة شاملة لعرض تفاصيل المستفيد
"""
import streamlit as st
import pandas as pd
from utils.i18n import tm


def get_direction_style():
    """الحصول على نمط الاتجاه حسب اللغة"""
    if tm.is_rtl():
        return "direction: rtl; text-align: right;"
    return "direction: ltr; text-align: left;"


def display_field(label: str, value: any, icon: str = "•"):
    """عرض حقل نصي مع أيقونة"""
    direction = get_direction_style()
    if pd.notna(value) and str(value).strip():
        st.markdown(f"<div style='{direction}'><strong>{icon} {label}:</strong> {value}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='{direction}'><strong>{icon} {label}:</strong> {tm.t('messages.no_data')}</div>", unsafe_allow_html=True)


def display_image_with_rotate(url: str, label: str, key: str, width: int = 300):
    """عرض صورة مع زر تدوير يظهر عند hover فقط"""
    if pd.notna(url) and url:
        # تحديد حالة التدوير
        rotation_key = f"rotation_{key}"
        if rotation_key not in st.session_state:
            st.session_state[rotation_key] = 0
        
        rotation = st.session_state[rotation_key]
        
        # عرض الصورة
        st.markdown(f"""
            <style>
                .img-{key} {{
                    max-width: {width}px;
                    transform: rotate({rotation}deg);
                    transition: transform 0.3s ease;
                    border-radius: 8px;
                    display: block;
                    margin: 0 auto;
                }}
            </style>
            <img src="{url}" alt="{label}" class="img-{key}">
        """, unsafe_allow_html=True)
        
        # زر التدوير
        if st.button(f"🔄 {tm.t('buttons.rotate')}", key=f"btn_{key}", help=tm.t('buttons.rotate') + " 90°"):
            st.session_state[rotation_key] = (st.session_state[rotation_key] + 90) % 360
    else:
        st.info(f"📷 {label}: {tm.t('messages.no_data')}")


def display_image_field(label: str, url: str, icon: str = "📄"):
    """عرض حقل صورة - للتوافق مع الكود القديم"""
    if pd.notna(url) and url:
        st.markdown(f"**{icon} {label}**")
        try:
            st.image(url, use_container_width=True)
        except:
            st.info(f"🔗 {url}")
    else:
        st.info(f"{icon} {label}: {tm.t('messages.no_data')}")


def create_personal_info_tab(row):
    """تبويب المعلومات الشخصية"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>👤 {tm.t('modal.personal_info')}</h3>", unsafe_allow_html=True)
    
    # القسم الأول: المعلومات الأساسية
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h4 style='{direction}'>📝 {tm.t('modal.basic_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.first_name'), row.get('الاسم الأول'), "📝")
        display_field(tm.t('fields.father_name'), row.get('اسم الأب'), "👨")
        display_field(tm.t('fields.last_name'), row.get('الكنية'), "📛")
        display_field(tm.t('fields.mother_name'), row.get('اسم الأم كما هو مذكور في الهوية'), "👩")
        
    with col2:
        st.markdown(f"<h4 style='{direction}'>ℹ️ {tm.t('modal.additional_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.gender'), row.get('الجنس'), "⚧")
        display_field(tm.t('fields.birth_date'), row.get('تاريخ الميلاد كما هو مذكور في الهوية'), "📅")
        display_field(tm.t('fields.marital_status'), row.get('الحالة الاجتماعية'), "💍")
        display_field(tm.t('fields.spouse_name'), row.get('الاسم الثلاثي للزوج أو الزوجة (إن وجد)'), "👫")
    
    # القسم الثاني: معلومات الوثيقة
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h4 style='{direction}'>🆔 {tm.t('modal.document_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.id_type'), row.get('نوع الوثيقة الشخصية'), "📋")
        display_field(tm.t('fields.id_number'), row.get('رقم الوثيقة الشخصية (الرقم الوطني)'), "🔢")
    
    with col2:
        st.markdown(f"<h4 style='{direction}'>📞 {tm.t('modal.contact_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.phone'), row.get('رقم الهاتف الرئيسي (واتساب إن أمكن)'), "📱")
        display_field(tm.t('fields.phone_alt'), row.get('رقم هاتف بديل (إضافي)'), "📞")
    
    # القسم الثالث: صور الوثيقة بجانب بعضها
    st.markdown("---")
    st.markdown(f"<h3 style='{direction}'>📸 {tm.t('modal.id_photos')}</h3>", unsafe_allow_html=True)
    
    front_url = row.get('صورة الوثيقة الشخصية (الوجه الأول)_URL')
    back_url = row.get('صورة الوثيقة الشخصية (الوجه الثاني)_URL')
    
    # عرض الصور بجانب بعضها
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**🪪 {tm.t('fields.id_photo_front')}**")
        display_image_with_rotate(front_url, tm.t('fields.id_photo_front'), "id_front", width=300)
    
    with col2:
        st.markdown(f"**🪪 {tm.t('fields.id_photo_back')}**")
        display_image_with_rotate(back_url, tm.t('fields.id_photo_back'), "id_back", width=300)
    
    # القسم الرابع: معلومات صحية
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>🏥 {tm.t('modal.health_info')}</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        display_field(tm.t('fields.disability'), row.get('هل مالك المنزل من الأشخاص ذوي الإعاقة؟'), "♿")
    with col2:
        display_field(tm.t('fields.chronic_diseases'), row.get('هل تعاني من أمراض مزمنة؟'), "💊")


def create_family_info_tab(row):
    """تبويب معلومات الأسرة"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>👨‍👩‍👧‍👦 {tm.t('modal.family_info')}</h3>", unsafe_allow_html=True)
    
    # معلومات عامة
    col1, col2, col3 = st.columns(3)
    with col1:
        display_field(tm.t('fields.families_in_house'), row.get('عدد العائلات المقيمة في نفس المنزل'), "🏠")
    with col2:
        display_field(tm.t('fields.family_size'), row.get('عدد أفراد الأسرة (بما فيهم مالك المنزل)'), "👥")
    with col3:
        display_field(tm.t('fields.family_type'), row.get('نوع معيل الأسرة'), "💼")
    
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>📊 {tm.t('modal.family_distribution')}</h4>", unsafe_allow_html=True)
    
    # الكبار
    col1, col2 = st.columns(2)
    with col1:
        display_field(tm.t('fields.men') + " (+18)", row.get('عدد الرجال (العمر أكبر من 18 سنة)'), "👨")
        display_field(tm.t('fields.boys'), row.get('عدد الشباب الذكور (من 12 إلى 17 سنة)'), "👦")
        display_field(tm.t('fields.child_boys'), row.get('عدد الأطفال الذكور (دون سن 12 سنة)'), "👶")
    
    with col2:
        display_field(tm.t('fields.women') + " (+18)", row.get('عدد النساء (العمر أكبر من 18 سنة)'), "👩")
        display_field(tm.t('fields.girls'), row.get('عدد الفتيات الإناث (من 12 إلى 17 سنة)'), "👧")
        display_field(tm.t('fields.child_girls'), row.get('عدد الأطفال الإناث (دون سن 12 سنة)'), "👶")
    
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>🎯 {tm.t('modal.special_categories')}</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        display_field(tm.t('fields.elderly_count'), row.get('عدد أفراد الأسرة من كبار السن (60 سنة فأكثر)'), "👴")
        display_field(tm.t('fields.disabled_count'), row.get('عدد أفراد الأسرة من ذوي الإعاقة'), "♿")
    
    with col2:
        display_field(tm.t('fields.nursing_mothers'), row.get('عدد النساء المرضعات'), "🤱")
        display_field(tm.t('fields.pregnant_women'), row.get('عدد النساء الحوامل'), "🤰")
    
    with col3:
        display_field(tm.t('fields.divorced_women'), row.get('عدد النساء المطلقات'), "💔")
        display_field(tm.t('fields.widowed_women'), row.get('عدد النساء الأرامل'), "🖤")
        display_field(tm.t('fields.separated_children'), row.get('عدد الأطفال المنفصلين عن ذويهم'), "👶")
    
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>💰 {tm.t('modal.economic_info')}</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        display_field(tm.t('fields.income_source'), row.get('ما هو مصدر الدخل الرئيسي للأسرة؟'), "💵")
    with col2:
        display_field(tm.t('fields.working_members'), row.get('عدد الأفراد العاملين في الأسرة'), "👷")


def create_address_tab(row):
    """تبويب معلومات العنوان"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>📍 {tm.t('modal.address_info')}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        display_field(tm.t('fields.governorate'), row.get('المحافظة'), "🏛️")
        display_field(tm.t('fields.district'), row.get('المنطقة'), "🏘️")
        display_field(tm.t('fields.subdistrict'), row.get('الناحية'), "📍")
        display_field(tm.t('fields.village'), row.get('القرية'), "🏡")
    
    with col2:
        display_field(tm.t('fields.detailed_address'), row.get('العنوان التفصيلي لمكان السكن الحالي'), "🗺️")
        display_field(tm.t('fields.full_address'), row.get('عنوان المنزل الكامل'), "📮")
        display_field(tm.t('fields.residence_status'), row.get('ما هي حالة إقامتك في المنطقة؟'), "🏠")
    
    # إحداثيات GPS
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>🌍 {tm.t('modal.gps_coordinates')}</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        display_field(tm.t('fields.latitude'), row.get('_إحداثيات الموقع الجغرافي للمنزل (GPS)_latitude'), "🧭")
    with col2:
        display_field(tm.t('fields.longitude'), row.get('_إحداثيات الموقع الجغرافي للمنزل (GPS)_longitude'), "🧭")
    
    # حالة الإقامة
    st.markdown("---")
    display_field(tm.t('fields.residence_status'), row.get('حالة الاقامة في المنزل'), "🏚️")


def create_house_info_tab(row):
    """تبويب معلومات المنزل"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>🏠 {tm.t('modal.house_info')}</h3>", unsafe_allow_html=True)
    
    # معلومات أساسية
    col1, col2, col3 = st.columns(3)
    with col1:
        display_field(tm.t('fields.house_type'), row.get('نوع المنزل'), "🏘️")
        display_field(tm.t('fields.rooms'), row.get('عدد الغرف (بما فيها الصالون)'), "🛏️")
    with col2:
        display_field(tm.t('fields.floor'), row.get('رقم الطابق الذي يقع فيه المنزل'), "🏢")
        area = row.get('مساحة المنزل بالمتر المربع')
        if pd.notna(area):
            display_field(tm.t('fields.area'), f"{area} m²", "📐")
        else:
            display_field(tm.t('fields.area'), None, "📐")
    with col3:
        display_field(tm.t('fields.damage_status'), row.get('حالة الضرر'), "⚠️")
    
    # وثائق الملكية
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>📄 {tm.t('modal.ownership_documents')}</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        display_field(tm.t('fields.ownership_document'), row.get('هل لديك وثيقة اثبات ملكية حديث؟'), "📋")
        display_field(tm.t('fields.ownership_type'), row.get('نوع وثيقة الملكية'), "📑")
    with col2:
        display_field(tm.t('fields.ownership_date'), row.get('تاريخ إصدار وثيقة الملكية'), "📅")
    
    # صورة وثيقة الملكية
    ownership_url = row.get('صورة وثيقة الملكية_URL')
    if pd.notna(ownership_url) and ownership_url:
        st.markdown(f"**📸 {tm.t('modal.ownership_document')}**")
        try:
            st.image(ownership_url, use_container_width=True)
        except:
            st.info(f"🔗 {ownership_url}")
    
    # حالة المنزل
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>🔍 {tm.t('modal.house_condition')}</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        display_field(tm.t('fields.external_walls'), row.get('هل يملك المنزل أو الشقة جدرانًا خارجية سليمة ولا يحتاج إلى أعمال بناء (بلوك) خارجية؟'), "🧱")
        display_field(tm.t('fields.internal_walls'), row.get('هل يملك المنزل أو الشقة جدرانًا داخلية مكتملة ولا يحتاج إلى أعمال بناء (بلوك) داخلية؟'), "🏗️")
        display_field(tm.t('fields.roof'), row.get('هل يملك المنزل أو الشقة سقفًا وسلالم (أدراج) سليمة؟'), "🏚️")
    
    with col2:
        display_field(tm.t('fields.building_damage'), row.get('هل توجد أية أضرار إنشائية في المنزل أو الشقة؟'), "⚠️")
        display_field(tm.t('fields.facilities'), row.get('هل المرافق (المياه والصرف) عاملة أم مجرد بناء؟'), "🚰")
        display_field(tm.t('fields.sewerage'), row.get('هل المنزل موصول بنظام صرف صحي أو حفرة فنية؟'), "🚽")
    
    # وصف الضرر
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>📝 {tm.t('modal.damage_description')}</h4>", unsafe_allow_html=True)
    damage_desc = row.get('وصف حالة الضرر من وجهة نظرك كمالك للمنزل')
    if pd.notna(damage_desc) and str(damage_desc).strip():
        st.info(damage_desc)
    else:
        st.info(tm.t('messages.no_data'))


def create_photos_tab(row):
    """تبويب صور المنزل"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>📸 {tm.t('modal.photos')}</h3>", unsafe_allow_html=True)
    
    # الواجهة الأمامية
    # st.markdown(f"#### 🏠 {tm.t('fields.front_view')}")
    display_image_field(tm.t('fields.front_view'), row.get('صورة الواجهة الأمامية للمنزل_URL'), "🏠")
    
    st.markdown("---")
    
    # من الداخل
    # st.markdown(f"#### 🪟 {tm.t('fields.inside_view')}")
    display_image_field(tm.t('fields.inside_view'), row.get('صورة للمنزل من الداخل_URL'), "🏠")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # st.markdown(f"#### 🧱 {tm.t('fields.walls')}")
        display_image_field(tm.t('fields.walls'), row.get('صورة توضح حالة الجدران_URL'), "🧱")
        
        # st.markdown(f"#### 🏗️ {tm.t('fields.columns')}")
        display_image_field(tm.t('fields.columns'), row.get('صورة توضح حالة الأعمدة_URL'), "🏗️")
        
        # st.markdown(f"#### 🏚️ {tm.t('fields.roof')}")
        display_image_field(tm.t('fields.roof'), row.get('صورة توضح حالة السقف_URL'), "🏚️")
    
    with col2:
        # st.markdown(f"#### 🍳 {tm.t('fields.kitchen')}")
        display_image_field(tm.t('fields.kitchen'), row.get('صورة توضح حالة المرافق (المطبخ)_URL'), "🍳")
        
        # st.markdown(f"#### 🚿 {tm.t('fields.bathroom')}")
        display_image_field(tm.t('fields.bathroom'), row.get('صورة توضح حالة المرافق (الحمام)_URL'), "🚿")
        
        # st.markdown(f"#### 🚽 {tm.t('fields.toilet')}")
        display_image_field(tm.t('fields.toilet'), row.get('صورة توضح حالة المرافق (التواليت)_URL'), "🚽")



def create_costs_tab(row, sub_items_df):
    """تبويب التكاليف مع جدول تفاعلي وصور ديناميكية"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>💰 {tm.t('modal.costs_and_items')}</h3>", unsafe_allow_html=True)
    
    if sub_items_df is None or sub_items_df.empty:
        st.warning(tm.t('messages.no_data'))
        return
    
    # الحصول على index المستفيد
    beneficiary_index = row.get('_index')
    
    # فلترة البنود الخاصة بهذا المستفيد
    if '_parent_index' in sub_items_df.columns:
        house_items = sub_items_df[sub_items_df['_parent_index'] == beneficiary_index].copy()
    else:
        st.warning(tm.t('messages.no_data'))
        return
    
    if house_items.empty:
        st.info(tm.t('messages.no_data'))
        return
    
    # حساب الإجمالي
    total_cost = 0
    if 'الإجمالي' in house_items.columns:
        total_cost = house_items['الإجمالي'].sum()
    elif 'Total' in house_items.columns:
        total_cost = house_items['Total'].sum()
    
    # 1. بطاقة التكلفة الإجمالية
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #009688, #00796B); 
                    color: white; padding: 20px; border-radius: 10px; 
                    text-align: center; margin-bottom: 20px;'>
            <h2 style='margin: 0; color: white;'>${total_cost:,.2f}</h2>
            <p style='margin: 5px 0 0 0;'>{tm.t('modal.total_cost')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. جدول البنود
    st.markdown(f"<h4 style='{direction}'>� {tm.t('modal.items_details')} ({len(house_items)} {tm.t('modal.items')})</h4>", unsafe_allow_html=True)
    
    # تحضير البيانات للجدول
    display_cols = ['البند الرئيسي', 'البند الفرعي', 'الكمية', 'السعر الإفرادي', 'الإجمالي']
    available_cols = [c for c in display_cols if c in house_items.columns]
    
    if not available_cols:
        st.warning(tm.t('messages.no_data'))
        return
    
    # إضافة عمود الصورة للتتبع
    house_items_display = house_items.reset_index(drop=True)
    
    # عرض الجدول
    # استخدام session_state لتتبع الصف المحدد
    if 'selected_item_row' not in st.session_state:
        st.session_state.selected_item_row = 0
    
    # عرض الجدول
    st.dataframe(
        house_items_display[available_cols],
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    # 3. صورة البند - تتغير حسب التمرير
    st.markdown("---")
    
    # استخدام selectbox لاختيار البند وعرض صورته
    item_options = [f"{row.get('البند الرئيسي', tm.t('modal.not_specified'))} - {row.get('البند الفرعي', tm.t('modal.not_specified'))}" 
                    for _, row in house_items_display.iterrows()]
    
    if item_options:
        selected_item_label = st.selectbox(
            f"🔧 {tm.t('modal.item_photo')}",
            options=item_options,
            index=0,
            key="item_selector"
        )
        
        # الحصول على index البند المحدد
        selected_idx = item_options.index(selected_item_label)
        
        # عرض تفاصيل البند المحدد
        selected_item = house_items_display.iloc[selected_idx]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"📦 {tm.t('modal.quantity')}", f"{selected_item.get('الكمية', 0)}")
        with col2:
            unit_price = selected_item.get('السعر الإفرادي', 0)
            st.metric(f"💵 {tm.t('modal.unit_price')}", f"${unit_price:,.2f}" if pd.notna(unit_price) else "-")
        with col3:
            total = selected_item.get('الإجمالي', 0)
            st.metric(f"💰 {tm.t('modal.total')}", f"${total:,.2f}" if pd.notna(total) else "-")
        with col4:
            st.metric("📸", tm.t('modal.item_photo'))
        
        # عرض صورة البند
        item_photo_url = selected_item.get('صورة توضيحية للبند_URL', '')
        
        if pd.notna(item_photo_url) and item_photo_url:
            st.markdown("---")
            try:
                st.image(item_photo_url, use_container_width=True, caption=selected_item_label)
            except:
                st.info(f"🔗 {item_photo_url}")
        else:
            st.info(f"� {tm.t('messages.no_data')}")



def create_assessment_tab(row):
    """تبويب التقييم"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>🔍 {tm.t('modal.assessment')}</h3>", unsafe_allow_html=True)
    
    # الوصول الآمن
    st.markdown(f"#### 🚧 {tm.t('modal.safe_access')}")
    safe_access = row.get('هل يتوفر وصول آمن إلى المنزل؟')
    if safe_access == "نعم":
        st.success(f"✅ {tm.t('modal.safe_access')}: {tm.t('modal.yes')}")
    else:
        st.warning(f"⚠️ {tm.t('modal.safe_access')}: {tm.t('modal.no')}")
        
        # أسباب عدم الوصول الآمن
        reasons = []
        if row.get('في حال عدم توفر الوصول الآمن، يرجى توضيح الأسباب/مخلفات حرب (ألغام، ذخائر غير منفجرة)'):
            reasons.append(f"🎯 {tm.t('assessment.war_remnants')}")
        if row.get('في حال عدم توفر الوصول الآمن، يرجى توضيح الأسباب/نزاع ملكية أو خلاف قانوني'):
            reasons.append(f"⚖️ {tm.t('assessment.ownership_dispute')}")
        if row.get('في حال عدم توفر الوصول الآمن، يرجى توضيح الأسباب/طريق مسدود بالأنقاض أو الركام'):
            reasons.append(f"🚧 {tm.t('assessment.blocked_road')}")
        if row.get('في حال عدم توفر الوصول الآمن، يرجى توضيح الأسباب/انهيار مبانٍ مجاورة تعيق الوصول'):
            reasons.append(f"🏚️ {tm.t('assessment.collapsed_buildings')}")
        if row.get('في حال عدم توفر الوصول الآمن، يرجى توضيح الأسباب/مبانٍ غير مستقرة أو مهددة بالانهيار في الطريق'):
            reasons.append(f"⚠️ {tm.t('assessment.unstable_buildings')}")
        
        if reasons:
            st.markdown(f"**{tm.t('modal.unsafe_reasons')}:**")
            for reason in reasons:
                st.markdown(f"- {reason}")
    
    st.markdown("---")
    
    # معلومات إضافية
    st.markdown(f"#### 📝 {tm.t('modal.additional_info')}")
    col1, col2 = st.columns(2)
    with col1:
        other_apps = row.get('هل لدى مالك المنزل طلبات استفادة أخرى ضمن مشاريع مشابهة؟')
        if pd.notna(other_apps) and str(other_apps).strip():
            st.info(f"**{tm.t('modal.other_applications')}:** {other_apps}")
    
    with col2:
        notes = row.get('ملاحظات إضافية أو تعليقات عامة (اختياري)')
        if pd.notna(notes) and str(notes).strip():
            st.info(f"**{tm.t('modal.notes')}:** {notes}")
    
    # المقاول
    contractor = row.get('Contractor')
    if pd.notna(contractor) and str(contractor).strip():
        st.markdown("---")
        st.success(f"👷 **{tm.t('modal.contractor')}:** {contractor}")


def create_beneficiary_modal(row, main_items_df=None, sub_items_df=None):
    """إنشاء نافذة منبثقة شاملة لعرض تفاصيل المستفيد"""
    direction = get_direction_style()
    
    # العنوان
    beneficiary_name = f"{row.get('الاسم الأول', '')} {row.get('اسم الأب', '')} {row.get('الكنية', '')}"
    st.markdown(f"<h1 style='{direction}'>👤 {beneficiary_name}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # التبويبات
    tabs = st.tabs([
        f"👤 {tm.t('modal.personal_info')}",
        f"👨‍👩‍👧‍👦 {tm.t('modal.family_info')}",
        f"📍 {tm.t('modal.address_info')}",
        f"🏠 {tm.t('modal.house_info')}",
        f"📸 {tm.t('modal.photos')}",
        f"💰 {tm.t('modal.costs')}",
        f"🔍 {tm.t('modal.assessment')}"
    ])
    
    with tabs[0]:
        create_personal_info_tab(row)
    
    with tabs[1]:
        create_family_info_tab(row)
    
    with tabs[2]:
        create_address_tab(row)
    
    with tabs[3]:
        create_house_info_tab(row)
    
    with tabs[4]:
        create_photos_tab(row)
    
    with tabs[5]:
        create_costs_tab(row, sub_items_df)
    
    with tabs[6]:
        create_assessment_tab(row)

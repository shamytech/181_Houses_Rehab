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
    """تبويب المعلومات الشخصية - تخطيط محسّن بأربعة أعمدة"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>👤 {tm.t('modal.personal_info')}</h3>", unsafe_allow_html=True)
    
    # 1. تجميع الأقسام الأربعة في سطر واحد بأربعة أعمدة
    col1, col2, col3, col4 = st.columns(4)
    
    # العمود الأول: المعلومات الأساسية
    with col1:
        st.markdown(f"<h4 style='{direction}'>📝 {tm.t('modal.basic_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.first_name'), row.get('الاسم الأول'), "📝")
        display_field(tm.t('fields.father_name'), row.get('اسم الأب'), "👨")
        display_field(tm.t('fields.last_name'), row.get('الكنية'), "📛")
        display_field(tm.t('fields.mother_name'), row.get('اسم الأم كما هو مذكور في الهوية'), "👩")
        
    # العمود الثاني: معلومات إضافية
    with col2:
        st.markdown(f"<h4 style='{direction}'>ℹ️ {tm.t('modal.additional_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.gender'), row.get('الجنس'), "⚧")
        display_field(tm.t('fields.birth_date'), row.get('تاريخ الميلاد كما هو مذكور في الهوية'), "📅")
        display_field(tm.t('fields.marital_status'), row.get('الحالة الاجتماعية'), "💍")
        display_field(tm.t('fields.spouse_name'), row.get('الاسم الثلاثي للزوج أو الزوجة (إن وجد)'), "👫")
    
    # العمود الثالث: معلومات الوثيقة
    with col3:
        st.markdown(f"<h4 style='{direction}'>🆔 {tm.t('modal.document_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.id_type'), row.get('نوع الوثيقة الشخصية'), "📋")
        display_field(tm.t('fields.id_number'), row.get('رقم الوثيقة الشخصية (الرقم الوطني)'), "🔢")
        # إضافة حقلين فارغين للحفاظ على التوازن المرئي مع الأعمدة الأخرى
        # display_field("", "", "")
        # display_field("", "", "")
    
    # العمود الرابع: معلومات الاتصال
    with col4:
        st.markdown(f"<h4 style='{direction}'>📞 {tm.t('modal.contact_info')}</h4>", unsafe_allow_html=True)
        display_field(tm.t('fields.phone'), row.get('رقم الهاتف الرئيسي (واتساب إن أمكن)'), "📱")
        display_field(tm.t('fields.phone_alt'), row.get('رقم هاتف بديل (إضافي)'), "📞")
        # إضافة حقلين فارغين للحفاظ على التوازن المرئي مع الأعمدة الأخرى
        # display_field("", "", "")
        # display_field("", "", "")
    
    # 2. صور الوثيقة (الوجه الأمامي والخلفي) - دمج 4 أعمدة
    st.markdown("---")
    st.markdown(f"<h3 style='{direction}'>📸 {tm.t('modal.id_photos')}</h3>", unsafe_allow_html=True)
    
    front_url = row.get('صورة الوثيقة الشخصية (الوجه الأول)_URL')
    back_url = row.get('صورة الوثيقة الشخصية (الوجه الثاني)_URL')
    
    # استخدام st.columns(2) لعرض الصورتين بجانب بعضهما، مع تقليل حجم الصورة (width=200)
    img_col1, img_col2 = st.columns(2)
    
    with img_col1:
        st.markdown(f"**🪪 {tm.t('fields.id_photo_front')}**")
        # تم تقليل العرض من 300 إلى 200 لتقليل الحجم
        display_image_with_rotate(front_url, tm.t('fields.id_photo_front'), "id_front", width=200)
    
    with img_col2:
        st.markdown(f"**🪪 {tm.t('fields.id_photo_back')}**")
        # تم تقليل العرض من 300 إلى 200 لتقليل الحجم
        display_image_with_rotate(back_url, tm.t('fields.id_photo_back'), "id_back", width=200)
        
    # 3. القسم الرابع: معلومات صحية (افتراضاً أنه يمثل "الصورة الخلفية" المطلوبة)
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>🏥 {tm.t('modal.health_info')}</h4>", unsafe_allow_html=True)
    col_health1, col_health2 = st.columns(2)
    with col_health1:
        display_field(tm.t('fields.disability'), row.get('هل مالك المنزل من الأشخاص ذوي الإعاقة؟'), "♿")
    with col_health2:
        display_field(tm.t('fields.chronic_diseases'), row.get('هل تعاني من أمراض مزمنة؟'), "💊")

def create_family_info_tab(row):
    """تبويب معلومات الأسرة - تخطيط محسّن بـ 3 أعمدة متوازنة لجميع الأقسام"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>👨‍👩‍👧‍👦 {tm.t('modal.family_info')}</h3>", unsafe_allow_html=True)
    
    # 1. معلومات عامة (3 حقول / 3 أعمدة = 1 حقل لكل عمود)
    # st.markdown(f"<h4 style='{direction}'>🏠 {tm.t('modal.general_info')}</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        display_field(tm.t('fields.families_in_house'), row.get('عدد العائلات المقيمة في نفس المنزل'), "🏠")
    with col2:
        display_field(tm.t('fields.family_size'), row.get('عدد أفراد الأسرة (بما فيهم مالك المنزل)'), "👥")
    with col3:
        display_field(tm.t('fields.family_type'), row.get('نوع معيل الأسرة'), "💼")
    
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>📊 {tm.t('modal.family_distribution')}</h4>", unsafe_allow_html=True)
    
    # 2. توزيع الأسرة (6 حقول / 3 أعمدة = 2 حقل لكل عمود)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_field(tm.t('fields.men') + " (+18)", row.get('عدد الرجال (العمر أكبر من 18 سنة)'), "👨")
        display_field(tm.t('fields.women') + " (+18)", row.get('عدد النساء (العمر أكبر من 18 سنة)'), "👩")
    
    with col2:
        display_field(tm.t('fields.boys'), row.get('عدد الشباب الذكور (من 12 إلى 17 سنة)'), "👦")
        display_field(tm.t('fields.girls'), row.get('عدد الفتيات الإناث (من 12 إلى 17 سنة)'), "👧")
    
    with col3:
        display_field(tm.t('fields.child_boys'), row.get('عدد الأطفال الذكور (دون سن 12 سنة)'), "👶")
        display_field(tm.t('fields.child_girls'), row.get('عدد الأطفال الإناث (دون سن 12 سنة)'), "👶")
    
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>🎯 {tm.t('modal.special_categories')}</h4>", unsafe_allow_html=True)
    
    # 3. الفئات الخاصة (7 حقول / 3 أعمدة = 3، 2، 2)
    col1, col2, col3 = st.columns(3)
    
    # العمود الأول: 3 حقول
    with col1:
        display_field(tm.t('fields.elderly_count'), row.get('عدد أفراد الأسرة من كبار السن (60 سنة فأكثر)'), "👴")
        display_field(tm.t('fields.disabled_count'), row.get('عدد أفراد الأسرة من ذوي الإعاقة'), "♿")
        display_field(tm.t('fields.separated_children'), row.get('عدد الأطفال المنفصلين عن ذويهم'), "👶")
    
    # العمود الثاني: 2 حقل
    with col2:
        display_field(tm.t('fields.nursing_mothers'), row.get('عدد النساء المرضعات'), "🤱")
        display_field(tm.t('fields.pregnant_women'), row.get('عدد النساء الحوامل'), "🤰")
        # حقل فارغ للحفاظ على التوازن المرئي
        # display_field("", "", "")
    
    # العمود الثالث: 2 حقل
    with col3:
        display_field(tm.t('fields.divorced_women'), row.get('عدد النساء المطلقات'), "💔")
        display_field(tm.t('fields.widowed_women'), row.get('عدد النساء الأرامل'), "🖤")
        # حقل فارغ للحفاظ على التوازن المرئي
        # display_field("", "", "")
    
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>💰 {tm.t('modal.economic_info')}</h4>", unsafe_allow_html=True)
    
    # 4. المعلومات الاقتصادية (2 حقل / 3 أعمدة = 1، 1، 0)
    col1, col2, col3 = st.columns(3)
    with col1:
        display_field(tm.t('fields.income_source'), row.get('ما هو مصدر الدخل الرئيسي للأسرة؟'), "💵")
    with col2:
        display_field(tm.t('fields.working_members'), row.get('عدد الأفراد العاملين في الأسرة'), "👷")
    # with col3:
        # حقل فارغ للحفاظ على التوازن المرئي
        # display_field("", "", "")


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
    """تبويب معلومات المنزل - تخطيط محسّن بـ 3 أعمدة متوازنة لجميع الأقسام"""
    direction = get_direction_style()
    
    st.markdown(f"<h3 style='{direction}'>🏠 {tm.t('modal.house_info')}</h3>", unsafe_allow_html=True)
    
    # 1. معلومات أساسية (5 حقول / 3 أعمدة = 2، 2، 1 + حقل فارغ)
    st.markdown(f"<h4 style='{direction}'>📝 {tm.t('modal.basic_info')}</h4>", unsafe_allow_html=True)
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
        # حقل فارغ للحفاظ على التوازن المرئي
        # display_field("", "", "")
    
    # 2. وثائق الملكية (3 حقول / 3 أعمدة = 1، 1، 1)
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>📄 {tm.t('modal.ownership_documents')}</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_field(tm.t('fields.ownership_document'), row.get('هل لديك وثيقة اثبات ملكية حديث؟'), "📋")
    with col2:
        display_field(tm.t('fields.ownership_type'), row.get('نوع وثيقة الملكية'), "📑")
    with col3:
        display_field(tm.t('fields.ownership_date'), row.get('تاريخ إصدار وثيقة الملكية'), "📅")
    
    # 3. صورة وثيقة الملكية (عرض كامل)
    ownership_url = row.get('صورة وثيقة الملكية_URL')
    if pd.notna(ownership_url) and ownership_url:
        st.markdown(f"**📸 {tm.t('modal.ownership_document')}**")
        try:
            st.image(ownership_url, use_container_width=True)
        except:
            st.info(f"🔗 {ownership_url}")
    
    # 4. حالة المنزل (6 حقول / 3 أعمدة = 2، 2، 2)
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>🔍 {tm.t('modal.house_condition')}</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_field(tm.t('fields.external_walls'), row.get('هل يملك المنزل أو الشقة جدرانًا خارجية سليمة ولا يحتاج إلى أعمال بناء (بلوك) خارجية؟'), "🧱")
        display_field(tm.t('fields.internal_walls'), row.get('هل يملك المنزل أو الشقة جدرانًا داخلية مكتملة ولا يحتاج إلى أعمال بناء (بلوك) داخلية؟'), "🏗️")
    
    with col2:
        display_field(tm.t('fields.roof'), row.get('هل يملك المنزل أو الشقة سقفًا وسلالم (أدراج) سليمة؟'), "🏚️")
        display_field(tm.t('fields.building_damage'), row.get('هل توجد أية أضرار إنشائية في المنزل أو الشقة؟'), "⚠️")
    
    with col3:
        display_field(tm.t('fields.facilities'), row.get('هل المرافق (المياه والصرف) عاملة أم مجرد بناء؟'), "🚰")
        display_field(tm.t('fields.sewerage'), row.get('هل المنزل موصول بنظام صرف صحي أو حفرة فنية؟'), "🚽")
    
    # 5. وصف الضرر (عرض كامل)
    st.markdown("---")
    st.markdown(f"<h4 style='{direction}'>📝 {tm.t('modal.damage_description')}</h4>", unsafe_allow_html=True)
    damage_desc = row.get('وصف حالة الضرر من وجهة نظرك كمالك للمنزل')
    if pd.notna(damage_desc) and str(damage_desc).strip():
        st.info(damage_desc)
    else:
        st.info(tm.t('messages.no_data'))


def create_photos_tab(row):
    """تبويب صور المنزل - تصميم محسن مع خيارات عرض متعددة"""
    direction = get_direction_style()
    
    # 1. تجميع كل الصور المتاحة
    images = []
    
    fields_config = [
        (tm.t('fields.front_view'), 'صورة الواجهة الأمامية للمنزل_URL', "🏠"),
        (tm.t('fields.inside_view'), 'صورة من داخل المنزل_URL', "🪟"),
        (tm.t('fields.walls'), 'صورة توضح حالة الجدران_URL', "🧱"),
        (tm.t('fields.columns'), 'صورة توضح حالة الأعمدة_URL', "🏛️"),
        (tm.t('fields.roof'), 'صورة توضح حالة السقف_URL', "🏠"),
        (tm.t('fields.kitchen'), 'صورة توضح حالة المرافق (المطبخ)_URL', "🍳"),
        (tm.t('fields.bathroom'), 'صورة توضح حالة المرافق (الحمام)_URL', "🚿"),
        (tm.t('fields.toilet'), 'صورة توضح حالة المرافق (التواليت)_URL', "🚽")
    ]

    for label, key, icon in fields_config:
        url = row.get(key)
        if pd.notna(url) and url:
            images.append({'label': label, 'url': url, 'icon': icon, 'key': key})

    if not images:
        st.warning(tm.t('messages.no_data'))
        return

    # 2. CSS المحسن
    st.markdown("""
        <style>
        /* حاوية الصورة في السلايدر - متوسطة */
        .slider-image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background: #1a1a2e;
            border-radius: 12px;
            padding: 15px;
            min-height: 350px;
            max-height: 550px;
            overflow: hidden;
        }
        
        .slider-image-container img {
            max-height: 550px !important;
            width: auto !important;
            max-width: 100% !important;
            object-fit: contain !important;
            border-radius: 8px;
        }
        
        /* حاوية الصورة في الشبكي - كامل العرض */
        .grid-image-container {
            background: #2d2d44;
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 5px;
        }
        
        .grid-image-container img {
            width: 100% !important;
            height: auto !important;
            border-radius: 8px;
            display: block;
        }
        
        /* عنوان الصورة في الشبكي */
        .grid-image-title {
            text-align: center;
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        /* شريط التحكم */
        .photo-control-bar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. تهيئة حالة العرض
    if 'photo_view_mode' not in st.session_state:
        st.session_state.photo_view_mode = 'slider'
    
    if 'photo_idx' not in st.session_state:
        st.session_state.photo_idx = 0
    
    if 'expanded_image' not in st.session_state:
        st.session_state.expanded_image = None
    
    total = len(images)
    if st.session_state.photo_idx >= total:
        st.session_state.photo_idx = 0

    # 4. دوال التنقل
    def go_prev():
        st.session_state.photo_idx = (st.session_state.photo_idx - 1) % total
    
    def go_next():
        st.session_state.photo_idx = (st.session_state.photo_idx + 1) % total
    
    def toggle_view():
        st.session_state.photo_view_mode = 'grid' if st.session_state.photo_view_mode == 'slider' else 'slider'
    
    def expand_image(url, label):
        st.session_state.expanded_image = {'url': url, 'label': label}
    
    def close_expanded():
        st.session_state.expanded_image = None

    # 5. عرض الصورة المكبرة
    if st.session_state.expanded_image:
        st.markdown(f"""
            <div style='background: #1a1a2e; padding: 15px; border-radius: 12px; text-align: center;'>
                <p style='color: white; font-size: 16px; margin-bottom: 10px;'>
                    🔍 {st.session_state.expanded_image['label']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            st.image(st.session_state.expanded_image['url'], use_container_width=True)
        except:
            st.error("❌ خطأ في تحميل الصورة")
        
        st.button("✖️ إغلاق العرض المكبر", on_click=close_expanded, use_container_width=True, type="primary")
        return

    # 6. شريط التحكم العلوي
    if st.session_state.photo_view_mode == 'slider':
        # === وضع السلايدر ===
        current = images[st.session_state.photo_idx]
        
        col_mode, col_prev, col_info, col_next, col_expand = st.columns([1.2, 0.7, 3.5, 0.7, 1])
        
        with col_mode:
            st.button("🔲 شبكي", on_click=toggle_view, use_container_width=True, key="to_grid")
        
        with col_prev:
            st.button("◀", on_click=go_prev, use_container_width=True, key="prev_btn")
        
        with col_info:
            st.markdown(f"""
                <div class='photo-control-bar'>
                    <span style='font-weight: bold;'>{current['icon']} {current['label']}</span>
                    <span style='opacity: 0.8; font-size: 12px;'> ({st.session_state.photo_idx + 1}/{total})</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col_next:
            st.button("▶", on_click=go_next, use_container_width=True, key="next_btn")
        
        with col_expand:
            if st.button("🔍", use_container_width=True, key="expand_btn", help="تكبير الصورة"):
                expand_image(current['url'], f"{current['icon']} {current['label']}")
        
        # عرض الصورة في المنتصف (حجم محدود)
        st.markdown(f"""
            <div class='slider-image-container'>
                <img src='{current['url']}' alt='{current['label']}' 
                     onerror="this.onerror=null; this.src='https://via.placeholder.com/400x300?text=Error';">
            </div>
        """, unsafe_allow_html=True)
        
        # شريط التقدم
        st.progress((st.session_state.photo_idx + 1) / total)
        
        # أزرار التنقل السريع
        if total > 1:
            st.markdown("##### التنقل السريع:")
            thumb_cols = st.columns(min(total, 8))
            
            for i, img in enumerate(images[:8]):
                with thumb_cols[i]:
                    def select_image(idx=i):
                        st.session_state.photo_idx = idx
                    
                    st.button(
                        img['icon'],
                        key=f"thumb_{i}",
                        help=img['label'],
                        on_click=select_image,
                        use_container_width=True,
                        type="primary" if i == st.session_state.photo_idx else "secondary"
                    )
    
    else:
        # === وضع العرض الشبكي - الصور بكامل الحجم ===
        col_mode, col_info = st.columns([1.2, 5])
        
        with col_mode:
            st.button("▶️ سلايدر", on_click=toggle_view, use_container_width=True, key="to_slider")
        
        with col_info:
            st.markdown(f"""
                <div class='photo-control-bar'>
                    <span style='font-weight: bold;'>📷 جميع الصور ({total})</span>
                </div>
            """, unsafe_allow_html=True)
        
        # عرض الصور في شبكة (2 بجانب بعض) - بكامل العرض
        for i in range(0, len(images), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                img1 = images[i]
                st.markdown(f"<div class='grid-image-title'>{img1['icon']} {img1['label']}</div>", unsafe_allow_html=True)
                
                # الصورة بكامل العرض باستخدام st.image
                try:
                    st.image(img1['url'], use_container_width=True)
                except:
                    st.error("❌ خطأ في التحميل")
                
                if st.button(f"🔍 تكبير", key=f"exp_grid_{i}", use_container_width=True):
                    expand_image(img1['url'], f"{img1['icon']} {img1['label']}")
            
            with col2:
                if i + 1 < len(images):
                    img2 = images[i + 1]
                    st.markdown(f"<div class='grid-image-title'>{img2['icon']} {img2['label']}</div>", unsafe_allow_html=True)
                    
                    try:
                        st.image(img2['url'], use_container_width=True)
                    except:
                        st.error("❌ خطأ في التحميل")
                    
                    if st.button(f"🔍 تكبير", key=f"exp_grid_{i+1}", use_container_width=True):
                        expand_image(img2['url'], f"{img2['icon']} {img2['label']}")
            
            st.markdown("---")


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
    
    # 1. بطاقة التكلفة الإجمالية (حجم مدمج جداً)
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #009688, #00796B); 
                    color: white; padding: 8px 15px; border-radius: 6px; 
                    text-align: center; margin-bottom: 10px; display: flex; 
                    justify-content: space-between; align-items: center;'>
            <span style='font-size: 14px; font-weight: bold;'>{tm.t('modal.total_cost')}</span>
            <span style='font-size: 18px; font-weight: bold;'>${total_cost:,.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. تحديد أسماء الحقول حسب اللغة
    is_english = tm.get_current_language() == 'en'
    main_item_col = 'البند الرئيسي EN' if is_english else 'البند الرئيسي'
    sub_item_col = 'البند الفرعي EN' if is_english else 'البند الفرعي'
    
    # التحقق من وجود الأعمدة الإنجليزية، وإلا استخدام العربية
    if main_item_col not in house_items.columns:
        main_item_col = 'البند الرئيسي'
    if sub_item_col not in house_items.columns:
        sub_item_col = 'البند الفرعي'
    
    # 3. تقسيم العرض: جدول (يمين) وصورة (يسار)
    col_table, col_image = st.columns([1.5, 1])
    
    with col_table:
        st.markdown(f"<h4 style='{direction}'>📊 {tm.t('modal.items_details')} ({len(house_items)} {tm.t('modal.items')})</h4>", unsafe_allow_html=True)
        
        # إنشاء DataFrame جديد بالأعمدة المطلوبة فقط (لتجنب التكرار)
        display_data = []
        for idx, row in house_items.iterrows():
            row_data = {
                tm.t('modal.main_item'): row.get(main_item_col, ''),
                tm.t('modal.sub_item'): row.get(sub_item_col, ''),
                tm.t('modal.quantity'): row.get('الكمية', 0),
                tm.t('modal.unit_price'): f"${row.get('السعر الافرادي', 0):,.2f}" if pd.notna(row.get('السعر الافرادي')) else "-",
                tm.t('modal.total'): f"${row.get('الإجمالي', 0):,.2f}" if pd.notna(row.get('الإجمالي')) else "-"
            }
            display_data.append(row_data)
        
        display_df = pd.DataFrame(display_data)
        
        # الأعمدة المطلوب عرضها
        display_cols = [
            tm.t('modal.main_item'), 
            tm.t('modal.sub_item'), 
            tm.t('modal.quantity'), 
            tm.t('modal.unit_price'), 
            tm.t('modal.total')
        ]
        
        # التأكد من وجود الأعمدة
        available_cols = [c for c in display_cols if c in display_df.columns]
        
        if not available_cols:
            st.warning(tm.t('messages.no_data'))
            return
        
        # عرض الجدول مع إمكانية التحديد
        selected_rows = st.dataframe(
            display_df[available_cols],
            use_container_width=True,
            hide_index=True,
            height=300,
            on_select="rerun",
            selection_mode="single-row"
        )
    
    with col_image:
        # تحديد الصف المحدد (إذا لم يكن هناك تحديد، استخدم الصف الأول)
        selected_idx = 0
        if selected_rows and selected_rows.selection and selected_rows.selection.rows:
            selected_idx = selected_rows.selection.rows[0]
        
        # عرض صورة البند المحدد فقط
        house_items_reset = house_items.reset_index(drop=True)
        if selected_idx < len(house_items_reset):
            selected_item = house_items_reset.iloc[selected_idx]
            
            # عرض صورة البند
            item_photo_url = selected_item.get('صورة توضيحية للبند_URL', '')
            
            if pd.notna(item_photo_url) and item_photo_url:
                # عنوان البند (من العمود المحدد حسب اللغة)
                main_item = selected_item.get(main_item_col, tm.t('modal.not_specified'))
                sub_item = selected_item.get(sub_item_col, tm.t('modal.not_specified'))
                
                st.markdown(f"**📸 {main_item} - {sub_item}**")
                try:
                    st.image(item_photo_url, use_container_width=True)
                except:
                    st.info(f"🔗 {item_photo_url}")
            else:
                st.info(f"📷 {tm.t('messages.no_data')}")
                st.markdown(f"*{tm.t('modal.item_photo')}*")


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
    # st.markdown(f"<h1 style='{direction}'>👤 {beneficiary_name}</h1>", unsafe_allow_html=True)
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

"""
صفحة قائمة المنازل
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# إضافة مسار المشروع
sys.path.append(str(Path(__file__).parent.parent))

from config import *
from utils.data_loader import (
    load_houses_data,
    filter_houses,
    search_houses
)

# إعدادات الصفحة
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# العنوان
st.markdown("""
    <h1 style='text-align: center; color: #0D47A1;'>
        🏠 قائمة المنازل
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
    
    # أدوات البحث والفلترة
    st.markdown("### 🔍 البحث والفلترة")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # بحث نصي
        search_term = st.text_input("🔎 بحث (الاسم، الرقم الوطني، العنوان)", "")
    
    with col2:
        # فلترة حسب المحافظة
        governorates = ['الكل'] + sorted(df['المحافظة'].dropna().unique().tolist())
        selected_gov = st.selectbox("📍 المحافظة", governorates)
    
    with col3:
        # فلترة حسب حالة الضرر
        damage_statuses = ['الكل'] + sorted(df['حالة الضرر'].dropna().unique().tolist())
        selected_damage = st.selectbox("⚠️ حالة الضرر", damage_statuses)
    
    with col4:
        # فلترة حسب نوع المنزل
        house_types = ['الكل'] + sorted(df['نوع المنزل'].dropna().unique().tolist())
        selected_type = st.selectbox("🏘️ نوع المنزل", house_types)
    
    # تطبيق الفلاتر
    filtered_df = df.copy()
    
    # البحث
    if search_term:
        filtered_df = search_houses(filtered_df, search_term)
    
    # الفلاتر
    filtered_df = filter_houses(
        filtered_df,
        governorate=selected_gov if selected_gov != 'الكل' else None,
        damage_status=selected_damage if selected_damage != 'الكل' else None,
        house_type=selected_type if selected_type != 'الكل' else None
    )
    
    # عرض النتائج
    st.markdown(f"### 📋 النتائج ({len(filtered_df)} منزل)")
    
    if len(filtered_df) > 0:
        
        # إعداد البيانات للعرض
        display_cols = [
            '_index',
            'الاسم الكامل',
            'المحافظة',
            'المنطقة',
            'الناحية',
            'نوع المنزل',
            'حالة الضرر',
            'عدد أفراد الأسرة (بما فيهم مالك المنزل)',
            'رقم الهاتف الرئيسي (واتساب إن أمكن)'
        ]
        
        # التأكد من وجود الأعمدة
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        display_df = filtered_df[available_cols].copy()
        
        # إعادة تسمية الأعمدة للعرض
        display_df.columns = [
            'الرقم',
            'الاسم الكامل',
            'المحافظة',
            'المنطقة',
            'الناحية',
            'نوع المنزل',
            'حالة الضرر',
            'عدد الأفراد',
            'الهاتف'
        ][:len(available_cols)]
        
        # عرض الجدول
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # زر التصدير
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            # تصدير إلى CSV
            csv = display_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 تصدير إلى CSV",
                data=csv,
                file_name="houses_list.csv",
                mime="text/csv"
            )
        
        with col2:
            # تصدير إلى Excel
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                display_df.to_excel(writer, index=False, sheet_name='المنازل')
            output.seek(0)
            
            st.download_button(
                label="📥 تصدير إلى Excel",
                data=output,
                file_name="houses_list.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # عرض تفاصيل كل منزل
        st.markdown("---")
        st.markdown("### 📝 تفاصيل المنازل")
        
        # اختيار منزل لعرض التفاصيل
        for idx, row in filtered_df.iterrows():
            house_name = row.get('الاسم الكامل', 'غير محدد')
            house_area = row.get('المنطقة', 'غير محدد')
            damage_status = row.get('حالة الضرر', 'غير محدد')
            
            # تحديد اللون حسب حالة الضرر
            status_color = DAMAGE_STATUS.get(damage_status, {}).get('color', INFO_BLUE)
            
            with st.expander(f"🏠 {house_name} - {house_area} ({damage_status})"):
                
                # قسم معلومات المالك
                st.markdown("#### 👤 معلومات المالك")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    - **الاسم الكامل:** {row.get('الاسم الكامل', 'غير محدد')}
                    - **الجنس:** {row.get('الجنس', 'غير محدد')}
                    - **تاريخ الميلاد:** {row.get('تاريخ الميلاد كما هو مذكور في الهوية', 'غير محدد')}
                    - **الحالة الاجتماعية:** {row.get('الحالة الاجتماعية', 'غير محدد')}
                    """)
                
                with col2:
                    st.markdown(f"""
                    - **نوع الوثيقة:** {row.get('نوع الوثيقة الشخصية', 'غير محدد')}
                    - **رقم الوثيقة:** {row.get('رقم الوثيقة الشخصية (الرقم الوطني)', 'غير محدد')}
                    - **الهاتف:** {row.get('رقم الهاتف الرئيسي (واتساب إن أمكن)', 'غير محدد')}
                    - **هاتف بديل:** {row.get('رقم هاتف بديل (إضافي)', 'غير محدد')}
                    """)
                
                # صور الوثيقة
                id_front_url = row.get('صورة الوثيقة الشخصية (الوجه الأول)_URL', '')
                id_back_url = row.get('صورة الوثيقة الشخصية (الوجه الثاني)_URL', '')
                
                if id_front_url or id_back_url:
                    st.markdown("**صور الوثيقة:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if id_front_url:
                            try:
                                st.image(id_front_url, caption="الوجه الأول", use_container_width=True)
                            except:
                                st.warning("لم يتم تحميل الصورة")
                    
                    with col2:
                        if id_back_url:
                            try:
                                st.image(id_back_url, caption="الوجه الثاني", use_container_width=True)
                            except:
                                st.warning("لم يتم تحميل الصورة")
                
                st.markdown("---")
                
                # قسم معلومات الأسرة
                st.markdown("#### 👨‍👩‍👧‍👦 معلومات الأسرة")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("إجمالي الأفراد", row.get('عدد أفراد الأسرة (بما فيهم مالك المنزل)', 0))
                
                with col2:
                    st.metric("الرجال", row.get('عدد الرجال (العمر أكبر من 18 سنة)', 0))
                
                with col3:
                    st.metric("النساء", row.get('عدد النساء (العمر أكبر من 18 سنة)', 0))
                
                with col4:
                    st.metric("الأطفال", 
                             int(row.get('عدد الأطفال الذكور (دون سن 12 سنة)', 0)) + 
                             int(row.get('عدد الأطفال الإناث (دون سن 12 سنة)', 0)))
                
                st.markdown("---")
                
                # قسم معلومات المنزل
                st.markdown("#### 🏠 معلومات المنزل")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    - **العنوان:** {row.get('عنوان المنزل الكامل', row.get('العنوان التفصيلي لمكان السكن الحالي', 'غير محدد'))}
                    - **المحافظة:** {row.get('المحافظة', 'غير محدد')}
                    - **المنطقة:** {row.get('المنطقة', 'غير محدد')}
                    - **الناحية:** {row.get('الناحية', 'غير محدد')}
                    """)
                
                with col2:
                    st.markdown(f"""
                    - **نوع المنزل:** {row.get('نوع المنزل', 'غير محدد')}
                    - **عدد الغرف:** {row.get('عدد الغرف (بما فيها الصالون)', 'غير محدد')}
                    - **المساحة:** {row.get('مساحة المنزل بالمتر المربع', 'غير محدد')} م²
                    - **الطابق:** {row.get('رقم الطابق الذي يقع فيه المنزل', 'غير محدد')}
                    """)
                
                # الإحداثيات
                lat = row.get('latitude', None)
                lon = row.get('longitude', None)
                
                if pd.notna(lat) and pd.notna(lon):
                    st.markdown(f"**الإحداثيات:** {lat}, {lon}")
                
                st.markdown("---")
                
                # قسم الصور
                st.markdown("#### 📸 صور المنزل")
                
                # جمع روابط الصور
                image_cols = [
                    ('صورة الواجهة الأمامية للمنزل_URL', 'الواجهة الأمامية'),
                    ('صورة للمنزل من الداخل_URL', 'من الداخل'),
                    ('صورة توضح حالة الجدران_URL', 'حالة الجدران'),
                    ('صورة توضح حالة الأعمدة_URL', 'حالة الأعمدة'),
                    ('صورة توضح حالة السقف_URL', 'حالة السقف'),
                    ('صورة توضح حالة المرافق (المطبخ)_URL', 'المطبخ'),
                    ('صورة توضح حالة المرافق (الحمام)_URL', 'الحمام'),
                    ('صورة توضح حالة المرافق (التواليت)_URL', 'التواليت')
                ]
                
                # عرض الصور في صفوف
                images_per_row = 3
                images = [(col, caption) for col, caption in image_cols if row.get(col, '')]
                
                for i in range(0, len(images), images_per_row):
                    cols = st.columns(images_per_row)
                    for j, (img_col, caption) in enumerate(images[i:i+images_per_row]):
                        with cols[j]:
                            img_url = row.get(img_col, '')
                            if img_url:
                                try:
                                    st.image(img_url, caption=caption, use_container_width=True)
                                except:
                                    st.warning(f"لم يتم تحميل صورة {caption}")
                
                # تقييم الضرر
                st.markdown("---")
                st.markdown("#### ⚠️ تقييم الضرر")
                
                damage_desc = row.get('وصف حالة الضرر من وجهة نظرك كمالك للمنزل', 'غير محدد')
                st.markdown(f"**الوصف:** {damage_desc}")
                
                st.markdown(f"""
                - **حالة الضرر:** <span style='color: {status_color}; font-weight: bold;'>{damage_status}</span>
                - **الجدران الخارجية:** {row.get('هل يملك المنزل أو الشقة جدرانًا خارجية سليمة ولا يحتاج إلى أعمال بناء (بلوك) خارجية؟', 'غير محدد')}
                - **الجدران الداخلية:** {row.get('هل يملك المنزل أو الشقة جدرانًا داخلية مكتملة ولا يحتاج إلى أعمال بناء (بلوك) داخلية؟', 'غير محدد')}
                - **السقف:** {row.get('هل يملك المنزل أو الشقة سقفًا وسلالم (أدراج) سليمة؟', 'غير محدد')}
                - **المرافق:** {row.get('هل المرافق (المياه والصرف) عاملة أم مجرد بناء؟', 'غير محدد')}
                """, unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ لا توجد نتائج مطابقة للبحث أو الفلاتر المحددة")

else:
    st.error("⚠️ لا توجد بيانات لعرضها")

# الشريط الجانبي
with st.sidebar:
    st.markdown("### 🏠 قائمة المنازل")
    st.markdown("""
        هذه الصفحة تعرض قائمة شاملة بجميع المنازل المسجلة في المشروع.
        
        **الميزات:**
        - 🔍 بحث متقدم
        - 📊 فلترة حسب معايير متعددة
        - 📥 تصدير البيانات
        - 📝 عرض تفاصيل كل منزل
        - 📸 معرض صور شامل
    """)

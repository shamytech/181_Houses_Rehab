"""
Translation system for multilingual support
"""

TRANSLATIONS = {
    'ar': {
        # Navigation
        'dashboard': 'لوحة المعلومات',
        'houses_list': 'قائمة المنازل',
        'interactive_map': 'خريطة تفاعلية',
        'statistics': 'إحصائيات',
        'work_items': 'بنود العمل',
        
        # Dashboard
        'title': 'إعادة تأهيل المنازل في معرة النعمان',
        'app_title': 'لوحة تحكم إعادة تأهيل المنازل',
        'app_subtitle': 'برنامج الأمم المتحدة الإنمائي (UNDP) - ريف دمشق',
        'sections': {
            'key_indicators': 'المؤشرات الرئيسية',
            'damage_distribution': 'توزيع الضرر',
            'house_types': 'أنواع المنازل',
            'geographic_distribution': 'التوزيع الجغرافي',
            'demographics': 'الديموغرافيا'
        },
        'metrics': {
            'total_applications': 'إجمالي الطلبات',
            'light_damage': 'ضرر خفيف',
            'medium_damage': 'ضرر متوسط',
            'severe_damage': 'ضرر شديد',
            'estimated_cost': 'التكلفة التقديرية',
            'total_families': 'إجمالي الأسر',
            'total_individuals': 'إجمالي الأفراد',
            'disabled_persons': 'ذوي الإعاقة',
            'elderly': 'كبار السن'
        },
        'font_family': 'Tajawal, sans-serif',
        'no_houses_received': 'عدد وحدات/شقق المنازل التي تلقت مساهمة من UNDP (الهدف 20)',
        'houses_nominated': 'عدد المنازل التي تم ترشيحها',
        'houses_studied': 'عدد المنازل التي تم دراستها',
        'houses_assigned': 'عدد المنازل التي أسندت للمقاول',
        'houses_rehabilitating': 'عدد المنازل قيد الترميم',
        'houses_suspended': 'عدد المنازل المتوقفة مؤقتاً',
        'houses_completed': 'عدد المنازل المنتهية والمسلمة لأصحابها',
        'point_on_map': 'النقطة على الخريطة',
        'progress_survey': 'مخطط نسبة التقدم في إنجاز دراسة الكميات من 100% أو من عدد المنازل',
        'progress_rehab': 'نسبة التقدم في إنجاز الترميم من 100% أو من عدد المنازل',
        'ownership_docs': 'مخطط بياني أعمدة عن نوع وثائق الملكية',
        'damage_filter': 'فلتر نوع الضرر',
        'damage_light': 'خفيف',
        'damage_moderate': 'متوسط',
        'date_filter': 'فلتر التاريخ (تقرير تراكمي)',
        'rejected_houses': 'استعلام عن المنازل المرفوضة مع السبب',
        'suspended_houses': 'استعلام عن المنازل المتوقفة مؤقتاً مع السبب',
        'beneficiary_families': 'عدد العائلات المستفيدة - الأفراد',
        'ownership_training': 'عدد العائلات/المستفيدين الذين تلقوا تدريبات حقوق الملكية',
        'document_support': 'عدد العائلات التي استلمت مبلغ الدعم لوثائق الملكية - الهدف 200',
        
        # Details page
        'personal_info': 'معلومات شخصية',
        'address_info': 'معلومات العنوان',
        'evaluation': 'التقييم',
        'house_photos': 'صور المنزل',
        'estimated_boq': 'بنود الكميات التقديرية',
        'estimated_cost': 'الكلفة التقديرية',
        'search': 'بحث',
        'filter': 'فلترة',
        'beneficiary_name': 'اسم المستفيد',
        'view_details': 'عرض التفاصيل',
        
        # Common
        'total': 'الإجمالي',
        'target': 'الهدف',
        'progress': 'التقدم',
        'status': 'الحالة',
        'location': 'الموقع',
        'cost': 'التكلفة',
        'quantity': 'الكمية',
        'unit_price': 'السعر الإفرادي',
        'total_price': 'السعر الإجمالي',
        'messages': {
            'no_data': 'لا توجد بيانات متاحة'
        }
    },
    'en': {
        # Navigation
        'dashboard': 'Dashboard',
        'houses_list': 'Houses List',
        'interactive_map': 'Interactive Map',
        'statistics': 'Statistics',
        'work_items': 'Work Items',
        
        # Dashboard
        'title': 'Houses Rehabilitation in Maaret Alnoman',
        'app_title': 'Houses Rehabilitation Dashboard',
        'app_subtitle': 'United Nations Development Programme (UNDP) - Rural Damascus',
        'sections': {
            'key_indicators': 'Key Indicators',
            'damage_distribution': 'Damage Distribution',
            'house_types': 'House Types',
            'geographic_distribution': 'Geographic Distribution',
            'demographics': 'Demographics'
        },
        'metrics': {
            'total_applications': 'Total Applications',
            'light_damage': 'Light Damage',
            'medium_damage': 'Medium Damage',
            'severe_damage': 'Severe Damage',
            'estimated_cost': 'Estimated Cost',
            'total_families': 'Total Families',
            'total_individuals': 'Total Individuals',
            'disabled_persons': 'Disabled Persons',
            'elderly': 'Elderly'
        },
        'font_family': 'Inter, sans-serif',
        'no_houses_received': 'No. of houses units/apartments received UNDP contribution (Target 20)',
        'houses_nominated': 'Number of nominated houses',
        'houses_studied': 'Number of houses studied',
        'houses_assigned': 'Number of houses assigned to contractor',
        'houses_rehabilitating': 'Number of houses under rehabilitation',
        'houses_suspended': 'Number of temporarily suspended houses',
        'houses_completed': 'Number of completed and handed over houses',
        'point_on_map': 'Point on map',
        'progress_survey': 'Progress chart for quantity survey completion from 100% or number of houses',
        'progress_rehab': 'Progress percentage in rehabilitation completion from 100% or number of houses',
        'ownership_docs': 'Bar chart for type of ownership documents',
        'damage_filter': 'Damage type filter',
        'damage_light': 'Light',
        'damage_moderate': 'Moderate',
        'date_filter': 'Date filter (cumulative report)',
        'rejected_houses': 'Query for rejected houses with reason',
        'suspended_houses': 'Query for temporarily suspended houses with reason',
        'beneficiary_families': 'Number of beneficiary families - individuals',
        'ownership_training': 'Number of families/beneficiaries who received ownership rights training',
        'document_support': 'Number of families who received ownership document support amount - Target 200',
        
        # Details page
        'personal_info': 'Personal Information',
        'address_info': 'Address Information',
        'evaluation': 'Evaluation',
        'house_photos': 'House Photos',
        'estimated_boq': 'Estimated Bill of Quantities',
        'estimated_cost': 'Estimated Cost',
        'search': 'Search',
        'filter': 'Filter',
        'beneficiary_name': 'Beneficiary Name',
        'view_details': 'View Details',
        
        # Common
        'total': 'Total',
        'target': 'Target',
        'progress': 'Progress',
        'status': 'Status',
        'location': 'Location',
        'cost': 'Cost',
        'quantity': 'Quantity',
        'unit_price': 'Unit Price',
        'total_price': 'Total Price',
        'messages': {
            'no_data': 'No data available'
        }
    }
}

def get_text(key, lang='ar'):
    """Get translated text"""
    # Handle nested keys like 'sections.key_indicators'
    if '.' in key:
        keys = key.split('.')
        value = TRANSLATIONS.get(lang, {})
        for k in keys:
            value = value.get(k, {})
        return value if not isinstance(value, dict) else key
    
    return TRANSLATIONS.get(lang, {}).get(key, key)

def get_direction(lang='ar'):
    """Get text direction for language"""
    return 'rtl' if lang == 'ar' else 'ltr'

def get_alignment(lang='ar'):
    """Get text alignment for language"""
    return 'right' if lang == 'ar' else 'left'

def get_reverse_alignment(lang='ar'):
    """Get reverse text alignment for language"""
    return 'left' if lang == 'ar' else 'right'

"""
نظام مطابقة البنود وحساب التكاليف
يطابق البنود من الاستبيان مع جدول BOQs ويحسب التكاليف
"""
import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple


# خريطة المطابقة بين البنود الفرعية ومعرفات BOQs
ITEM_MAPPING = {
    # main_1: أعمال الغرف والتشطيبات الخارجية
    "1.1 أعمال هدم بسيط بالأدوات اليدوية": "w1_1",
    "1.2 إزالة الأنقاض": "w1_2",
    "1.3 أعمال بناء البلوك": "w1_3",
    "1.4 تصليح الأرضيات بالبيتون بدون قالب (250 كغ/م³)": "w1_4",
    "1.5 تصليح الأسقف بالبيتون مع القالب (350 كغ/م³)": "w1_5",
    "1.6 أعمال الطينة للجدران والأسقف": "w1_6",
    "1.7 صيانة الأبواب والشبابيك الموجودة مع الدهان": "w1_7",
    "1.8 تركيب زجاج صافي/مصنّفر للأبواب والشبابيك": "w1_8",
    "1.9 تقديم وتركيب منجور خشبي مع الإكسسوارات": "w1_9",
    "1.10 تقديم وتركيب منجور معدني مع الزجاج": "w1_10",
    "1.11 تقديم وتركيب منجور PVC": "w1_11",
    "1.12 تركيب وزرة رخام للأبواب (سماكة 3 سم)": "w1_12",
    "1.13 تركيب درابزونات ستانلس ستيل لذوي الاحتياجات الخاصة": "w1_13",
    "1.14 إنشاء رامب لذوي الاحتياجات الخاصة": "w1_14",
    
    # main_2: أعمال المطبخ ودورات المياه
    "2.1 تركيب خلاط مياه كروم مع قلب نحاسي": "w2_1",
    "2.2 تركيب سيراميك للأرضيات": "w2_2",
    "2.3 تركيب سيراميك للجدران": "w2_3",
    "2.4 تركيب مجلى موزاييك (2.2 م) مع وقافيات حجر": "w2_4",
    "2.5 تركيب مرحاض أرضي (بلاط)": "w2_5",
    "2.6 تركيب كرسي توالت": "w2_6",
    "2.7 تركيب حنفية مياه مفردة مع قلب نحاسي": "w2_7",
    "2.8 تركيب مغسلة سيراميك": "w2_8",
    "2.9 تركيب أسقف مستعارة": "w2_9",
    
    # main_3: أعمال الكهرباء
    "3.1 تأسيس كهربائي (حفر + أنابيب + علبا) بدون أسلاك": "w3_1",
    "3.2 أسلاك نحاسية 1 * 2 ملم": "w3_2",
    "3.3 تركيب مفاتيح إنارة": "w3_3",
    "3.4 بيضاء تركيب لمبات LED": "w3_4",
    "3.5 بطارية بسائلة 120 أمبير": "w3_5",
    "3.6 منظم شحن 20A / 24V فولت": "w3_6",
    "3.7 أسلاك شمسية نحاسية 6 كم * 7.3": "w3_7",
    "3.8 لوح طاقة شمسية 300 واط / 24V فولت": "w3_8",
    
    # main_4: أعمال التمديدات الصحية والسباكة
    "4.1 حفرة صحية جديدة (12*2 م)": "w4_1",
    "4.2 تركيب أنبوب صرف صحي 2 إنش": "w4_2",
    "4.3 تركيب أنبوب صرف صحي 4 إنش": "w4_3",
    "4.4 تركيب أنبوب صرف صحي 6 إنش": "w4_4",
    "4.5 تنظيف حفرة صحية يدوية/ميكانيكياً": "w4_5",
    "4.6 تركيب بالوعة ستانلس ستيل مع غطاء": "w4_6",
    
    # main_5: تمديدات المياه الحلوة
    "5.1 تركيب خزان مياه حلوة 1000 لتر": "w5_1",
    "5.2 تركيب خزان مياه حلوة 2000 لتر": "w5_2",
    "5.3 قطر 0 إنش PPR تركيب أنابيب": "w5_3",
    "5.4 قطر 1 إنش PPR تركيب أنابيب": "w5_4",
    "5.5 قطر 1.5 إنش PPR تركيب أنابيب": "w5_5",
    
    # main_6: أعمال عزل الأسطح
    "6.1 عزل مطاطي (أكريليك) للأسطح": "w6_1",
}


@st.cache_data
def load_boqs_with_mapping(file_path: str) -> pd.DataFrame:
    """
    تحميل بيانات BOQs مع إضافة معرف للمطابقة
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame مع بيانات BOQs ومعرفات المطابقة
    """
    try:
        df = pd.read_excel(file_path, sheet_name='BOQs2')
        
        # تنظيف البيانات
        df = df.dropna(how='all')
        
        # إضافة عمود المعرف إذا لم يكن موجوداً
        if 'ID' not in df.columns and len(df) > 0:
            # إنشاء معرفات تلقائية
            df['ID'] = [f"item_{i}" for i in range(len(df))]
        
        # تحويل الأعمدة الرقمية
        if 'Quantity' in df.columns:
            df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        
        if 'Unit Price USD' in df.columns:
            df['Unit Price USD'] = pd.to_numeric(df['Unit Price USD'], errors='coerce')
        
        # حساب التكلفة الإجمالية
        if 'Quantity' in df.columns and 'Unit Price USD' in df.columns:
            df['Total Price USD'] = df['Quantity'] * df['Unit Price USD']
        
        return df
        
    except Exception as e:
        st.error(f"خطأ في قراءة بيانات BOQs: {str(e)}")
        return pd.DataFrame()


def match_item_to_boq(item_description: str, boqs_df: pd.DataFrame) -> Tuple[str, float]:
    """
    مطابقة بند فرعي مع بند في BOQs والحصول على السعر
    
    Args:
        item_description: وصف البند الفرعي
        boqs_df: DataFrame بيانات BOQs
        
    Returns:
        (معرف البند في BOQs, السعر الإفرادي)
    """
    # البحث في خريطة المطابقة
    boq_id = ITEM_MAPPING.get(item_description, None)
    
    if boq_id and 'ID' in boqs_df.columns:
        # البحث عن البند في BOQs
        matched_row = boqs_df[boqs_df['ID'] == boq_id]
        
        if len(matched_row) > 0:
            unit_price = matched_row['Unit Price USD'].iloc[0]
            return boq_id, unit_price
    
    # إذا لم يتم العثور على مطابقة، محاولة البحث بالوصف
    if 'Item Description (AR)' in boqs_df.columns:
        # البحث عن تطابق جزئي في الوصف العربي
        for idx, row in boqs_df.iterrows():
            ar_desc = str(row.get('Item Description (AR)', ''))
            
            # استخراج الكلمات الرئيسية
            keywords = item_description.split()[:3]  # أول 3 كلمات
            
            match_found = all(keyword in ar_desc for keyword in keywords if len(keyword) > 2)
            
            if match_found:
                return row.get('ID', ''), row.get('Unit Price USD', 0)
    
    return None, 0.0


def calculate_house_cost(house_index: int, sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame) -> Dict:
    """
    حساب تكلفة منزل معين
    
    Args:
        house_index: رقم المنزل (_parent_index)
        sub_items_df: DataFrame البنود الفرعية
        boqs_df: DataFrame بيانات BOQs
        
    Returns:
        قاموس بتفاصيل التكلفة
    """
    # فلترة البنود الخاصة بهذا المنزل
    house_items = sub_items_df[sub_items_df['_parent_index'] == house_index]
    
    total_cost = 0.0
    items_breakdown = []
    
    for idx, item in house_items.iterrows():
        item_desc = item.get('البند الفرعي', '')
        quantity = item.get('الكمية', 0)
        
        # مطابقة مع BOQs
        boq_id, unit_price = match_item_to_boq(item_desc, boqs_df)
        
        # حساب التكلفة
        item_cost = quantity * unit_price
        total_cost += item_cost
        
        items_breakdown.append({
            'البند': item_desc,
            'الكمية': quantity,
            'السعر الإفرادي': unit_price,
            'التكلفة': item_cost,
            'BOQ_ID': boq_id
        })
    
    return {
        'total_cost': total_cost,
        'items_count': len(items_breakdown),
        'items': items_breakdown
    }


def calculate_all_houses_costs(sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame) -> pd.DataFrame:
    """
    حساب تكاليف جميع المنازل
    
    Args:
        sub_items_df: DataFrame البنود الفرعية
        boqs_df: DataFrame بيانات BOQs
        
    Returns:
        DataFrame مع تكاليف كل منزل
    """
    if '_parent_index' not in sub_items_df.columns:
        return pd.DataFrame()
    
    # الحصول على قائمة المنازل الفريدة
    house_indices = sub_items_df['_parent_index'].unique()
    
    costs_data = []
    
    for house_idx in house_indices:
        cost_info = calculate_house_cost(house_idx, sub_items_df, boqs_df)
        
        costs_data.append({
            'رقم المنزل': house_idx,
            'عدد البنود': cost_info['items_count'],
            'التكلفة التقديرية (USD)': cost_info['total_cost']
        })
    
    return pd.DataFrame(costs_data)


def get_cost_statistics(costs_df: pd.DataFrame) -> Dict:
    """
    حساب إحصائيات التكاليف
    
    Args:
        costs_df: DataFrame بتكاليف المنازل
        
    Returns:
        قاموس بالإحصائيات
    """
    if len(costs_df) == 0:
        return {}
    
    return {
        'الإجمالي': costs_df['التكلفة التقديرية (USD)'].sum(),
        'المتوسط': costs_df['التكلفة التقديرية (USD)'].mean(),
        'الأدنى': costs_df['التكلفة التقديرية (USD)'].min(),
        'الأعلى': costs_df['التكلفة التقديرية (USD)'].max(),
        'عدد المنازل': len(costs_df)
    }


@st.cache_data
def load_boqs_data(file_path: str) -> pd.DataFrame:
    """
    تحميل بيانات BOQs (اسم مستعار للتوافق)
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame مع بيانات BOQs
    """
    return load_boqs_with_mapping(file_path)


def calculate_total_cost(sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame) -> float:
    """
    حساب التكلفة الإجمالية لجميع المنازل
    
    Args:
        sub_items_df: DataFrame البنود الفرعية
        boqs_df: DataFrame بيانات BOQs
        
    Returns:
        التكلفة الإجمالية
    """
    costs_df = calculate_all_houses_costs(sub_items_df, boqs_df)
    if len(costs_df) > 0:
        return costs_df['التكلفة التقديرية (USD)'].sum()
    return 0.0


def get_cost_by_category(sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame) -> Dict[str, float]:
    """
    حساب التكاليف حسب الفئة
    
    Args:
        sub_items_df: DataFrame البنود الفرعية
        boqs_df: DataFrame بيانات BOQs
        
    Returns:
        قاموس بالتكاليف حسب الفئة
    """
    category_costs = {}
    
    if '_parent_index' not in sub_items_df.columns:
        return category_costs
    
    # الحصول على قائمة المنازل الفريدة
    house_indices = sub_items_df['_parent_index'].unique()
    
    for house_idx in house_indices:
        cost_info = calculate_house_cost(house_idx, sub_items_df, boqs_df)
        
        for item in cost_info['items']:
            # استخراج الفئة من البند
            item_desc = item['البند']
            category = item_desc.split('.')[0] if '.' in item_desc else 'أخرى'
            
            if category not in category_costs:
                category_costs[category] = 0.0
            
            category_costs[category] += item['التكلفة']
    
    return category_costs

"""
وحدة تحميل وحساب بيانات BOQs (Bill of Quantities)
"""
import pandas as pd
import streamlit as st
from typing import Dict, Tuple


@st.cache_data
def load_boqs_data(file_path: str) -> pd.DataFrame:
    """
    تحميل بيانات BOQs من Excel
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame مع بيانات BOQs
    """
    try:
        df = pd.read_excel(file_path, sheet_name='BOQs2')
        
        # تنظيف البيانات
        df = df.dropna(how='all')  # حذف الصفوف الفارغة بالكامل
        
        # تحويل الأعمدة الرقمية
        if 'Quantity' in df.columns:
            df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        
        if 'Unit Price USD' in df.columns:
            df['Unit Price USD'] = pd.to_numeric(df['Unit Price USD'], errors='coerce')
        
        # حساب التكلفة الإجمالية إذا لم تكن موجودة
        if 'Total Price USD' not in df.columns or df['Total Price USD'].isna().all():
            df['Total Price USD'] = df['Quantity'] * df['Unit Price USD']
        
        return df
        
    except Exception as e:
        st.error(f"خطأ في قراءة بيانات BOQs: {str(e)}")
        return pd.DataFrame()


def calculate_total_cost(df: pd.DataFrame) -> float:
    """
    حساب التكلفة الإجمالية
    
    Args:
        df: DataFrame مع بيانات BOQs
        
    Returns:
        التكلفة الإجمالية بالدولار
    """
    if 'Total Price USD' in df.columns:
        return df['Total Price USD'].sum()
    return 0.0


def get_cost_by_category(df: pd.DataFrame) -> Dict[str, float]:
    """
    حساب التكلفة حسب الفئة
    
    Args:
        df: DataFrame مع بيانات BOQs
        
    Returns:
        قاموس بالتكاليف حسب الفئة
    """
    if 'Item Description (AR)' in df.columns and 'Total Price USD' in df.columns:
        # استخراج الفئة من الوصف العربي
        costs = {}
        for idx, row in df.iterrows():
            desc = row.get('Item Description (AR)', '')
            cost = row.get('Total Price USD', 0)
            
            # تصنيف حسب الكلمة الأولى أو النمط
            if 'غرف' in desc or 'بناء' in desc or 'طينة' in desc:
                category = 'أعمال الغرف والتشطيبات'
            elif 'مطبخ' in desc or 'حمام' in desc or 'توالت' in desc:
                category = 'أعمال المطبخ ودورات المياه'
            elif 'كهرباء' in desc or 'كهربائي' in desc:
                category = 'أعمال الكهرباء'
            elif 'سباكة' in desc or 'صحية' in desc or 'مياه' in desc:
                category = 'أعمال السباكة'
            else:
                category = 'أعمال أخرى'
            
            costs[category] = costs.get(category, 0) + cost
        
        return costs
    
    return {}


def get_top_cost_items(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    الحصول على أعلى البنود تكلفة
    
    Args:
        df: DataFrame مع بيانات BOQs
        top_n: عدد البنود المطلوبة
        
    Returns:
        DataFrame مع أعلى البنود تكلفة
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # ترتيب حسب التكلفة
    sorted_df = df.sort_values('Total Price USD', ascending=False)
    
    # اختيار الأعمدة المهمة
    cols = []
    if 'Item Description (AR)' in sorted_df.columns:
        cols.append('Item Description (AR)')
    elif 'Item Description (EN)' in sorted_df.columns:
        cols.append('Item Description (EN)')
    
    if 'Unit' in sorted_df.columns:
        cols.append('Unit')
    if 'Quantity' in sorted_df.columns:
        cols.append('Quantity')
    if 'Unit Price USD' in sorted_df.columns:
        cols.append('Unit Price USD')
    if 'Total Price USD' in sorted_df.columns:
        cols.append('Total Price USD')
    
    return sorted_df[cols].head(top_n)

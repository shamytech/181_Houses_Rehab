"""
نظام حساب التكاليف من البنود الفرعية مباشرة
(التكلفة والسعر الإفرادي موجودين مباشرة في جدول البنود الفرعية)
"""
import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple


@st.cache_data
def load_boqs_with_mapping(file_path: str) -> pd.DataFrame:
    """
    تحميل بيانات BOQs (للتوافق - حالياً غير مستخدمة)
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame فارغ (البيانات تأتي من البنود الفرعية مباشرة)
    """
    # لم نعد نحتاج لتحميل BOQs2 لأن الأسعار موجودة في البنود الفرعية
    return pd.DataFrame()


def calculate_house_cost(house_index: int, sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame = None) -> Dict:
    """
    حساب تكلفة منزل معين من البنود الفرعية مباشرة
    
    Args:
        house_index: رقم المنزل (_parent_index)
        sub_items_df: DataFrame البنود الفرعية (تحتوي على السعر والإجمالي)
        boqs_df: (غير مستخدم - للتوافق فقط)
        
    Returns:
        قاموس بتفاصيل التكلفة
    """
    if sub_items_df is None or sub_items_df.empty:
        return {'total_cost': 0.0, 'items_count': 0, 'items': []}
    
    # فلترة البنود الخاصة بهذا المنزل
    house_items = sub_items_df[sub_items_df['_parent_index'] == house_index]
    
    total_cost = 0.0
    items_breakdown = []
    
    for idx, item in house_items.iterrows():
        item_desc = item.get('البند الفرعي', '')
        quantity = item.get('الكمية', 0)
        unit_price = item.get('السعر الافرادي', 0)
        item_total = item.get('الإجمالي', 0)
        
        # استخدام الإجمالي إذا كان موجوداً، وإلا نحسبه
        if item_total and item_total > 0:
            item_cost = item_total
        else:
            item_cost = quantity * unit_price
        
        total_cost += item_cost
        
        items_breakdown.append({
            'البند': item_desc,
            'الكمية': quantity,
            'السعر الإفرادي': unit_price,
            'التكلفة': item_cost
        })
    
    return {
        'total_cost': total_cost,
        'items_count': len(items_breakdown),
        'items': items_breakdown
    }


def calculate_all_houses_costs(sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    حساب تكاليف جميع المنازل من البنود الفرعية مباشرة
    
    Args:
        sub_items_df: DataFrame البنود الفرعية
        boqs_df: (غير مستخدم - للتوافق فقط)
        
    Returns:
        DataFrame مع تكاليف كل منزل
    """
    if sub_items_df is None or sub_items_df.empty:
        return pd.DataFrame()
    
    if '_parent_index' not in sub_items_df.columns:
        return pd.DataFrame()
    
    # الحصول على قائمة المنازل الفريدة
    house_indices = sub_items_df['_parent_index'].unique()
    
    costs_data = []
    
    for house_idx in house_indices:
        cost_info = calculate_house_cost(house_idx, sub_items_df)
        
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
    if costs_df is None or len(costs_df) == 0:
        return {}
    
    cost_col = 'التكلفة التقديرية (USD)'
    if cost_col not in costs_df.columns:
        return {}
    
    return {
        'الإجمالي': costs_df[cost_col].sum(),
        'المتوسط': costs_df[cost_col].mean(),
        'الأدنى': costs_df[cost_col].min(),
        'الأعلى': costs_df[cost_col].max(),
        'عدد المنازل': len(costs_df)
    }


@st.cache_data
def load_boqs_data(file_path: str) -> pd.DataFrame:
    """
    تحميل بيانات BOQs (للتوافق - غير مستخدمة)
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame فارغ
    """
    return load_boqs_with_mapping(file_path)


def calculate_total_cost(sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame = None) -> float:
    """
    حساب التكلفة الإجمالية لجميع المنازل
    
    Args:
        sub_items_df: DataFrame البنود الفرعية
        boqs_df: (غير مستخدم - للتوافق فقط)
        
    Returns:
        التكلفة الإجمالية
    """
    costs_df = calculate_all_houses_costs(sub_items_df)
    if len(costs_df) > 0:
        return costs_df['التكلفة التقديرية (USD)'].sum()
    return 0.0


def get_cost_by_category(sub_items_df: pd.DataFrame, boqs_df: pd.DataFrame = None) -> Dict[str, float]:
    """
    حساب التكاليف حسب الفئة (البند الرئيسي)
    
    Args:
        sub_items_df: DataFrame البنود الفرعية
        boqs_df: (غير مستخدم - للتوافق فقط)
        
    Returns:
        قاموس بالتكاليف حسب الفئة
    """
    if sub_items_df is None or sub_items_df.empty:
        return {}
    
    category_costs = {}
    
    # استخدام البند الرئيسي كفئة
    if 'البند الرئيسي' in sub_items_df.columns:
        for idx, item in sub_items_df.iterrows():
            category = item.get('البند الرئيسي', 'أخرى')
            item_total = item.get('الإجمالي', 0)
            
            if pd.isna(item_total):
                item_total = item.get('الكمية', 0) * item.get('السعر الافرادي', 0)
            
            if category not in category_costs:
                category_costs[category] = 0.0
            
            category_costs[category] += item_total
    
    return category_costs

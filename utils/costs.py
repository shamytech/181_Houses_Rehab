"""
نظام حساب التكاليف المبسط
يستخدم البيانات مباشرة من جدول rehab_sub_rep بدون مطابقة
"""
import pandas as pd
import streamlit as st
from typing import Dict


def calculate_house_cost_simple(house_index: int, sub_items_df: pd.DataFrame) -> Dict:
    """
    حساب تكلفة منزل معين من البيانات المباشرة
    
    Args:
        house_index: رقم المنزل (_parent_index)
        sub_items_df: DataFrame البنود الفرعية مع الأسعار
        
    Returns:
        قاموس بتفاصيل التكلفة
    """
    # فلترة البنود الخاصة بهذا المنزل
    house_items = sub_items_df[sub_items_df['_parent_index'] == house_index]
    
    total_cost = 0.0
    items_breakdown = []
    
    for idx, item in house_items.iterrows():
        item_desc = item.get('البند الفرعي', 'غير محدد')
        quantity = item.get('الكمية', 0)
        unit_price = item.get('السعر الافرادي', 0)
        item_total = item.get('الإجمالي', 0)
        
        # إذا لم يكن الإجمالي محسوب، احسبه
        if pd.isna(item_total) or item_total == 0:
            item_total = quantity * unit_price
        
        total_cost += item_total
        
        items_breakdown.append({
            'البند': item_desc,
            'الكمية': quantity,
            'السعر الإفرادي': unit_price,
            'التكلفة': item_total
        })
    
    return {
        'total_cost': total_cost,
        'items_count': len(items_breakdown),
        'items': items_breakdown
    }


def calculate_all_houses_costs_simple(sub_items_df: pd.DataFrame) -> pd.DataFrame:
    """
    حساب تكاليف جميع المنازل من البيانات المباشرة
    
    Args:
        sub_items_df: DataFrame البنود الفرعية مع الأسعار
        
    Returns:
        DataFrame مع تكاليف كل منزل
    """
    if sub_items_df is None or len(sub_items_df) == 0:
        return pd.DataFrame()
    
    if '_parent_index' not in sub_items_df.columns:
        return pd.DataFrame()
    
    # الحصول على قائمة المنازل الفريدة
    house_indices = sub_items_df['_parent_index'].unique()
    
    costs_data = []
    
    for house_idx in house_indices:
        cost_info = calculate_house_cost_simple(house_idx, sub_items_df)
        
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
    
    return {
        'الإجمالي': costs_df['التكلفة التقديرية (USD)'].sum(),
        'المتوسط': costs_df['التكلفة التقديرية (USD)'].mean(),
        'الأدنى': costs_df['التكلفة التقديرية (USD)'].min(),
        'الأعلى': costs_df['التكلفة التقديرية (USD)'].max(),
        'عدد المنازل': len(costs_df)
    }


def get_total_project_cost(sub_items_df: pd.DataFrame) -> float:
    """
    حساب التكلفة الإجمالية للمشروع
    
    Args:
        sub_items_df: DataFrame البنود الفرعية مع الأسعار
        
    Returns:
        التكلفة الإجمالية
    """
    if sub_items_df is None or len(sub_items_df) == 0:
        return 0.0
    
    # إذا كان عمود الإجمالي موجود، استخدمه مباشرة
    if 'الإجمالي' in sub_items_df.columns:
        total = sub_items_df['الإجمالي'].sum()
        if pd.notna(total) and total > 0:
            return total
    
    # وإلا احسب من الكمية × السعر
    if 'الكمية' in sub_items_df.columns and 'السعر الافرادي' in sub_items_df.columns:
        sub_items_df['calculated_total'] = sub_items_df['الكمية'] * sub_items_df['السعر الافرادي']
        return sub_items_df['calculated_total'].sum()
    
    return 0.0


def get_cost_by_main_item(sub_items_df: pd.DataFrame) -> Dict[str, float]:
    """
    حساب التكاليف حسب البند الرئيسي
    
    Args:
        sub_items_df: DataFrame البنود الفرعية مع الأسعار
        
    Returns:
        قاموس بالتكاليف حسب البند الرئيسي
    """
    if sub_items_df is None or len(sub_items_df) == 0:
        return {}
    
    if 'البند الرئيسي' not in sub_items_df.columns:
        return {}
    
    # تجميع حسب البند الرئيسي
    if 'الإجمالي' in sub_items_df.columns:
        costs = sub_items_df.groupby('البند الرئيسي')['الإجمالي'].sum().to_dict()
    elif 'الكمية' in sub_items_df.columns and 'السعر الافرادي' in sub_items_df.columns:
        sub_items_df['calculated_total'] = sub_items_df['الكمية'] * sub_items_df['السعر الافرادي']
        costs = sub_items_df.groupby('البند الرئيسي')['calculated_total'].sum().to_dict()
    else:
        costs = {}
    
    return costs

"""
وحدة تحميل ومعالجة البيانات من ملف Excel
"""
import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple
import os


@st.cache_data
def load_excel_data(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    تحميل جميع sheets من ملف Excel
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        قاموس يحتوي على DataFrames لكل sheet
    """
    try:
        # قراءة جميع الـ sheets
        excel_file = pd.ExcelFile(file_path)
        
        data = {}
        for sheet_name in excel_file.sheet_names:
            data[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)
            
        return data
    except Exception as e:
        st.error(f"خطأ في قراءة ملف Excel: {str(e)}")
        return {}


@st.cache_data
def load_houses_data(file_path: str) -> pd.DataFrame:
    """
    تحميل بيانات المنازل من الشيت الرئيسي
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame مع بيانات المنازل
    """
    try:
        # قراءة الشيت الرئيسي
        df = pd.read_excel(file_path, sheet_name='181-UNDP Houses Rehab Applic')
        
        # تنظيف البيانات
        df = clean_houses_data(df)
        
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة بيانات المنازل: {str(e)}")
        return pd.DataFrame()


def clean_houses_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    تنظيف ومعالجة بيانات المنازل
    
    Args:
        df: DataFrame الخام
        
    Returns:
        DataFrame منظف
    """
    # نسخ DataFrame لتجنب التعديل على الأصل
    df = df.copy()
    
    # تحويل تاريخ الارسال
    if 'تاريخ الارسال' in df.columns:
        df['تاريخ الارسال'] = pd.to_datetime(df['تاريخ الارسال'], errors='coerce')
    
    # تحويل الإحداثيات الجغرافية
    if '_إحداثيات الموقع الجغرافي للمنزل (GPS)_latitude' in df.columns:
        df['latitude'] = pd.to_numeric(
            df['_إحداثيات الموقع الجغرافي للمنزل (GPS)_latitude'], 
            errors='coerce'
        )
    
    if '_إحداثيات الموقع الجغرافي للمنزل (GPS)_longitude' in df.columns:
        df['longitude'] = pd.to_numeric(
            df['_إحداثيات الموقع الجغرافي للمنزل (GPS)_longitude'], 
            errors='coerce'
        )
    
    # تحويل الأرقام
    numeric_cols = [
        'عدد أفراد الأسرة (بما فيهم مالك المنزل)',
        'عدد الغرف (بما فيها الصالون)',
        'مساحة المنزل بالمتر المربع',
        'رقم الطابق الذي يقع فيه المنزل'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # إنشاء الاسم الكامل
    if all(col in df.columns for col in ['الاسم الأول', 'اسم الأب', 'الكنية']):
        df['الاسم الكامل'] = (
            df['الاسم الأول'].fillna('') + ' ' + 
            df['اسم الأب'].fillna('') + ' ' + 
            df['الكنية'].fillna('')
        ).str.strip()
    
    # تصنيف حالة الضرر إذا لم تكن موجودة
    if 'وصف حالة الضرر من وجهة نظرك كمالك للمنزل' in df.columns and 'حالة الضرر' not in df.columns:
        df['حالة الضرر'] = df['وصف حالة الضرر من وجهة نظرك كمالك للمنزل']
    
    # ملء القيم الفارغة
    df = df.fillna('')
    
    return df


@st.cache_data
def load_main_items(file_path: str) -> pd.DataFrame:
    """
    تحميل البنود الرئيسية
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame مع البنود الرئيسية
    """
    try:
        df = pd.read_excel(file_path, sheet_name='rehab_main_rep')
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة البنود الرئيسية: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_sub_items(file_path: str) -> pd.DataFrame:
    """
    تحميل البنود الفرعية
    
    Args:
        file_path: مسار ملف Excel
        
    Returns:
        DataFrame مع البنود الفرعية
    """
    try:
        df = pd.read_excel(file_path, sheet_name='rehab_sub_rep')
        
        # تحويل الأعمدة الرقمية
        numeric_cols = ['الكمية', 'السعر الافرادي', 'الإجمالي']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"خطأ في قراءة البنود الفرعية: {str(e)}")
        return pd.DataFrame()


def get_damage_status_counts(df: pd.DataFrame) -> Dict[str, int]:
    """
    حساب عدد المنازل حسب حالة الضرر
    
    Args:
        df: DataFrame بيانات المنازل
        
    Returns:
        قاموس بالإحصائيات
    """
    if 'حالة الضرر' not in df.columns:
        return {}
    
    counts = df['حالة الضرر'].value_counts().to_dict()
    return counts


def get_location_counts(df: pd.DataFrame) -> Dict[str, int]:
    """
    حساب عدد المنازل حسب المحافظة
    
    Args:
        df: DataFrame بيانات المنازل
        
    Returns:
        قاموس بالإحصائيات
    """
    if 'المحافظة' not in df.columns:
        return {}
    
    counts = df['المحافظة'].value_counts().to_dict()
    return counts


def get_house_type_counts(df: pd.DataFrame) -> Dict[str, int]:
    """
    حساب عدد المنازل حسب النوع
    
    Args:
        df: DataFrame بيانات المنازل
        
    Returns:
        قاموس بالإحصائيات
    """
    if 'نوع المنزل' not in df.columns:
        return {}
    
    counts = df['نوع المنزل'].value_counts().to_dict()
    return counts


def get_demographic_stats(df: pd.DataFrame) -> Dict[str, int]:
    """
    حساب الإحصائيات الديموغرافية
    
    Args:
        df: DataFrame بيانات المنازل
        
    Returns:
        قاموس بالإحصائيات
    """
    stats = {}
    
    # إجمالي الأسر
    stats['إجمالي الأسر'] = len(df)
    
    # إجمالي الأفراد
    if 'عدد أفراد الأسرة (بما فيهم مالك المنزل)' in df.columns:
        stats['إجمالي الأفراد'] = df['عدد أفراد الأسرة (بما فيهم مالك المنزل)'].sum()
    
    # عدد الرجال والنساء
    if 'عدد الرجال (العمر أكبر من 18 سنة)' in df.columns:
        stats['الرجال'] = df['عدد الرجال (العمر أكبر من 18 سنة)'].sum()
    
    if 'عدد النساء (العمر أكبر من 18 سنة)' in df.columns:
        stats['النساء'] = df['عدد النساء (العمر أكبر من 18 سنة)'].sum()
    
    # الأطفال
    if 'عدد الأطفال الذكور (دون سن 12 سنة)' in df.columns:
        stats['الأطفال الذكور'] = df['عدد الأطفال الذكور (دون سن 12 سنة)'].sum()
    
    if 'عدد الأطفال الإناث (دون سن 12 سنة)' in df.columns:
        stats['الأطفال الإناث'] = df['عدد الأطفال الإناث (دون سن 12 سنة)'].sum()
    
    # ذوي الإعاقة
    if 'عدد أفراد الأسرة من ذوي الإعاقة' in df.columns:
        stats['ذوي الإعاقة'] = df['عدد أفراد الأسرة من ذوي الإعاقة'].sum()
    
    # كبار السن
    if 'عدد أفراد الأسرة من كبار السن (60 سنة فأكثر)' in df.columns:
        stats['كبار السن'] = df['عدد أفراد الأسرة من كبار السن (60 سنة فأكثر)'].sum()
    
    return stats


def filter_houses(
    df: pd.DataFrame,
    governorate: str = None,
    region: str = None,
    damage_status: str = None,
    house_type: str = None
) -> pd.DataFrame:
    """
    فلترة المنازل حسب معايير محددة
    
    Args:
        df: DataFrame بيانات المنازل
        governorate: المحافظة
        region: المنطقة
        damage_status: حالة الضرر
        house_type: نوع المنزل
        
    Returns:
        DataFrame مفلتر
    """
    filtered_df = df.copy()
    
    if governorate and governorate != 'الكل':
        filtered_df = filtered_df[filtered_df['المحافظة'] == governorate]
    
    if region and region != 'الكل':
        filtered_df = filtered_df[filtered_df['المنطقة'] == region]
    
    if damage_status and damage_status != 'الكل':
        filtered_df = filtered_df[filtered_df['حالة الضرر'] == damage_status]
    
    if house_type and house_type != 'الكل':
        filtered_df = filtered_df[filtered_df['نوع المنزل'] == house_type]
    
    return filtered_df


def search_houses(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """
    البحث في بيانات المنازل
    
    Args:
        df: DataFrame بيانات المنازل
        search_term: نص البحث
        
    Returns:
        DataFrame مع النتائج
    """
    if not search_term:
        return df
    
    # البحث في عدة أعمدة
    search_columns = [
        'الاسم الكامل',
        'رقم الوثيقة الشخصية (الرقم الوطني)',
        'العنوان التفصيلي لمكان السكن الحالي',
        'القرية',
        'المحافظة',
        'المنطقة',
        'الناحية'
    ]
    
    mask = False
    for col in search_columns:
        if col in df.columns:
            mask |= df[col].astype(str).str.contains(search_term, case=False, na=False)
    
    return df[mask]

"""
معالجة وتحسين الصور
"""
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from typing import Optional


@st.cache_data(show_spinner=False)
def load_image_from_url(url: str, max_width: int = 800) -> Optional[Image.Image]:
    """
    تحميل صورة من URL مع تصغير تلقائي
    
    Args:
        url: رابط الصورة
        max_width: العرض الأقصى بالبكسل
        
    Returns:
        كائن PIL Image أو None عند الفشل
    """
    try:
        # تحميل الصورة
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # فتح الصورة
        img = Image.open(BytesIO(response.content))
        
        # تصغير الصورة إذا كانت أكبر من الحد الأقصى
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        return img
        
    except Exception as e:
        st.warning(f"فشل تحميل الصورة: {str(e)}")
        return None


def display_image_safe(url: str, caption: str = "", max_width: int = 800, use_container_width: bool = True):
    """
    عرض صورة بشكل آمن مع معالجة الأخطاء
    
    Args:
        url: رابط الصورة
        caption: تسمية توضيحية
        max_width: العرض الأقصى
        use_container_width: استخدام عرض الحاوية
    """
    if not url:
        st.info("لا توجد صورة متوفرة")
        return
    
    with st.spinner("جاري تحميل الصورة..."):
        img = load_image_from_url(url, max_width)
        
        if img:
            st.image(img, caption=caption, use_container_width=use_container_width)
        else:
            st.error("❌ فشل تحميل الصورة")


def create_image_gallery(image_urls: list, captions: list = None, columns: int = 3, max_width: int = 600):
    """
    إنشاء معرض صور
    
    Args:
        image_urls: قائمة روابط الصور
        captions: قائمة التسميات التوضيحية
        columns: عدد الأعمدة
        max_width: العرض الأقصى لكل صورة
    """
    if not image_urls:
        st.info("لا توجد صور متوفرة")
        return
    
    # التأكد من وجود تسميات
    if captions is None:
        captions = [f"صورة {i+1}" for i in range(len(image_urls))]
    
    # إنشاء صفوف من الأعمدة
    for i in range(0, len(image_urls), columns):
        cols = st.columns(columns)
        
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(image_urls):
                with col:
                    display_image_safe(
                        image_urls[idx],
                        caption=captions[idx] if idx < len(captions) else "",
                        max_width=max_width,
                        use_container_width=True
                    )


@st.cache_data(show_spinner=False)
def get_image_thumbnail(url: str, size: tuple = (200, 200)) -> Optional[Image.Image]:
    """
    الحصول على صورة مصغرة (thumbnail)
    
    Args:
        url: رابط الصورة
        size: حجم الصورة المصغرة (عرض، ارتفاع)
        
    Returns:
        كائن PIL Image أو None
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        return img
        
    except:
        return None

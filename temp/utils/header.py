"""
مكون الهيدر الموحد لجميع الصفحات
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
from utils.i18n import tm


def get_image_as_base64(image_path: str) -> str:
    """تحويل الصورة إلى base64 للاستخدام في HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""


def create_header(page_title: str = None):
    """
    إنشاء الهيدر الموحد للوحة التحكم
    يظهر في أعلى كل صفحة بدون فراغ
    
    Args:
        page_title: عنوان الصفحة الحالية (اختياري)
    """
    # مسارات الصور
    images_dir = Path(__file__).parent.parent / "images"
    binaa_logo = images_dir / "Binaa-logo-green_blue.png"
    undp_logo = images_dir / "UNDP-blue.png"
    
    # تحويل الصور إلى base64
    binaa_b64 = get_image_as_base64(str(binaa_logo))
    undp_b64 = get_image_as_base64(str(undp_logo))
    
    # الحصول على النصوص المترجمة
    project_code_label = tm.t('header.project_code')
    project_title_text = tm.t('header.project_title')
    last_update_label = tm.t('header.last_update')
    
    # حساب الارتفاع
    header_height = 125 if page_title else 75
    
    # HTML لعنوان الصفحة
    page_title_section = ""
    if page_title:
        page_title_section = f"""
        <div style="background: linear-gradient(135deg, #26A69A 0%, #009688 100%); padding: 5px 15px; margin: 0; border-bottom: 1px solid #00897B;">
            <h2 style="color: white; margin: 0; font-size: 16px; font-weight: 600; text-align: center;">{page_title}</h2>
        </div>
        """
    
    # إنشاء HTML للهيدر
    header_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .custom-header {{
                background: white;
                padding: 10px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 3px solid #00A0DC;
                margin: 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .header-left {{
                display: flex;
                align-items: center;
                gap: 15px;
            }}
            .header-center {{
                flex: 1;
                text-align: center;
                padding: 0 20px;
            }}
            .header-right {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .binaa-logo {{
                height: 55px;
            }}
            .undp-logo {{
                height: 55px;
            }}
            .project-code {{
                font-size: 15px;
                color: #666;
                margin: 2px 0 0 0;
            }}
            .project-title {{
                font-size: 12px;
                font-weight: bold;
                margin: 0;
                line-height: 1.3;
                color: #00558C;
            }}
            .update-info {{
                text-align: right;
                font-size: 15px;
                color: #666;
            }}
            .update-date {{
                font-weight: bold;
                color: #333;
                font-size: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="custom-header">
            <div class="header-left">
                <img src="data:image/png;base64,{binaa_b64}" class="binaa-logo" alt="BINAA">
                <div>
                    <p class="project-code">181-UNDP-R.Damascus-IDL-SH-48-2025</p>
                </div>
            </div>
            <div class="header-center">
                <p class="project-title">
                    {project_title_text}
                </p>
            </div>
            <div class="header-right">
                <div class="update-info">
                    <div class="update-date">12/4/2025 12:02:10 PM</div>
                    <div>{last_update_label}</div>
                </div>
                <img src="data:image/png;base64,{undp_b64}" class="undp-logo" alt="UNDP">
            </div>
        </div>
        {page_title_section}
    </body>
    </html>
    """
    
    # استخدام components.html لعرض HTML بشكل صحيح
    components.html(header_html, height=header_height, scrolling=False)

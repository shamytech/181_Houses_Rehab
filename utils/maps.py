"""
وحدة الخرائط التفاعلية
"""
import folium
from folium import plugins
import pandas as pd
from config import DAMAGE_STATUS, SUCCESS_GREEN, WARNING_YELLOW, DANGER_RED


def create_houses_map(df, tm=None, center=None, zoom=11):
    """
    إنشاء خريطة تفاعلية لمواقع المنازل
    
    Args:
        df: DataFrame بيانات المنازل
        tm: Translation Manager للترجمات
        center: مركز الخريطة [lat, lon]
        zoom: مستوى التقريب
        
    Returns:
        Folium map object
    """
    # تحديد المركز التلقائي إذا لم يتم تحديده
    if center is None:
        valid_coords = df[df['latitude'].notna() & df['longitude'].notna()]
        if len(valid_coords) > 0:
            center = [
                valid_coords['latitude'].mean(),
                valid_coords['longitude'].mean()
            ]
        else:
            center = [33.5138, 36.2765]  # دمشق
    
    # إنشاء الخريطة
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    
    # إضافة النقاط
    for idx, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        
        if pd.notna(lat) and pd.notna(lon):
            # تحديد اللون حسب حالة الضرر
            damage_status = row.get('حالة الضرر', 'غير محدد')
            color = get_marker_color(damage_status)
            
            # إنشاء النافذة المنبثقة
            popup_html = create_popup_html(row, tm)
            
            # إضافة العلامة
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
    
    return m


def get_marker_color(damage_status):
    """
    تحديد لون العلامة حسب حالة الضرر
    
    Args:
        damage_status: حالة الضرر
        
    Returns:
        كود اللون hex
    """
    status_config = DAMAGE_STATUS.get(damage_status, {})
    return status_config.get('color', '#2196F3')


def create_popup_html(row, tm=None):
    """
    إنشاء محتوى HTML للنافذة المنبثقة
    
    Args:
        row: صف من DataFrame
        tm: Translation Manager للترجمات
        
    Returns:
        HTML string
    """
    name = row.get('الاسم الكامل', 'غير محدد')
    area = row.get('المنطقة', 'غير محدد')
    damage = row.get('حالة الضرر', 'غير محدد')
    house_type = row.get('نوع المنزل', 'غير محدد')
    family_size = row.get('عدد أفراد الأسرة (بما فيهم مالك المنزل)', 'غير محدد')
    total = row.get('Grand Total', 'غير محدد')
    
    # الصورة الأمامية
    front_image = row.get('صورة الواجهة الأمامية للمنزل_URL', '')
    
    # تحديد الاتجاه والتسميات حسب اللغة
    if tm and tm.get_current_language() == 'en':
        direction = 'ltr'
        text_align = 'left'
        label_area = tm.t('map.popup.area')
        label_damage = tm.t('map.popup.damage_status')
        label_house_type = tm.t('map.popup.house_type')
        label_family_size = tm.t('map.popup.family_size')
        label_total = tm.t('map.popup.total')
    else:
        direction = 'rtl'
        text_align = 'right'
        label_area = tm.t('map.popup.area')
        label_damage = tm.t('map.popup.damage_status')
        label_house_type = tm.t('map.popup.house_type')
        label_family_size = tm.t('map.popup.family_size')
        label_total = tm.t('map.popup.total')
    
    html = f"""
    <div style='font-family: Cairo, sans-serif; direction: {direction}; text-align: {text_align};'>
        <h4 style='margin: 0 0 10px 0; color: #0D47A1;'>{name}</h4>
        <p style='margin: 5px 0;'><b>{label_area}:</b> {area}</p>
        <p style='margin: 5px 0;'><b>{label_damage}:</b> {damage}</p>
        <p style='margin: 5px 0;'><b>{label_house_type}:</b> {house_type}</p>
        <p style='margin: 5px 0;'><b>{label_family_size}:</b> {family_size}</p>
        <p style='margin: 5px 0;'><b>{label_total}:</b>{total}💲</p>
    """
    
    if front_image:
        html += f"""
        <img src='{front_image}' style='width: 100%; max-width: 250px; margin-top: 10px; border-radius: 5px;'>
        """
    
    html += "</div>"
    
    return html


def add_map_legend(m, tm=None):
    """
    إضافة مفتاح الخريطة
    
    Args:
        m: Folium map object
        tm: Translation Manager للترجمات
        
    Returns:
        Folium map with legend
    """
    # تحديد التسميات حسب اللغة
    if tm and tm.get_current_language() == 'en':
        legend_title = tm.t('map.legend.damage_status')
        light_damage = tm.t('map.legend.light_damage')
        medium_damage = tm.t('map.legend.medium_damage')
        severe_damage = tm.t('map.legend.severe_damage')
    else:
        legend_title = tm.t('map.legend.damage_status')
        light_damage = tm.t('map.legend.light_damage')
        medium_damage = tm.t('map.legend.medium_damage')
        severe_damage = tm.t('map.legend.severe_damage')
    
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; border-radius: 5px; padding: 10px;
                font-family: Cairo, sans-serif; color: #333333;">
        <p style="margin: 0 0 10px 0; font-weight: bold; color: #333333;">{legend_title}</p>
        <p style="margin: 5px 0; color: #333333;">
            <span style="background-color: {SUCCESS_GREEN}; 
                        width: 15px; height: 15px; 
                        display: inline-block; border-radius: 50%;"></span>
            {light_damage}
        </p>
        <p style="margin: 5px 0; color: #333333;">
            <span style="background-color: {WARNING_YELLOW}; 
                        width: 15px; height: 15px; 
                        display: inline-block; border-radius: 50%;"></span>
            {medium_damage}
        </p>
        <p style="margin: 5px 0; color: #333333;">
            <span style="background-color: {DANGER_RED}; 
                        width: 15px; height: 15px; 
                        display: inline-block; border-radius: 50%;"></span>
            {severe_damage}
        </p>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m


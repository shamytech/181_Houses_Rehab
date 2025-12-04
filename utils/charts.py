"""
wحدة المخططات والتصورات
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import *


def create_damage_pie_chart(damage_counts):
    """
    إنشاء مخطط دائري لتوزيع حالة الضرر
    
    Args:
        damage_counts: قاموس بأعداد المنازل حسب حالة الضرر
        
    Returns:
        Plotly figure
    """
    damage_df = pd.DataFrame(
        list(damage_counts.items()),
        columns=['الحالة', 'العدد']
    )
    
    color_map = {
        'ضرر خفيف': SUCCESS_GREEN,
        'ضرر متوسط': WARNING_YELLOW,
        'ضرر شديد': DANGER_RED
    }
    
    colors = [color_map.get(status, INFO_BLUE) for status in damage_df['الحالة']]
    
    fig = go.Figure(data=[go.Pie(
        labels=damage_df['الحالة'],
        values=damage_df['العدد'],
        marker=dict(colors=colors),
        textinfo='label+percent+value',
        textposition='auto',
        hole=0.3
    )])
    
    fig.update_layout(
        showlegend=True,
        height=400,
        font=dict(family="Cairo, sans-serif", size=14)
    )
    
    return fig


def create_location_bar_chart(location_counts):
    """
    إنشاء مخطط أعمدة للتوزيع الجغرافي
    
    Args:
        location_counts: قاموس بأعداد المنازل حسب الموقع
        
    Returns:
        Plotly figure
    """
    location_df = pd.DataFrame(
        list(location_counts.items()),
        columns=['الموقع', 'العدد']
    )
    
    fig = px.bar(
        location_df,
        x='الموقع',
        y='العدد',
        text='العدد',
        color='العدد',
        color_continuous_scale='Blues'
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="",
        yaxis_title="عدد المنازل",
        font=dict(family="Cairo, sans-serif", size=14)
    )
    
    return fig


def create_demographic_bar_chart(demo_stats):
    """
    إنشاء مخطط أعمدة للتوزيع الديموغرافي
    
    Args:
        demo_stats: قاموس بالإحصائيات الديموغرافية
        
    Returns:
        Plotly figure
    """
    demo_data = {
        'الفئة': ['الرجال', 'النساء', 'الأطفال الذكور', 'الأطفال الإناث'],
        'العدد': [
            demo_stats.get('الرجال', 0),
            demo_stats.get('النساء', 0),
            demo_stats.get('الأطفال الذكور', 0),
            demo_stats.get('الأطفال الإناث', 0)
        ]
    }
    
    demo_df = pd.DataFrame(demo_data)
    
    fig = px.bar(
        demo_df,
        x='الفئة',
        y='العدد',
        text='العدد',
        color='الفئة',
        color_discrete_sequence=[PRIMARY_BLUE, PRIMARY_LIGHT, SUCCESS_GREEN, INFO_BLUE]
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="",
        yaxis_title="العدد",
        font=dict(family="Cairo, sans-serif", size=14)
    )
    
    return fig


def create_house_type_pie_chart(house_type_counts):
    """
    إنشاء مخطط دائري لأنواع المنازل
    
    Args:
        house_type_counts: قاموس بأعداد المنازل حسب النوع
        
    Returns:
        Plotly figure
    """
    house_type_df = pd.DataFrame(
        list(house_type_counts.items()),
        columns=['النوع', 'العدد']
    )
    
    fig = go.Figure(data=[go.Pie(
        labels=house_type_df['النوع'],
        values=house_type_df['العدد'],
        marker=dict(colors=[PRIMARY_BLUE, PRIMARY_LIGHT, INFO_BLUE]),
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        showlegend=True,
        height=400,
        font=dict(family="Cairo, sans-serif", size=14)
    )
    
    return fig

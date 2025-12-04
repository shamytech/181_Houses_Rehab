"""
Styling system for multilingual support
"""

def get_rtl_css(lang='ar'):
    """Get RTL/LTR CSS based on language"""
    if lang == 'ar':
        return """
        <style>
        /* RTL Support */
        .main .block-container {
            direction: rtl;
            text-align: right;
        }
        
        .stSelectbox > div > div {
            text-align: right;
        }
        
        .stMultiSelect > div > div {
            text-align: right;
        }
        
        .stDataFrame {
            direction: rtl;
        }
        
        .stTable {
            direction: rtl;
        }
        
        .css-1d391kg {
            text-align: right;
        }
        
        .css-1lcbmhc {
            text-align: right;
        }
        
        /* Dashboard Cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .metric-label {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        /* Progress Bar */
        .progress-container {
            background: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-bar {
            background: linear-gradient(90deg, #4CAF50, #45a049);
            height: 20px;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        
        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 20px;
            border-radius: 15px;
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .close {
            color: #aaa;
            float: left;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        
        .close:hover {
            color: black;
        }
        
        /* Tab Styles */
        .tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
            border-radius: 10px 10px 0 0;
        }
        
        .tab button {
            background-color: inherit;
            float: right;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 16px;
        }
        
        .tab button:hover {
            background-color: #ddd;
        }
        
        .tab button.active {
            background-color: #4CAF50;
            color: white;
        }
        
        .tabcontent {
            display: none;
            padding: 20px;
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 10px 10px;
        }
        
        /* Image Gallery */
        .image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .image-item {
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .image-item img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .image-item:hover img {
            transform: scale(1.05);
        }
        
        /* BOQ Table */
        .boq-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .boq-table th,
        .boq-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: right;
        }
        
        .boq-table th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        
        .boq-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .boq-table tr:hover {
            background-color: #f5f5f5;
        }
        
        /* Search and Filter */
        .search-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        
        /* Status Colors */
        .status-nominated { background-color: #FF9800; }
        .status-studied { background-color: #2196F3; }
        .status-assigned { background-color: #9C27B0; }
        .status-rehabilitating { background-color: #FF5722; }
        .status-suspended { background-color: #795548; }
        .status-completed { background-color: #4CAF50; }
        
        </style>
        """
    else:
        return """
        <style>
        /* LTR Support */
        .main .block-container {
            direction: ltr;
            text-align: left;
        }
        
        .stSelectbox > div > div {
            text-align: left;
        }
        
        .stMultiSelect > div > div {
            text-align: left;
        }
        
        .stDataFrame {
            direction: ltr;
        }
        
        .stTable {
            direction: ltr;
        }
        
        /* Dashboard Cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .metric-label {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        /* Progress Bar */
        .progress-container {
            background: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-bar {
            background: linear-gradient(90deg, #4CAF50, #45a049);
            height: 20px;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        
        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 20px;
            border-radius: 15px;
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        
        .close:hover {
            color: black;
        }
        
        /* Tab Styles */
        .tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
            border-radius: 10px 10px 0 0;
        }
        
        .tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 16px;
        }
        
        .tab button:hover {
            background-color: #ddd;
        }
        
        .tab button.active {
            background-color: #4CAF50;
            color: white;
        }
        
        .tabcontent {
            display: none;
            padding: 20px;
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 10px 10px;
        }
        
        /* Image Gallery */
        .image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .image-item {
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .image-item img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .image-item:hover img {
            transform: scale(1.05);
        }
        
        /* BOQ Table */
        .boq-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .boq-table th,
        .boq-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        .boq-table th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        
        .boq-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .boq-table tr:hover {
            background-color: #f5f5f5;
        }
        
        /* Search and Filter */
        .search-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        
        /* Status Colors */
        .status-nominated { background-color: #FF9800; }
        .status-studied { background-color: #2196F3; }
        .status-assigned { background-color: #9C27B0; }
        .status-rehabilitating { background-color: #FF5722; }
        .status-suspended { background-color: #795548; }
        .status-completed { background-color: #4CAF50; }
        
        </style>
        """

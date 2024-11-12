import pandas as pd
import re


file = 'amazon.xlsx'
data = pd.read_excel(file, sheet_name='in')


def filter_num(num):
    filtered_num = re.sub(
        r'[^\d.]', '', 
        str(num)
    )
    return float(filtered_num) if filtered_num else None

def filter_text(text):
    remove_strange_characters_from_text = re.sub(
        r'[^\da-zA-Z.-?,\'\"/]+', ' ', 
        str(text)
    )
    start_text_with_alpha_numeric = re.sub(
        r'^[^A-Za-z\d]+', '', 
        remove_strange_characters_from_text
    )
    text_with_normalized_spaces = re.sub(
        r'\s+', ' ', 
        start_text_with_alpha_numeric
    ).strip()
    return text_with_normalized_spaces if text_with_normalized_spaces else None

def convert_to_sales_metric(value): #revenue #capital
    multiplier = len(data.get('user_id', 0))
    new_value = (value * multiplier)
    return new_value
    
try:
    data['discount_percentage'] = pd.to_numeric(data['discount_percentage'], errors = 'coerce')
    value_ = data['discount_percentage'][0]
    result = value_ * 3
    print(value_, result)
    for field in ['discounted_price', 'actual_price', 'rating', 'rating_count']:
        data[field] = data[field].apply(filter_num)
    for field in ['product_name', 'user_id']:
        data[field] = data[field].apply(filter_text)
    data['category'] = data['category'].apply(
        lambda text: text.strip().split('|')[0]
    )
    for field in ['discounted_price', 'actual_price']:
        data[field] = data[field].apply(convert_to_sales_metric)
    data = data.drop(
        columns=[
            'user_id',
            'img_link', 
            'review_title', 
            'review_id',
            'product_link',
            'about_product',
            'review_content',
            'product_id',
            'Unnamed: 3',
            'user_name'
        ]
    )
    data.rename(
        columns={
            'discounted_price': 'capital',
            'actual_price': 'revenue'
        },
        inplace=True
    )
except:
    import sys
    import traceback
        
    error_type, error_message, error_traceback = sys.exc_info()
    error_name = error_type.__name__
    frames = traceback.extract_tb(error_traceback)
    line_no = next(
        frame.lineno for frame in reversed(frames) 
        if frame.filename == __file__
    )
    print(f"{error_name} - {error_message} [line {line_no}]")


from ..constants import COLUMN_INFO, SHIPPING_COMPANY_SIGNATURE

def convert_order_number(df, shipping_company_name): 
    """홈사에 따른 주문번호 변환 함수"""
    
    column_name = COLUMN_INFO[shipping_company_name]['order_number']
    order_number_series = df[column_name].copy()
    signature = SHIPPING_COMPANY_SIGNATURE[shipping_company_name]
    
    order_number_series = signature + order_number_series.astype(str)
    
    df[column_name] = order_number_series
    
    return df
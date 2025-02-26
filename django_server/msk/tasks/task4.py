import pandas as pd

from ..constants import COLUMN_INFO

def get_exploded_df_list(df, shipping_company_name, item_info):
    
    df_list = []
    item_code_column_name = COLUMN_INFO[shipping_company_name]['item_code']
    
    # 상품코드를 정수형에서 문자열로 변경 
    df[item_code_column_name] = df[item_code_column_name].astype(str)
    
    for item_dict in item_info:
        
        # 넘어온 item_code를 기반으로 기존 Df에서 해당 item_code에 해당하는 df만 추출
        item_code = item_dict['item'].strip()
        filterd_df = df[df[item_code_column_name] == item_code].copy()
        filterd_df['sku'] = ''
        filterd_df['za04'] = ''
        
        new_rows = []
        
        for _, row in filterd_df.iterrows():
            
            main_sku = item_dict['sku']
            is_sub_sku_exist = item_dict['isSubSkuExist']
            
            main_sku_row = row.copy()
            main_sku_row['sku'] = main_sku
            new_rows.append(main_sku_row)
            
            if is_sub_sku_exist:
                for subsku_dict in item_dict['subSku']:
                    
                    sub_sku_row = row.copy()
                    
                    sub_sku = subsku_dict['subSku']
                    is_za04 = 'za04' if subsku_dict['isZa04'] else ''
                    
                    sub_sku_row['sku'] = sub_sku
                    sub_sku_row['za04'] = is_za04
                    new_rows.append(sub_sku_row)
            
        new_df = pd.DataFrame(new_rows)
        
        df_list.append(new_df)
    
    return df_list
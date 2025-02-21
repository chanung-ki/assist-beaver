from ..constants import COLUMN_INFO

def get_task_1_column_name(shipping_company_name):
    
    base_name = COLUMN_INFO[shipping_company_name]['base_name']
    sub_name = COLUMN_INFO[shipping_company_name]['sub_name']
    base_hp = COLUMN_INFO[shipping_company_name]['base_hp']
    sub_hp = COLUMN_INFO[shipping_company_name]['sub_hp']
    
    return base_name, sub_name, base_hp, sub_hp


def fill_name_and_hp(df, shipping_company_name):
    """인수자명, 전화번호 결측치 처리 함수"""
    
    ### 1. 인수자명 결측치 처리
    base_name, sub_name, base_hp, sub_hp = get_task_1_column_name(shipping_company_name)
    base_name_series = df[base_name].copy()
    sub_name_series = df[sub_name].copy()
    
    # * 혹은 성함확인중* 값을 가진 인덱스 추출    
    invalid_name_index = base_name_series.index[base_name_series == '*'].tolist() + base_name_series.index[base_name_series.str.contains('확인', na=False)].tolist()
    # 보조 컬럼에서 결측치 가져와서 처리
    base_name_series.loc[invalid_name_index] = sub_name_series.loc[invalid_name_index]
        
    
    ### 2. 전화번호 결측치 처리
    base_hp_series = df[base_hp].copy()
    sub_hp_series = df[sub_hp].copy()
    
    invalid_hp_index = base_hp_series.index[base_hp_series.str.strip() == ''].tolist()
    base_hp_series.loc[invalid_hp_index] = sub_hp_series.loc[invalid_hp_index]
    
    # 기존 컬럼 값을 가공된 컬럼으로 대체
    df[base_name] = base_name_series
    df[base_hp] = base_hp_series
    
    # 불필요한 컬럼 제거
    df.drop([sub_name, sub_hp], axis=1, inplace=True)

    return df
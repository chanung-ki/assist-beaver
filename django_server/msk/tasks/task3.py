import re
import pandas as pd

from ..constants import COLUMN_INFO

def get_address_df(df, shipping_company_name):
    """
        홈사에 따라 df에서 address df만 반환
    """
    column_name = COLUMN_INFO[shipping_company_name]['address']
    # try:
    #     # 주소가 공백인 행 제거
    #     df = df.dropna(subset=[column_name])
    # except:
    #     # 홈사와, 홈사파일을 일치시켜서 첨부하지 않은 경우 code=1 반환
    #     # ex 홈사 : CJ , 파일 : GS 파일
    #     return 1, None
    address_df = df[column_name]
    address_df = address_df.str.strip()

    return 0, address_df


def extract_road_name_address(address):
    """
        한 문장의 주소에서 정규식에 일치하는 도로명 주소를 반환해주는 함수
    """
    pattern = re.compile(r'[가-힣0-9]+(로|길)\s(\d{1,4}-\d{1,4}|\d+)')
    
    match = pattern.search(address)
    if match:
        full_address = match.group(0)  
        return full_address
    else:
        return None
    

def extract_old_address(address):
    """
        한 문장의 주소에서 정규식에 일치하는 번지수를 반환해주는 함수
    """
    pattern = re.compile(r'\d+-\d+번지|\d+번지')
    
    match = pattern.search(address)
    if match:
        old_address = match.group(0)  
        return old_address
    else:
        return None
    

def get_separated_address_df(address_df):
    
    result = []
    
    for address in address_df:
        
        # 주소에 공백이 두번 들어갔다면 한번으로 수정
        address = re.sub(r'\s+', ' ', address)
    
        # city 추출
        city = address.split()[0]
        
        # city를 제거한 나머지 주소
        remove_city_text = address.replace(city, '').strip()
        
        # 도로명 주소 추출
        road_name_address = extract_road_name_address(remove_city_text)
        
        if road_name_address:
            if remove_city_text.count(road_name_address) > 1:
                remove_city_text = remove_city_text.replace(road_name_address, '', 1).strip()
            split_text = remove_city_text.split(road_name_address)
            street = split_text[0] + road_name_address
            district = split_text[1].strip()
            category = ''
        else:
            category = '구주소'
            if not re.search(r'(아파트|\s\d+동|\d{1,4}호)', address):
                # 동, 혹은 호수가 없는 경우
                street = remove_city_text
                district = ''
            else:
                old_address = extract_old_address(address)
                if old_address:
                    old_address = old_address.strip()
                    # 번지수가 있어서 번지로 구분이 가능한 경우
                    split_old_text = remove_city_text.split(old_address)
                    street = split_old_text[0] + old_address
                    district = split_old_text[1].strip()
                else:
                    
                    street = ''
                    
                    city_category = ['시', '구', '군', '동', '읍', '면', '리']
                    for item in city_category:
                        pattern = re.compile(fr"([가-힣0-9]+({item}))\s")
                        match = pattern.search(remove_city_text)
                        if match:
                            temp_city = match.group(0)
                            street += temp_city
                            remove_city_text = remove_city_text.replace(temp_city, '')
                    
                        district = remove_city_text
            
        # 결과 저장
        result.append({
            'address': address,
            'city': city,
            'street': street,
            'district': district,
            '구주소 여부': category
        })
        
        
    return pd.DataFrame(result)


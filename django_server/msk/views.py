from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

import pandas as pd
import os
from io import BytesIO

from .utills import get_separated_address_df

# Create your views here.
def shipping(request):
    return render(request, 'shipping.html')

def table(request):
    return render(request, 'table.html')




# def test_address():
    
#     data_list = [
#         '경기 파주시 목동동 월드메르디앙1차아파트 209동 603호',
#         '경기도 화성시 마도면 석교리 제이2하우스B동305호',
#         '대구 달서구 성당동 포스코더샾 103동 1408호',
#         '전남 여수시 신기동 140번지 신화아파트 3동 1203호',
#         '인천 부평구 청천2동 대우아파트 121동 1603호',
#         '대전 서구 도안동 파랜하이트 109동 601호',
#         '부산 북구 화명동 롯데캐슬 카이져 502동 3103호',
#         '경기 안양시 만안구 안양6동 501-12번지 유앤어스빌 A동 303호',
#         '광주 서구 치평동 라인대주아파트상가 215동 112호 조은헤어샵',
#         '경기 광주시 목현동 430번지 104동201호',
#         '경기 안양시 동안구 비산2동 롯데캐슬 109동302호',
#         '대전 서구 관저동 느리울12단지 1205동1702호',
#         '경기 안산시 단원구 고잔동 힐스테이트중앙 108동 1701호',
#         '광주 서구 쌍촌동 1282번지 모아제일아파트 101동 1109호',
#         '서울 송파구 석촌동 287-15호 지하 102호',
#         '경기 시흥시 월곶동 풍림아파트2차 210동 1404호',
#         '서울 동대문구 이문동 이문 E-편한세상 아파트 102동 703호 ',
#         '인천 부평구 산곡4동 경남2차 201-107',
#         '경기 고양시 일산서구 덕이동 동문아파트 101-1302',
#         '전북 전주시 덕진구 인후동1가 아주마을제일아파트 202동 205호',
#         '경남 김해시 지내동 360번지 동원아파트 204동 605호',
#         '경남 김해시 삼계동 푸르지오3단지 307-603',
#         '서울 서대문구 홍은2동 186-1번지 미성아파트 1동 608호',
#         '경기 화성시 영천동 동탄파크자이아파트 333동 504호',
#         '서울 동대문구 전농1동 460-1번지 롯데캐슬노블레스 101동 905호',
#         '경기 용인시 기흥구 신갈동 412-30번지 102호',
#         '전남 목포시 상동 현대@ 102-702호',
#         '서울 은평구 진관동 은평뉴타운제각말아파트 501동 1202호',
#         '서울 성북구 월곡2동 월곡래미안루나밸리아파트 102동 102호',
#         '전남 영암군 삼호읍 용앙리 1688-24',
#         '전북 군산시 수송동 제일오투그란데2단지아파트 512-1204',
#         '경기 시흥시 대야동 569-1번지 우성아파트 201동 303호',
#         '광주 광산구 월계동 라인8차@ 803동 305호',
#         '전남 무안군 일로읍 오룡리 6번지 호반써밋 남악오룡 3차 302동 701호',
#         '서울 서대문구 북아현1동 720번지301호',
#         '경북 경주시 현곡면 라원리 0 아진아파트 103동 105호',
#         '서울 마포구 현석동 래미안 웰스트림 107동 504호',
#         '울산 울주군 범서읍 굴화리 산 75-1번지 문수산더샵아파트 105동 2201호',
#         '전북 남원시 도통동 부영1차아파트 106동 1402호',
#         '서울 은평구 응암3동 120-42번지 재원빌라 102호',
#         '대전 유성구 장대동 월드컵패밀리타운 103동 303호',
#         '경남 창원시 의창구 소계동 711-9',
#         '서울 서초구 방배4동 870~874',
#         '서울 강동구 천호동 301-29 201호',
#     ]
    
#     import re
#     from .utills import extract_old_address
    
    
#     for address in data_list:
        
#         city = address.split()[0]
#         # city를 제거한 나머지 주소
#         remove_city_text = address.replace(city, '').strip()
    
#         if not re.search(r'(아파트|\s\d+동|\d{1,4}호)', address):
#             # 동, 혹은 호수가 없는 경우
#             street = remove_city_text
#             district = ''
#         else:
#             old_address = extract_old_address(address)
#             if old_address:
#                 old_address = old_address.strip()
#                 # 번지수가 있어서 번지로 구분이 가능한 경우
#                 split_old_text = remove_city_text.split(old_address)
#                 street = split_old_text[0] + old_address
#                 district = split_old_text[1].strip()
#             else:
                
#                 street = ''
                
#                 city_category = ['시', '구', '군', '동', '읍', '면', '리']

#                 for item in city_category:
#                     pattern = re.compile(fr"([가-힣]+({item}))\s")
        
#                     match = pattern.search(remove_city_text)
#                     if match:
#                         temp_city = match.group(0)
#                         street += temp_city
#                         remove_city_text = remove_city_text.replace(temp_city, '')
                
#                     district = remove_city_text
                
            
#             print('=======')
#             print(address)
#             print(city)
#             print(street)
#             print(district)
#             print('=======')
                        
                   
                    
            


def separate_address(request):
    
    if not request.method == "POST":
        return HttpResponseNotAllowed(['POST'])
    
    uploaded_file = request.FILES.get('addressFile')
    if not uploaded_file:
        return JsonResponse({'error': '파일을 첨부 해주세요.'}, status=400)

    uploaded_file = request.FILES.get('addressFile')
    
    # 파일을 DataFrame으로 변환    
    df = pd.read_excel(uploaded_file)
    address_df = df['신주소']
    address_df.str.strip()
    
    # 도로가 분리된 DataFrame을 받은 후 파일로 만듬
    result_df = pd.DataFrame(get_separated_address_df(address_df))
    
    output = BytesIO()
    result_df.to_excel(output, index=False)
    output.seek(0)  # 파일 시작으로 이동

    # HttpResponse로 파일 반환
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="separated-address.xlsx"'
    
    return response
    
    # return redirect('msk_shipping')
    
    


"""
    파일 저장 방법 및 비교 방법
    
    1. 저장 방법
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    result_df = pd.DataFrame(result)
    output_path = os.path.join(BASE_DIR, 'new_output.xlsx')
    result_df.to_excel(output_path, index=False)
    
    2. 비교 방법
    
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # currnet_excel_path = os.path.join(BASE_DIR, 'current_output.xlsx')
    # new_excel_path = os.path.join(BASE_DIR, 'new_output.xlsx')
    
    # current_df = pd.read_excel(currnet_excel_path)
    # new_df = pd.read_excel(new_excel_path)
    
    # count = 0
    
    # if current_df.shape == new_df.shape:
    #     for i in range(len(current_df)):
    #         if not current_df.iloc[i].equals(new_df.iloc[i]):
    #             print(f"행 {i}가 다릅니다.")
    #             print("current_df:", current_df.iloc[i].to_dict())
    #             print("new_df    :", new_df.iloc[i].to_dict())
    #             count += 1
                
    # print(f'총 {count}행 다릅니다.')
"""
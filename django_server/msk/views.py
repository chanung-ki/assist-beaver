from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

import pandas as pd
import os
from io import BytesIO

from share.decorators import login_required
from .utills import get_separated_address_df


# Create your views here.
@login_required
def shipping(request):
    return render(request, 'shipping.html')

@login_required
def table(request):
    return render(request, 'table.html')

@login_required
def separate_address(request):
    try:
        if not request.method == 'POST':
            msg = '잘못된 접근입니다.'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('index')
        
        uploaded_file = request.FILES.get('addressFile')
        if not uploaded_file:
            msg = '파일을 첨부해주세요.'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('shipping')

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
    except:
        msg = '오류가 발생했습니다.'
        messages.add_message(request, messages.ERROR, msg)
        return redirect('shipping')
    


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
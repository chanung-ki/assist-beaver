from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
import json
import pandas as pd
import os
from io import BytesIO

from share.decorators import login_required
from .utills import get_df
from .tasks.task1 import fill_name_and_hp
from .tasks.task2 import convert_order_number
from .tasks.task3 import get_address_df, get_separated_address_df
from .tasks.task4 import get_exploded_df_list
from .constants import ERROR_MESSAGE, SHIPPING_COMPANY_NAME, REQUIRED_COLUMN

# Create your views here.
@login_required
def shipping_task(request):
    data = {'shipping_company_name' : SHIPPING_COMPANY_NAME}
    return render(request, 'shipping_task.html', data)


@login_required
def shipping_total(request):
    data = {'shipping_company_name' : SHIPPING_COMPANY_NAME}
    return render(request, 'shipping_total.html', data)


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

        shipping_company_name = request.POST.get('shippingCompanyName', '')
        if not shipping_company_name:
            msg = '홈사를 선택해주세요.'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('shipping_task')
        
        uploaded_file = request.FILES.get('addressFile')
        if not uploaded_file:
            msg = '파일을 첨부해주세요.'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('shipping_task')
        
        # 홈사에 따라 파일을 DataFrame으로 변환
        code, df = get_df(uploaded_file, shipping_company_name)
        if not code == 0:
            msg = ERROR_MESSAGE[code]['msg']
            messages.add_message(request, messages.ERROR, msg)
            return redirect('shipping_task')
        
        # df에서 address df만 정제해서 추출
        code, address_df = get_address_df(df, shipping_company_name)
        if not code == 0:
            msg = ERROR_MESSAGE[code]['msg']
            messages.add_message(request, messages.ERROR, msg)
            return redirect('shipping_task')
        
        # 도로가 분리된 df 받은 후 파일로 만듬
        result_df = get_separated_address_df(address_df)
        
        output = BytesIO()
        result_df.to_excel(output, index=False)
        output.seek(0)  # 파일 시작으로 이동

        # HttpResponse로 파일 반환
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        file_name = f'{shipping_company_name}-separated-address.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        return response
    except:
        msg = '오류가 발생했습니다.'
        messages.add_message(request, messages.ERROR, msg)
        return redirect('shipping_task')
    


@login_required
def convert_shipping_file(request):
    
    """
        try,
        error 메시지 추가하자!
    """

    if not request.method == 'POST':
        response = HttpResponseServerError('잘못된 접근입니다.')
        return response

    # 엑셀 파일
    uploaded_file = request.FILES.get("rawFile")
    # 출가 부가정보
    json_data = request.POST.get("jsonData")
    item_data = json.loads(json_data)
    # 상품 정보 추출
    item_info = item_data['items']
    # 홈사 정보 추출
    shipping_company_name = item_data['shippingCompanyNameValue']
    
    # 홈사에 따라 파일을 DataFrame으로 변환
    code, raw_df = get_df(uploaded_file, shipping_company_name)
    if not code == 0:
        msg = ERROR_MESSAGE[code]['msg']
        response = HttpResponseServerError(msg)
        return response
    
    df = raw_df.copy()
    
    """Task 0 - 불필요한 컬럼 제거"""
    required_column = REQUIRED_COLUMN[shipping_company_name]
    df = df[required_column]
    
    """Task 1 - 성함, 전화번호 작업"""
    df = fill_name_and_hp(df, shipping_company_name)
    
    """Task 2 - 주문번호 가공 작업"""
    df = convert_order_number(df, shipping_company_name)
    
    """Task 3 - 주소 분리 작업"""
    code, address_df = get_address_df(df, shipping_company_name)
    if not code == 0:
        msg = ERROR_MESSAGE[code]['msg']
        response = HttpResponseServerError(msg)
        return response
        
    # 도로가 분리된 df 받은 후 기존 df와 concat
    separated_df = get_separated_address_df(address_df)
    
    del separated_df['address']
    
    # 기존 df와 주소 df를 병합
    df = pd.concat([df.reset_index(drop=True), separated_df.reset_index(drop=True)], axis=1)
    
    """Task 4 - 상품 정보를 기반으로 sku별로 row 확장 작업"""
    try:
        df_list = get_exploded_df_list(df, shipping_company_name, item_info)
    except:
        response = HttpResponseServerError('갓디용,, 오류 발생 비버에게 문의하라')
        return response
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for idx, df in enumerate(df_list):
            sheet_name = f"Sheet{idx + 1}"  # 시트 이름을 동적으로 설정 (Sheet1, Sheet2, ...)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
    output.seek(0)  # 파일의 시작 부분으로 이동

    # HttpResponse로 파일 반환
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file_name = f'{shipping_company_name}.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    return response


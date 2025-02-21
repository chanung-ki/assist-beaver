from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
import os
from io import BytesIO

from share.decorators import login_required
from .utills import get_df
from .tasks.task1 import fill_name_and_hp
from .tasks.task2 import convert_order_number
from .tasks.task3 import get_address_df, get_separated_address_df
from .constants import ERROR_MESSAGE, SHIPPING_COMPANY_NAME, REQUIRED_COLUMN

# Create your views here.
@login_required
def shipping(request):
    
    data = {'shipping_company_name' : SHIPPING_COMPANY_NAME}
    return render(request, 'shipping.html', data)


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
            return redirect('msk_shipping')
        
        uploaded_file = request.FILES.get('addressFile')
        if not uploaded_file:
            msg = '파일을 첨부해주세요.'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('msk_shipping')
        
        # 홈사에 따라 파일을 DataFrame으로 변환
        code, df = get_df(uploaded_file, shipping_company_name)
        if not code == 0:
            msg = ERROR_MESSAGE[code]['msg']
            messages.add_message(request, messages.ERROR, msg)
            return redirect('msk_shipping')
        
        # df에서 address df만 정제해서 추출
        code, address_df = get_address_df(df, shipping_company_name)
        if not code == 0:
            msg = ERROR_MESSAGE[code]['msg']
            messages.add_message(request, messages.ERROR, msg)
            return redirect('msk_shipping')
        
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
        return redirect('msk_shipping')
    


@login_required
def convert_shipping_file(request):
    if not request.method == 'POST':
        msg = '잘못된 접근입니다.'
        messages.add_message(request, messages.ERROR, msg)
        return redirect('index')

    shipping_company_name = request.POST.get('shippingCompanyName', '')
    if not shipping_company_name:
        msg = '홈사를 선택해주세요.'
        messages.add_message(request, messages.ERROR, msg)
        return redirect('msk_shipping')
    
    uploaded_file = request.FILES.get('rawFile')
    if not uploaded_file:
        msg = '파일을 첨부해주세요.'
        messages.add_message(request, messages.ERROR, msg)
        return redirect('msk_shipping')
    
    
    # 홈사에 따라 파일을 DataFrame으로 변환
    code, raw_df = get_df(uploaded_file, shipping_company_name)
    if not code == 0:
        msg = ERROR_MESSAGE[code]['msg']
        messages.add_message(request, messages.ERROR, msg)
        return redirect('msk_shipping')
    
    df = raw_df.copy()
    
    """불필요한 컬럼 제거"""
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
        messages.add_message(request, messages.ERROR, msg)
        return redirect('msk_shipping')
    
    # 도로가 분리된 df 받은 후 기존 df와 concat
    separated_df = get_separated_address_df(address_df)
    del separated_df['address']
    df = pd.concat([df, separated_df], axis=1)
    
    """Task 4 - """


    # df_sheet1 = df.iloc[:50]  # 1~50행
    # df_sheet2 = df.iloc[50:]  # 51행 이후
    
    # output = BytesIO()
    
    # with pd.ExcelWriter(output, engine="openpyxl") as writer:
    #     df_sheet1.to_excel(writer, sheet_name="Sheet1", index=False)
    #     df_sheet2.to_excel(writer, sheet_name="Sheet2", index=False)
        
    #     writer._save()  # writer 종료 후 저장 (pandas 2.0 이상에서는 생략 가능)

    # output.seek(0)  # 파일의 시작 부분으로 이동

    # # HttpResponse로 파일 반환
    # response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # file_name = f'{shipping_company_name}.xlsx'
    # response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    # return response
    
    
    
    msg = '작업에 성공했습니다.'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('msk_shipping')

    # # 홈사에 따라 파일을 DataFrame으로 변환
    # code, address_df = get_address_df(uploaded_file, shipping_company_name)
    # if not code == 0:
    #     msg = ERROR_MESSAGE[code]['msg']
    #     messages.add_message(request, messages.ERROR, msg)
    #     return redirect('msk_shipping')
    
    # # 도로가 분리된 DataFrame을 받은 후 파일로 만듬
    # result_df = pd.DataFrame(get_separated_address_df(address_df))
    
    # output = BytesIO()
    # result_df.to_excel(output, index=False)
    # output.seek(0)  # 파일 시작으로 이동

    # # HttpResponse로 파일 반환
    # response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # file_name = f'{shipping_company_name}-separated-address.xlsx'
    # response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    # return response
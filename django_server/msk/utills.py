import os
import pandas as pd
import msoffcrypto
from io import BytesIO
import zipfile
from dotenv import load_dotenv

def get_df(uploaded_file, shipping_company_name):
    """
        홈사에 따라 엑셀파일에서 다른 로직을 통해 df 반환
    """
    if shipping_company_name == 'HD':
        # 파일을 메모리에서 읽기
        file_stream = BytesIO(uploaded_file.read())
        
        # 암호로 보호된 파일 열기
        load_dotenv()
        password = os.getenv("HD_PASSWORD")
        office_file = msoffcrypto.OfficeFile(file_stream)
        office_file.load_key(password=password)  # 암호 입력
        
        # 암호를 해제하여 파일 저장
        decrypted_file = BytesIO()
        office_file.decrypt(decrypted_file)
        
        # 암호가 해제된 파일을 다시 열기
        decrypted_file.seek(0)
        from openpyxl import load_workbook
        wb = load_workbook(decrypted_file)
        
        ws = wb.active
        data = ws.values
        columns = next(data)
        df = pd.DataFrame(data, columns=columns)
        # 컬럼에 개행이 있을경우 제거
        df.columns = [col.replace('\n', '') if col is not None else "" for col in df.columns]
        df = df.drop(0)
        
    else:
        try:
            if uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='xlrd')
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
        except zipfile.BadZipFile:
            # 홈사를 현대로 선택하지 않고 현대 파일을 첨부할 경우 BadZipFile 발생
            return 2, None
        
    return 0, df

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
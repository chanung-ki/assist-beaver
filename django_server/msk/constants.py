ERROR_MESSAGE = {
    1: {
        'msg' : '주소 컬럼을 찾을 수 없습니다. 다른 홈사 파일을 첨부하신것은 아닌지 확인해주세요.'
    },
    2: {
        'msg' : '파일에 비밀번호가 걸려있습니다. 다른 홈사 파일을 첨부하신것은 아닌지 확인해주세요.'
    },  
}

SHIPPING_COMPANY_NAME = [
    {
        'label': 'CJ',
        'value': 'CJ',
    },
    {
        'label': 'GS',
        'value': 'GS',
    },
    {
        'label': 'HD',
        'value': 'HD',
    },
]

# 주문번호 앞에 붙는 시그니처
SHIPPING_COMPANY_SIGNATURE = {
    'CJ': 'T-',
    'GS': 'T_',
    'HD': 'T'
}

# 각 홈사별 컬럼 정보
COLUMN_INFO = {
    'CJ' : {
        'address': '신주소',
        'base_name': '인수자',
        'sub_name': '주문자',
        'base_hp': '인수자hp',
        'sub_hp': '인수자tel',
        'order_number': '주문번호',
        'item_code': '상품코드'
    },
    'GS' : {
        'address': '수취인주소',
        'base_name': '주문자',
        'sub_name': '수취인',
        'base_hp': '주문자전화번호',
        'sub_hp': '수취인전화번호',
        'order_number': '주문번호',
        'item_code': '상품상세코드'
    },
    'HD' : {
        'address': '인수자 주소',
        'base_name': '인수자',
        'sub_name': '주문자',
        'base_hp': '인수자 HP',
        'sub_hp': '일반전화(인수자)',
        'order_number': '주문번호',
        'item_code': '상품'
    },
}

REQUIRED_COLUMN = {
    'CJ': [
        '배송확인',
        '인수자',
        '주문자',
        '인수자tel',
        '인수자hp',
        '주문번호',
        '상품코드',
        '상품명',
        '수량',
        '신주소',
        '신우편번호',
    ],
    'GS': [
        '주문확인',
        '주문자',
        '수취인',
        '주문자전화번호',
        '수취인전화번호',
        '주문번호',
        '상품상세코드',
        '상품명(송장)',
        '수량',
        '수취인주소',
        '우편번호',
    ],
    'HD': [
        '인수자',
        '주문자',
        '인수자 HP',
        '일반전화(인수자)',
        '주문번호',
        '상품',
        '상품명',
        '요청수량',
        '인수자 주소',
        '우편번호',
    ],
}


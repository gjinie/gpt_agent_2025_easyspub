#gpt가 최신 주가 정보에 기반하여 답변하도록 하려면, 필요한 기능을 함수로 만들어 펑션 콜링을 활용해야 함.
#회사의 기본 정보와 최신 주가 정보를 가져오고, 투자 의견을 알려주는 함수 만듷기

from datetime import datetime
import pytz
import yfinance as yf

def get_current_time(timezone: str = 'Asia/Seoul'):
    tz = pytz.timezone(timezone) # 타임존 설정
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    now_timezone = f'{now} {timezone}'
    print(now_timezone)
    return now_timezone

#회사 기본 정보 가져오는 함수
def get_yf_stock_info(ticker: str):
    stock = yf.Ticker(ticker) #가져올 회사 선택
    info = stock.info #가져온 정보를 출력
    print(info)
    return str(info) #딕셔너리 형태로 반환되어 gpt애 바로 전달할 수 없으므로, 문자열로 반환



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "해당 타임존의 날짜와 시간을 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'timezone': {
                        'type': 'string',
                        'description': '현재 날짜와 시간을 반환할 타임존을 입력하세요. (예: Asia/Seoul)',
                    },
                },
                "required": ['timezone'],
            },        
        }
    },
    {
        "type": "function", #get_yf_stock_info 함수의 설명을 tools에 추가하여 gpt에서 이 함수를 사용할 수 있도록 하기.
        "function": { #함수의 기능 정의
            "name": "get_yf_stock_info",
            "description": "해당 종목의 Yahoo Finance 정보를 반환합니다.", #함수에 대한 설명
            "parameters": { #함수가 입력으로 받을 파라미터 정의를 시작하는 부분 (gpt가 이 함수를 쓰려면 어떤 값을 넣어야 하는지 알려줌
                "type": "object", #파라미터 전체가 하나의 객체로 되어있다는 뜻
                "properties": { #파라미터 속정 정의
                    'ticker': { #함수에 넘겨줄 매개변수 이름
                        'type': 'string',
                        'description': 'Yahoo Finance 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)', #사용자로부터 받을 값을 더 잘 이해하도록 도와줌
                    },
                },
                "required": ['ticker'], #필수로 입력되어야 하는 파라미터 목록
            },        
        }
    }
]


if __name__ == '__main__':
    # get_current_time('America/New_York')
    info = get_yf_stock_info('AAPL') #애플
from gpt_functions import get_current_time, tools  #gpt_funtions 파일의 get_current_time함수와 tools 임포트
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키 가져오기

client = OpenAI(api_key=api_key)  # 오픈AI 클라이언트의 인스턴스 생성

def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",  # 응답 생성에 사용할 모델 지정
        messages=messages,  # 대화 기록을 입력으로 전달
        tools=tools,  # 사용 가능한 도구 목록 전달
    )
    return response  # 생성된 응답 내용 반환



messages = [
    {"role": "system", "content": "너는 사용자를 도와주는 상담사야."},  # 초기 시스템 메시지
]

while True:
    user_input = input("사용자\t: ")  # 사용자 입력 받기

    if user_input == "exit":  # 사용자가 대화를 종료하려는지 확인
        break
    
    messages.append({"role": "user", "content": user_input})  # 사용자 메시지 대화 기록에 추가
    
    ai_response = get_ai_response(messages, tools=tools)
    ai_message = ai_response.choices[0].message #객체 형태로 반환
    print(ai_message)  # ③ gpt에서 반환되는 값을 파악하기 위해 임시로 추가

    tool_calls = ai_message.tool_calls  # AI 응답에 포함된 tool_calls를 가져옵니다.
    if tool_calls:  # tool_calls가 있는 경우 (만약 gpt가 특정 함수를 실행해야 한다고 판단하면, ai_message의 tool_calls라는 속성에 실행할 함수 정보가 포함됨)
        for tool_call in tool_calls:
            tool_name = tool_call.function.name # 실행해야한다고 판단한 함수명 받기
            tool_call_id = tool_call.id         # tool_call 아이디 받기    
            arguments = json.loads(tool_call.function.arguments) # (1) 문자열을 딕셔너리로 변환    
            
            if tool_name == "get_current_time":  # ⑤ 만약 tool_name이 "get_current_time"이라면
                messages.append({
                    "role": "function",  # role을 "function"으로 설정
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": get_current_time(timezone=arguments['timezone']),  # 타임존 추가
                })
        messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})  # 함수 실행 완료 메시지 추가
        #gpt가 불필요하게 함수 호출을 반복하는 실수를 하기도 하므로 시스템 프롬프트를 활용해 이런 실수를 하지 않도록 가이드를 줌.
        #(for문이 종료되고 나면 함수 사용을 멈추고 답변을 생성하라는 의미의 시스템 프롬프트를 메시지에 추가)
        ai_response = get_ai_response(messages, tools=tools) # 다시 GPT 응답 받기
        ai_message = ai_response.choices[0].message

    messages.append(ai_message)  # AI 응답을 대화 기록에 추가하기

    print("AI\t: " + ai_message.content)  # AI 응답 출력

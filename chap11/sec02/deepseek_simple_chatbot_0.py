# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

llm = ChatOllama(model="deepseek-r1:14b") 

messages = [
    SystemMessage("너는 사용자를 도와주는 상담사야."),
]

while True:
    user_input = input("사용자: ")

    if user_input == "exit":
        break
    
    messages.append( 
        HumanMessage(user_input)
    )  
    
    ai_response = llm.invoke(messages)
    messages.append(
        ai_response
    )  

    print("AI: " + ai_response.content)

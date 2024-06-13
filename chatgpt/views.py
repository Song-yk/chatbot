from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from .models import UsageLog



def index(request):
    return render(request, 'gpt/index.html')

@csrf_exempt
def chat(request):
    # 세션을 가져오거나 새로 생성합니다.
    session_key = request.session.session_key
    if not session_key:
        request.session.save()

    # 대화 기록을 세션에서 가져옵니다.
    chat_history = request.session.get('chat_history', [])

    # 사용자의 질문을 가져옵니다.
    query = request.POST.get('question')

    # 대화 기록에 질문을 추가합니다.
    chat_history.append({'user': query})

    # 대화 기록을 업데이트합니다.
    request.session['chat_history'] = chat_history

    # Chroma 데이터베이스 초기화
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    database = Chroma(persist_directory="./database", embedding_function=embeddings)

    # ChatOpenAI 모델 초기화
    chat = ChatOpenAI(model="gpt-3.5-turbo")

    # RetrievalQA 초기화
    k = 3
    retriever = database.as_retriever(search_kwargs={"k": k})
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", output_key="result",
                                    return_messages=True)
    qa = RetrievalQA.from_llm(llm=chat, retriever=retriever, memory=memory, input_key="question", output_key="result",
                            return_source_documents=True)

    # ChatOpenAI의 모델을 사용하여 적절한 답변을 생성합니다.
    result = qa.invoke({"question": query, "chat_history": chat_history})

    # 대화 기록에 봇의 답변을 추가합니다.
    chat_history.append({'bot': result['result']})

    # 대화 기록을 업데이트합니다.
    request.session['chat_history'] = chat_history

    # 클라이언트에 대답을 반환합니다.
    return JsonResponse({"result": result['result']})

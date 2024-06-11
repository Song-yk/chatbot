from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django import forms
from django.urls import reverse
from django.utils import timezone

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory , ChatMessageHistory 
from langchain.schema import Document

import pandas as pd
import json

from django.views.decorators.csrf import csrf_exempt

from .models import UsageLog

# Create your views here.

# Chroma 데이터베이스 초기화 - 사전에 database가 완성 되어 있다는 가정하에 진행 - aivleschool_qa.csv 내용이 저장된 상태임
embeddings = OpenAIEmbeddings(model = "text-embedding-ada-002")
database = Chroma(persist_directory = "./database", embedding_function = embeddings)

#chatgpt API 및 lang chain을 사용을 위한 선언
chat = ChatOpenAI(model="gpt-3.5-turbo")
k = 3
retriever = database.as_retriever(search_kwargs={"k": k})
memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", output_key="result",
                                  return_messages=True)
qa = RetrievalQA.from_llm(llm=chat,  retriever=retriever,  memory=memory, input_key="question", output_key="result",
                          return_source_documents=True)

def index(request):
    return render(request, 'gpt/index.html')


@csrf_exempt
def chat(request):
    #post로 받은 question (index.html에서 name속성이 question인 input태그의 value값)을 가져옴
    query = request.POST.get('question')
    result = qa.invoke({"question":query})
    
    UsageLog.objects.create(question=query, answer=result["result"])

    return JsonResponse({"result": result["result"]})




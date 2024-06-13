from django.contrib import admin
from django.db import connections
from django import forms
from .models import UsageLog, Document
from django.db import transaction
import csv
import io
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document as LC_Document

import pandas as pd
# Register your models here.
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'question', 'answer')
    list_filter = ('timestamp',)
    search_fields = ('question', 'answer')
 

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('content', )
    search_fields = ('content',)
    actions = ['import_from_chroma', 'delete_from_chroma', 'insert_from_chroma']
    # list_per_page = 10
    

    def save_model(self, request, obj, form, change):
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        database = Chroma(persist_directory="./database", embedding_function=embeddings)

        # Django의 기본 save_model 메서드 호출
        if obj.content != '':
            if database.get()['embeddings'] is not None:    
                score = database.similarity_search_with_score(obj.content, 1)[0][1]
                print('score:', score)
                if score > 0.2:
                    database.add_documents([LC_Document(page_content=obj.content)])
                    Document.objects.create(content=obj.content)
            else:
                database.add_documents([LC_Document(page_content=obj.content)])
                Document.objects.create(content=obj.content)
            self.message_user(request, "Document added successfully to Chroma database.")
        
        temp = []
        if obj.csv_file:
            csv_file = pd.read_csv(obj.csv_file)
            for qa in csv_file["QA"]:
                database = Chroma(persist_directory="./database", embedding_function=embeddings)
                if database.get()['embeddings'] is not None:
                    score = database.similarity_search_with_score(qa, 1)[0][1]
                    print('score:', score)
                    if score > 0.2:
                        temp.append(qa)
                else:
                    temp.append(qa)
                    
            for qa in temp:
                database.add_documents([LC_Document(page_content=qa)])
                Document.objects.create(content=qa)
                    
    @transaction.atomic
    def import_from_chroma(self, request, queryset):
        with connections['chroma'].cursor() as cursor:
            cursor.execute("SELECT c0 FROM embedding_fulltext_search_content")
            rows = cursor.fetchall()
 
        if not rows:
            self.message_user(request, "No documents found in Chroma database.")
            return
 
        for row in rows:
            Document.objects.create(content=row[0])
 
        self.message_user(request, "Documents imported successfully.")
 
    import_from_chroma.short_description = "Import documents from Chroma"
 
    @transaction.atomic
    def delete_from_chroma(self, request, queryset):
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        database = Chroma(persist_directory="./database", embedding_function=embeddings)
        data = database.get()
        data = pd.DataFrame(data)
        
        delete_list = []
        with connections['default'].cursor() as cursor:
            for document in queryset:
                cursor.execute("DELETE FROM chatgpt_document WHERE content=%s", [document.content])
                print(document.content)
                temp = data[data['documents'] == document.content]['ids'].item()
                
                delete_list.append(temp)
        delete_list = list(set(delete_list))
        database.delete(ids=delete_list)

        # 선택된 Document 모델 인스턴스를 삭제
        queryset.delete()
        self.message_user(request, "Documents deleted successfully.")
        
        # with connections['chroma'].cursor() as cursor:
        #     cursor.execute("SELECT c0 FROM embedding_fulltext_search_content")
        #     rows = cursor.fetchall()
 
        # if not rows:
        #     self.message_user(request, "No documents found in Chroma database.")
        #     return
 
        # for row in rows:
        #     Document.objects.create(content=row[0])
        

    delete_from_chroma.short_description = "Delete documents and Chroma database"
 
    def changelist_view(self, request, extra_context=None):
        # 데이터가 없는 경우 자동으로 데이터 삽입
        if not Document.objects.exists():
            self.import_from_chroma(request, Document.objects.all())
        return super().changelist_view(request, extra_context)
 
admin.site.register(UsageLog, UsageLogAdmin)
admin.site.register(Document, DocumentAdmin)
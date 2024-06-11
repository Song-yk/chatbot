from django.contrib import admin
from django.urls import path

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


from .models import UsageLog, Document

# Register your models here.


class UsageLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'question', 'answer')
    list_filter = ('timestamp',)
    search_fields = ('question', 'answer')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'content')
    search_fields = ('content',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Chroma DB에 문서를 추가합니다.
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        chroma_db = Chroma(persist_directory="./database", embedding_function=embeddings)
        chroma_db.add_documents([{'page_content': obj.content, 'embedding': obj.embedding}])


admin.site.register(UsageLog, UsageLogAdmin)
admin.site.register(Document, DocumentAdmin)
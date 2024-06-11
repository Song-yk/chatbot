from django.db import models


class UsageLog(models.Model):
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.question}"

class Document(models.Model):
    content = models.TextField()
    # embedding = models.BinaryField()  # 실제 사용 시 적절한 데이터 타입을 선택
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.content[:50]}"

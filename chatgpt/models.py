from django.db import models


class UsageLog(models.Model):
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.question}"

class Document(models.Model):
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to='csv_files', null=True, blank=True)
    def __str__(self):
        return f"{self.created_at}: {self.content[:50]}"



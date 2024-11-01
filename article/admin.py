from django.contrib import admin
from .models import Question, Answer, Test

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Answer, AnswerAdmin)

class TestAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Test, TestAdmin)
# Register your models here.

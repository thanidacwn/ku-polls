"""Import admin and models from django.contrib and .models."""""
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    """ChoiceInline."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """QuestionAdmin."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'was_published_recently', 'end_date')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

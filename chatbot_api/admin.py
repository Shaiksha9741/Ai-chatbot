from django.contrib import admin
from .models import ChatHistory

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'user_message', 'bot_response')
    readonly_fields = ('timestamp',)

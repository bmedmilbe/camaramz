from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.UserTokens)
class UserTokensAdmin(admin.ModelAdmin):
    list_display = ['email']
    # search_fields = ['title']

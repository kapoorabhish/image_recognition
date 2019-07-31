from django.contrib import admin
from image_recognition.models import UserImageEmbeddings


@admin.register(UserImageEmbeddings)
class AdminUserImageEmbeddings(admin.ModelAdmin):
    list_display = ('person_name', 'image_embedding')
    search_fields = ('image_embedding', )
    
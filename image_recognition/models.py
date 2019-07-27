from django.db import models


class UserImageEmbeddings(models.Model):
    person_name = models.CharField(max_length=100)
    image_embedding = models.BinaryField()
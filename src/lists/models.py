from django.db import models
from django.urls import reverse
from django.conf import settings


# Create your models here.
class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="shared_user"
    )

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

    class Meta:
        unique_together = ("list", "text")
        ordering = ["id"]

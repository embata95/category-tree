from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    similar_to = models.ManyToManyField("self", blank=True, null=True, default=None)

    def __str__(self):
        if self.parent:
            return f"{self.name} in category {self.parent.name}"
        else:
            return self.name

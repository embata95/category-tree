from django.db import models
from django.db.models.signals import m2m_changed


def similar_to_changed(sender, action, pk_set, **kwargs):
    if action == "pre_add":
        if kwargs["instance"].id in pk_set:
            raise ValueError("Object can't be similar to itself")


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="images")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children"
    )
    similar_to = models.ManyToManyField("self", blank=True, default=None)

    def _prepare_related_fields_for_save(self, operation_name):
        for field in self._meta.concrete_fields:
            if field.is_relation and field.is_cached(self):
                obj = getattr(self, field.name, None)
                if not obj:
                    continue
                if obj.pk is None:
                    if not field.remote_field.multiple:
                        field.remote_field.delete_cached_value(obj)
                    raise ValueError(
                        "%s() prohibited to prevent data loss due to unsaved "
                        "related object '%s'." % (operation_name, field.name)
                    )
                elif getattr(self, field.attname) in field.empty_values:
                    setattr(self, field.attname, obj.pk)
                if getattr(obj, field.target_field.attname) != getattr(
                    self, field.attname
                ):
                    field.delete_cached_value(self)

        if self.parent_id and self.parent_id == self.id:
            raise ValueError("Can't set as self parent.")

    def __str__(self):
        return self.name


m2m_changed.connect(similar_to_changed, sender=Category.similar_to.through)

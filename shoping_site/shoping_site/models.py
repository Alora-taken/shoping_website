from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # Exclude soft-deleted items by default
        return super().get_queryset().filter(deleted_at__isnull=True)
    
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(null=True, blank=True)
    modified_at = models.DateTimeField(auto_now = True)
    modified_by = models.ForeignKey(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(null=True, blank=True)
    
    
    class Meta:
       abstract=True # Set this model as Abstract

    defman = models.Manager()
    objects = SoftDeleteManager()


    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()
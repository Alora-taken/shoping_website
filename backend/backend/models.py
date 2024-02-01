from typing import Any
from django.utils import timezone
from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(models.ForeignKey, null = True, blank = True)
    updated = models.DateTimeField(null = True, blank = True)
    updated_by = models.ForeignKey(models.ForeignKey, null = True, blank = True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null = True, blank = True)
    
    class Meta:
        abstract = True
        
    # def delete(self, using = None, keep_parents = False):
    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


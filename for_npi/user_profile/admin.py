from django.contrib import admin
from .models import Task, ProductionIssue, IssueFix
admin.site.register(Task)
admin.site.register(ProductionIssue)
admin.site.register(IssueFix)
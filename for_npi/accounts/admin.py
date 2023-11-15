from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'supervisor']
    list_filter = ['role', 'supervisor']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(supervisor=request.user)
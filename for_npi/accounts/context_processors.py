from django.contrib.auth.models import Group

def add_group_names(request):
    if request.user.is_authenticated:
        group_names = [group.name for group in request.user.groups.all()]
        return {'group_names': group_names}
    return {}
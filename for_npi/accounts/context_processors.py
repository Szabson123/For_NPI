from django.contrib.auth.models import Group

def is_supervisor(request):
    if not request.user.is_authenticated:
        return {'is_supervisor': False}
    return {'is_supervisor': request.user.groups.filter(name="Supervisor").exists()}
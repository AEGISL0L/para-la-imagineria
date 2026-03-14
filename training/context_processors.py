from .models import UserProfile


def user_profile(request):
    return {'profile': UserProfile.get_instance()}

import datetime
from rest_framework import permissions
from .models import UserActivity, Post


def user_activity(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            activity, created = UserActivity.objects.update_or_create(
                user = request.user,
                defaults = {
                    "last_request":datetime.datetime.now()
                }
            )
        return view(request, *args, **kwargs)
    return wrapper


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, post_obj):
        if request.method == 'GET':
            return True
        return post_obj.author.id == request.user.id
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from functools import wraps

def allowed_roles(roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):

            if request.user.is_authenticated:
                print("HIIIII !!!!")
                if hasattr(request.user, 'profile'):
                    if request.user.profile.role in roles:
                        return view_func(request, *args, **kwargs)
                    else:
                        messages.error(request, "You are not authorized to view this page.")
                        return redirect('/products/')
                else:
                    messages.error(request, "Profile not found.")
                    return redirect('/products/')
            else:
                return redirect(settings.LOGIN_URL)
        return wrapper_func
    return decorator

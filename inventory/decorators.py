from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from functools import wraps
from django.contrib.auth import get_user_model

def allowed_roles(roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):

            if request.user.is_authenticated:
                # Allow superusers or staff by default
                if request.user.is_superuser or request.user.is_staff:
                    return view_func(request, *args, **kwargs)
                # Ensure profile exists; if not, create a default one
                if not hasattr(request.user, 'profile'):
                    try:
                        from .models import Profile
                        Profile.objects.get_or_create(user=request.user)
                    except Exception:
                        messages.error(request, "Profile not found.")
                        return redirect('product_list')
                if hasattr(request.user, 'profile'):
                    if request.user.profile.role in roles:
                        return view_func(request, *args, **kwargs)
                    else:
                        messages.error(request, "You are not authorized to view this page.")
                        return redirect('product_list')
                else:
                    messages.error(request, "Profile not found.")
                    return redirect('product_list')
            else:
                return redirect(settings.LOGIN_URL)
        return wrapper_func
    return decorator

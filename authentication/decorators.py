from django.shortcuts import redirect
from django.http import HttpResponse

# decorator to restrict views for unauthenticated users only
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:  # checks if the user is logged in
            return redirect('home')  # if they are, redirect to home
        else:
            return view_func(request, *args, **kwargs)  # otherwise, allow access to the view
    return wrapper_func

# decorator to allow access only to users in specific groups
def allowed_users(allowed_roles=[]):  # accepts a list of roles that are allowed access
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():  # checks if the user belongs to any groups
                group = request.user.groups.all()[0].name  # gets the first group name the user belongs to

            if group in allowed_roles:  # if the group is in the allowed roles list
                return view_func(request, *args, **kwargs)  # grant access to the view
            else:
                return HttpResponse('You are not authorized to view this page')  # deny access
        return wrapper_func
    return decorator

# decorator for admin-only views, with tourist redirection and custom messages
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():  # checks if the user has any groups
            group = request.user.groups.all()[0].name  # grabs the first group name

        if group == 'tourist':  # tourists are redirected to the home page
            return redirect('home')
        elif group == 'admin':  # admins can access the view
            return view_func(request, *args, **kwargs)
        else:  # other users get a custom unauthorized message
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func

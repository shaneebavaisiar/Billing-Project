from django.shortcuts import redirect

def admin_only(func):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            return redirect('errorpage')
        else:
            return func(request,*args,**kwargs)
    return wrapper
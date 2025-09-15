from django.shortcuts import redirect

def rol_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('bodega:login')
        if getattr(request.user, 'rol', 'empleado') != 'admin':
            return redirect('bodega:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

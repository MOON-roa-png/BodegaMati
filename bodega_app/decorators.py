from django.shortcuts import redirect

def rol_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('bodega:login')
        if request.user.is_superuser or getattr(request.user, 'rol', 'empleado') == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('bodega:dashboard')
    return wrapper

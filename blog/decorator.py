from django.http import HttpResponseForbidden

def group_required(group_name):
    """
    Dekorátor pro kontrolu, zda uživatel patří do specifické skupiny.
    
    Args:
        group_name (str): Název skupiny, do které musí uživatel patřit
    
    Returns:
        function: Dekorátor, který ověří členství uživatele ve skupině
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Kontrola, zda uživatel patří do požadované skupiny
            if not request.user.groups.filter(name=group_name).exists():
                # Pokud uživatel není členem skupiny, vrátí chybu 403 Forbidden
                return HttpResponseForbidden("You do not have permission to access this page.")
            # Pokud uživatel je členem skupiny, pokračuje se v běžném zpracování požadavku
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


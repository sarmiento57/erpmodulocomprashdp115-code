from django.shortcuts import redirect

class ViewSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path == '/admin/' and 'view_site' in request.GET:
            return redirect('/solicitudCompra/')

        return response


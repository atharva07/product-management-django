from django.http import JsonResponse

# Create your views here.
def products(request):
    return JsonResponse({
        "message": "Products endpoint is working"
    })

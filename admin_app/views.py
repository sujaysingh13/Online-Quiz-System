from django.shortcuts import render

# Create your views here.
def admin_app_index(request):
    return render(request, 'admin_app/index.html')
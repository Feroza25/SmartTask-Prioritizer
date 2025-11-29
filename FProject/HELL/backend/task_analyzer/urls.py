from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "🚀 Smart Task Analyzer API is Running!",
        "endpoints": {
            "GET suggestions": "/api/tasks/suggest/",
            "POST analyze": "/api/tasks/analyze/",
            "admin": "/admin/"
        },
        "frontend": "Open frontend/index.html in browser"
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/tasks/', include('tasks.urls')),
]
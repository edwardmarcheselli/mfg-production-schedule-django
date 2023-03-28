from django.shortcuts import render

# Create your views here.
def schedule_display(request):
    return render(request, 'partials/index.html')
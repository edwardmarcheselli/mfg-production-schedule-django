from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRelease

# Create your views here.
def schedule_display(request):
    return render(request, 'partials/index.html')

def create_release(request):
    if request.method == 'POST':
        form = CreateRelease(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('schedule:schedule_display')
    else:
        form = CreateRelease()
    context = {
        'form' : form
    }

    return render(request, 'schedule/create_release.html', context) 
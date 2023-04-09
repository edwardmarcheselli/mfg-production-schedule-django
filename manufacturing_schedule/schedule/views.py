from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRelease
from .models import Release

# Create your views here.
def schedule_display(request):
    return render(request, 'partials/index.html')

def create_release(request):
    if request.method == 'POST':
        form = CreateRelease(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            priority_recalc()
            return redirect('schedule:schedule_display')
    else:
        form = CreateRelease()
    context = {
        'form' : form
    }

    return render(request, 'schedule/create_release.html', context)

def priority_recalc_doubles():
    def num_priority(e):
        return e.priority
    
    releases = Release.objects.filter()
    releases = list(releases)
    releases.sort(key=num_priority)
    #if a project is assigned the same priority number the most recent assignment takes precedent
    for release in releases:
        for comp_release in releases:
            if (release.priority == comp_release.priority):
                if (release.release_date > comp_release.release_date):
                    comp_release_inst = Release.objects.get(pk = comp_release.pk)
                    comp_release_inst.priority += 1
                    comp_release_inst.save()
                else:
                    release_inst = Release.objects.get(pk = release.pk)
                    release_inst.priority += 1
                    release_inst.save()
            else:
                pass

def priority_recalc():
    priority_recalc_doubles()

    def num_priority(e):
        return e.priority
    
    releases = Release.objects.filter()
    releases = list(releases)
    releases.sort(key=num_priority)
    for i, release in enumerate(releases):
        if (release.priority > i):
            release_inst = Release.objects.get(pk = release.pk)
            release_inst.priority = i
            release_inst.save()
        else:
            pass
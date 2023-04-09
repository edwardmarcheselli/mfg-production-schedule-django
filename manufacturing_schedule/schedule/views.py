from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRelease
from .models import Release, ScheduleItems
from bom.models import BOM, LineItemPart, Parts
from constants.models import ConstantVals
from datetime import datetime, date, timedelta

# Create your views here.
def schedule_display(request):
    schedule_line_items()
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

def release_sort_priority(releases_to_sort):
    def num_priority(e):
        return e.priority
    
    releases = list(releases_to_sort)
    releases.sort(key=num_priority)
    return releases

def priority_recalc_doubles():
    
    releases = Release.objects.filter()
    releases = release_sort_priority(releases)

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

    releases = Release.objects.filter()
    releases = release_sort_priority(releases)

    for i, release in enumerate(releases):
        if (release.priority > i):
            release_inst = Release.objects.get(pk = release.pk)
            release_inst.priority = i
            release_inst.save()
        else:
            pass

def schedule_line_items():
    releases = Release.objects.filter()
    releases = release_sort_priority(releases)
    for release in releases:
        rel_bom = release.bom
        rel_bom = BOM.objects.get(pk=rel_bom.pk)
        line_items_iter = rel_bom.line_items.all()
        #possibly use .iterator() if doesn't work
        for items in line_items_iter:
            if items.is_complete == False:
                for i in range(items.qty):
                    indiv_part = items.line_item_part
                    if indiv_part.is_purchased == False:
                        if indiv_part.routing1:
                            run_scheduling_routine(1, indiv_part.routing1, indiv_part.routing1_time, indiv_part, items, release)
                        if indiv_part.routing2:
                            run_scheduling_routine(2, indiv_part.routing2, indiv_part.routing2_time, indiv_part, items, release)
                        if indiv_part.routing3:
                            run_scheduling_routine(3, indiv_part.routing3, indiv_part.routing3_time, indiv_part, items, release)
                        if indiv_part.routing4:
                            run_scheduling_routine(4, indiv_part.routing4, indiv_part.routing4_time, indiv_part, items, release)
        #need to set release scheduled to true at the end of this for loop

#eventually to check if sub parts still in process items.lineitem_assembly_part
#have to check all in routing filter by date
#d = datetime.today() - timedelta(days=days_to_subtract)

def run_scheduling_routine(route_order, route_type, route_time, part, line_item, release):
    schedule_item = ScheduleItems.objects.create()
    schedule_item.schedule_part = part
    schedule_item.schedule_release = release
    schedule_item.routing = route_type
    scheduled = False
    d = date.today()
    work = route_time
    #print('enter while')
    #need to check if sub assembly parts are complete and max date
    subparts = list(line_item.lineitem_assembly_part.all())
    if len(subparts) > 0:
        for subpart in subparts:
            print(list(subpart.schedule_lineitems.all()))
            scheduled = True
    else:
        scheduled = True
        #schedule_lineitems.work_finish_datetime)
    #need to look out routing position and compare to former routing finish date if applicable


    #then need to step through rounting process backlog to find an opening for the part

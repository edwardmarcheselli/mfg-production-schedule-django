from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRelease
from .models import Release, ScheduleItems
from bom.models import BOM, LineItemPart, Parts
from constants.models import ConstantVals
from datetime import datetime, date, timedelta
from django.utils.timezone import make_aware
from django.conf import settings

# Create your views here.
def schedule_display(request):
    schedule_line_items()
    print('finish')
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
        #gets actual BOM instance from database
        rel_bom = BOM.objects.get(pk=rel_bom.pk)
        #grabs all line items in that BOM above
        line_items_iter = rel_bom.line_items.all()
        #possibly use .iterator() if doesn't work
        #iterates through each line item
        for items in line_items_iter:
            if items.is_complete == False:
                for i in range(items.qty):
                    indiv_part = items.line_item_part
                    if indiv_part.is_purchased == False:
                        if indiv_part.routing1:
                            route_inst1 = run_scheduling_routine(-1, 1, indiv_part.routing1, indiv_part.routing1_time, indiv_part, items, release)
                        if indiv_part.routing2:
                            route_inst2 = run_scheduling_routine(route_inst1, 2, indiv_part.routing2, indiv_part.routing2_time, indiv_part, items, release)
                        if indiv_part.routing3:
                            route_inst3 = run_scheduling_routine(route_inst2, 3, indiv_part.routing3, indiv_part.routing3_time, indiv_part, items, release)
                        if indiv_part.routing4:
                            route_inst4 = run_scheduling_routine(route_inst3, 4, indiv_part.routing4, indiv_part.routing4_time, indiv_part, items, release)
        #need to set release scheduled to true at the end of this for loop

#eventually to check if sub parts still in process items.lineitem_assembly_part
#have to check all in routing filter by date
#d = datetime.today() - timedelta(days=days_to_subtract)

def run_scheduling_routine(former_route, route, route_type, route_time, part, line_item, release):
    schedule_item = ScheduleItems.objects.create()
    schedule_item.schedule_part = part
    schedule_item.schedule_line_Item = line_item
    schedule_item.schedule_release = release
    schedule_item.routing = route_type
    schedule_item.routing_time = route_time
    scheduled = False
    d = datetime.today()
    work = route_time
    max_pred_date = 0
    #print('enter while')
    #need to check if sub assembly parts are complete and max date
    subparts = list(line_item.lineitem_assembly_part.all())
    if len(subparts) > 0:
        for subpart in subparts:
            if (len(list(subpart.schedule_lineitems.all()))):
                subpart_schedule_items = list(subpart.schedule_lineitems.all())
                for schedule_item in subpart_schedule_items:
                    if schedule_item.work_finish_datetime > max_pred_date:
                        max_pred_date = schedule_item.work_finish_datetime
    #need to look at routing position and compare to former routing finish date if applicable
    if former_route != -1:
        preroute_finish = former_route.work_finish_datetime
        if max_pred_date > 0:
            if preroute_finish > max_pred_date:
                max_pred_date = preroute_finish
    #then need to step through rounting process backlog to find an opening for the part
    all_items_in_route_type = ScheduleItems.objects.filter(routing = route_type)
    constants = ConstantVals.objects.latest('post_date')
    if route_type == 1:
        max_day_work_capacity = constants.laser_max_work
    elif route_type == 2:
        max_day_work_capacity = constants.weld_max_work
    elif route_type == 3:
        max_day_work_capacity = constants.press_max_work
    elif route_type == 4:
        max_day_work_capacity = constants.machine_max_work
    elif route_type == 5:
        max_day_work_capacity = constants.cut_max_work
    elif route_type == 6:
        max_day_work_capacity = constants.paint_max_work

    def filter_route_work_for_day(d, all_items_in_route_type):
        def is_in_date(day_route_item):
            if day_route_item.work_datetime == d:
                return True

        all_items_in_route_type =  list(all_items_in_route_type)
        route_type_items_day = filter(is_in_date, all_items_in_route_type)

        total_work_day = 0

        for route_item in route_type_items_day:
            total_work_day += route_item.routing_time

        return total_work_day
    
    while scheduled == False:
        total_work_day = filter_route_work_for_day(d, all_items_in_route_type)
        if (total_work_day + work) < max_day_work_capacity:
            settings.TIME_ZONE
            schedule_item.work_datetime = make_aware(d)
            next_day = d + timedelta(days=1)
            schedule_item.work_finish_datetime = make_aware(next_day)
            scheduled = True
        else:
            d += timedelta(days=1)
    

    schedule_item.save()
    return schedule_item
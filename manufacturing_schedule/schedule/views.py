from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRelease
from .models import Release, ScheduleItems
from bom.models import BOM, LineItemPart, Parts
from constants.models import ConstantVals
from datetime import datetime, date, timedelta
from django.utils.timezone import make_aware
from django.conf import settings
from json import dumps

# Create your views here.
def schedule_display(request):
    def routing_word_conversion(value):
        if value == 1:
            return'LASER'
        elif value == 2:
            return 'WELD'
        elif value == 3:
            return 'PRESS'
        elif value == 4:
            return 'MACHINE'
        elif value == 5:
            return 'CUT'
        elif value == 6:
            return 'PAINT'
        
    schedule_line_items()
    try:
        schedule_items = list(ScheduleItems.objects.values())
        keys = ['release', 'route', 'part', 'date']
        schedule_data = dict.fromkeys(keys)
        schedule_list = []
        for i, items in enumerate(schedule_items):
            schedule_data['release'] = str(Release.objects.get(pk=items['schedule_release_id']))
            schedule_data['route'] = routing_word_conversion(items['routing'])
            schedule_data['part'] = str(Parts.objects.get(pk = items['schedule_part_id']))
            schedule_data['date'] = str(items['work_datetime'].isoformat(' ', 'minutes'))
            schedule_list.append(schedule_data)
        #form list for JSONdump with the following Release, Route, Part, Date
    except:
        HttpResponse('error in schedule')
    dataJSON = dumps(schedule_list, default=str)
    context = {
        'schedule_items' : schedule_items,
        'data' : dataJSON
    }
    return render(request, 'schedule/schedule_timeline.html', context)

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

#function to reprioritize releases with the same priority (most recent release wins the priority spot)
def priority_recalc_doubles():
    
    releases = Release.objects.filter()
    releases = release_sort_priority(releases)

    there_is_change = 0
    #if a project is assigned the same priority number the most recent assignment takes precedent
    for release in releases:
        for comp_release in releases:
            if (release.priority == comp_release.priority):
                if (release.release_date > comp_release.release_date):
                    comp_release_inst = Release.objects.get(pk = comp_release.pk)
                    comp_release_inst.priority += 1
                    comp_release_inst.save()
                    there_is_change += 1
                else:
                    release_inst = Release.objects.get(pk = release.pk)
                    release_inst.priority += 1
                    release_inst.save()
                    there_is_change += 1
            else:
                pass
    #need to add the reschedule function
    #need to add changing the priority on the schedule items function

def priority_recalc():
    priority_recalc_doubles()

    releases = Release.objects.filter()
    releases = release_sort_priority(releases)

    #For loop makes sure that priority is rebased down to 1,2,3,4 not e.g. 4,6,8,9
    for i, release in enumerate(releases):
        if (release.priority > i):
            release_inst = Release.objects.get(pk = release.pk)
            release_inst.priority = i
            release_inst.save()
        else:
            pass
#this function is for new releases
def schedule_line_items():
    releases = Release.objects.filter()
    #sort the releases by their priority number so that as the schedule arranges the schedule items the higher priority get scheduled first
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
        release.scheduled = True
        release.save()
        #need to set release scheduled to true at the end of this for loop

#eventually to check if sub parts still in process items.lineitem_assembly_part
#have to check all in routing filter by date
#d = datetime.today() - timedelta(days=days_to_subtract)

def run_scheduling_routine(former_route, route, route_type, route_time, part, line_item, release):
    schedule_item = ScheduleItems.objects.create()
    #Initial Assignements
    schedule_item.schedule_part = part
    schedule_item.schedule_line_Item = line_item
    schedule_item.schedule_release = release
    schedule_item.routing = route_type
    schedule_item.routing_time = route_time
    if former_route != -1:
        schedule_item.preroute_schedule_item = former_route
        schedule_item.preroute_finish_datetime = former_route.work_finish_datetime
    #Initial Variables    
    scheduled = False
    d = datetime.today()
    d = make_aware(d)
    d += timedelta(days=1)
    d = d.replace(hour = 7, minute=0, second=0)
    work = route_time
    max_pred_date = d
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
        if preroute_finish > max_pred_date:
            max_pred_date = preroute_finish
    #change today's date to the max_date if max_date was changed from 0
    if type(max_pred_date) != int:
        if max_pred_date > d:
            d = max_pred_date
    #Find the max amount of work in a day for each worker that routing type + number of workers in the routing area
    all_items_in_route_type = list(ScheduleItems.objects.filter(routing = route_type))
    constants = ConstantVals.objects.latest('post_date')
    if route_type == 1:
        max_day_work_capacity = constants.laser_max_work
        worker_qty = constants.laser_worker_qty
    elif route_type == 2:
        max_day_work_capacity = constants.weld_max_work
        worker_qty = constants.weld_worker_qty
    elif route_type == 3:
        max_day_work_capacity = constants.press_max_work
        worker_qty = constants.press_worker_qty
    elif route_type == 4:
        max_day_work_capacity = constants.machine_max_work
        worker_qty = constants.machine_worker_qty
    elif route_type == 5:
        max_day_work_capacity = constants.cut_max_work
        worker_qty = constants.cut_worker_qty
    elif route_type == 6:
        max_day_work_capacity = constants.paint_max_work
        worker_qty = constants.paint_worker_qty

    max_time = []
    #setup the worker schedule max time object
    for i in range(worker_qty):
        max_time.append(d)

    #then need to step through rounting process backlog to find an opening for the part
    def filter_route_work_for_day(d, all_items_in_route_type):
        def is_in_date(day_route_item):
            if day_route_item.work_datetime.date() == d.date():
                return True

        def workers_work(items, w_num):
            if items.worker_num == w_num:
                return True

        route_type_items_day = list(filter(is_in_date, all_items_in_route_type))

        total_work_day = 0

        for route_item in route_type_items_day:
            total_work_day += route_item.routing_time

        if (total_work_day + work) < (max_day_work_capacity * worker_qty):
            for i in range(worker_qty):
                worker_parts = list(filter(lambda items: workers_work(items, i), route_type_items_day))
                worker_work_day = 0

                for w_item in worker_parts:
                    worker_work_day += w_item.routing_time

                if worker_work_day == 0:
                    return[i, d]

                elif (worker_work_day + work) < max_day_work_capacity:
                    worker_parts.sort(key=lambda x: x.work_finish_datetime, reverse=True)
                    worker_specific_d = worker_parts[0]
                    worker_specific_d = worker_specific_d.work_finish_datetime
                    if worker_specific_d.time() > d.time():
                        work_day_info = [i, worker_specific_d]
                        return work_day_info
                    else:
                        work_day_info = [i, d]
                        return work_day_info
                    
                    # schedule_item.work_datetime = work_day_info[1]
                    # finish_time = work_day_info[1] + timedelta(minutes=work)
                    # schedule_item.work_finish_datetime = finish_time
        return False
    
            # if route_item.work_finish_datetime.time() > d.time():
            #     date_string = route_item.work_finish_datetime.strftime("%H:%M:%S")
            #     tocompare = datetime.strptime(date_string, '%H:%M:%S')
            #     d = make_aware(datetime(d.year, d.month, d.day, tocompare.hour, tocompare.minute))
        
        

        return work_day_info
    #Once total work currently scheduled in the day and the latest time a part will finish in that day is determined
    while scheduled == False:
        work_day_info = filter_route_work_for_day(d, all_items_in_route_type)
        if work_day_info != False:
            schedule_item.worker_num = work_day_info[0]
            schedule_item.work_datetime = work_day_info[1]
            finish_time = work_day_info[1] + timedelta(minutes=work)
            schedule_item.work_finish_datetime = finish_time
            scheduled = True
        else:
            d += timedelta(days=1)
            d = d.replace(hour = 7, minute=0, second=0)
            for i in range(worker_qty):
                max_time[i] = d
    
    schedule_item.save()
    return schedule_item

#Need to add in rescheduling if priority order changes by checking items priority and only changing items in priority past the change
#Need to make sure that finished items are not rescheduled
#Need to add in scheduled True for already scheduled items
#Loop that looks at Releases new priority and makes sure that Schedule Items are reassigned the correct priority (then rescheduled)
#Change constants to include number of people and then hours to be per person


#Need to write scheduling function for rescheduling existing lineItems
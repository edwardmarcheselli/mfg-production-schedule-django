from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .forms import UploadFileForm
import logging
import math
import traceback

from .models import Parts, LineItemPart, BOM

logger = logging.getLogger(__name__)

# Create your views here.
# function that converts the routing to the corresponding model integer
def routing_conversion(value):
	if value == 'LASER':
		return 1
	elif value == 'WELD':
		return 2
	elif value == 'PRESS':
		return 3
	elif value == 'MACHINE':
		return 4
	elif value == 'CUT':
		return 5
	elif value == 'PAINT':
		return 6

def indented_bom_assembly(address_book):
	def add_match(items, addr ):
		key , value = items
		if key == addr:
			return True
		else:
			return False	

	for key in address_book:
		parent_addr = key.split('.')
		#checks do see that address has an up stream assembly address
		if (len(parent_addr) > 1):
			parent_addr.pop()
			parent_addr = '.'.join(parent_addr)
			#passes in all of the items in the bom and the parent address to then find the parent part
			filtered = dict(filter(lambda items: add_match(items, parent_addr),  address_book.items()))
			for i in filtered:
				inst = LineItemPart.objects.get(pk = address_book[key])
				parent_inst = LineItemPart.objects.get(pk = filtered[i])
				inst.assembly_address = parent_inst
				inst.save()
		else:
			pass
		

def handle_uploaded_file(csv_file, form_data):
	name = form_data['title']
	routing_fields = ['LASER', 'WELD', 'PRESS', 'MACHINE', 'CUT', 'PAINT']
	#test the file is a csv and that the file is not too big +2MB
	try:
		if not csv_file.name.endswith('.csv'):
			logging.getLogger("error_logger").error('File is not CSV type')
			return HttpResponseRedirect(reverse('bom:bom_upload/'))
		if csv_file.multiple_chunks():
			logging.getLogger("error_logger").error("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse('bom:bom_upload/'))
		#Creates a BOM instance to start loading line items into
		address_book = {}
		bom_inst = BOM.objects.create(bom_name=name)
		file_data = csv_file.read().decode("utf-8")
		lines = file_data.split("\n")
		lines.pop()
		#loop over the the BOM line items create parts in database and the use parts to create line items with corresponding quantities
		for count, line in enumerate(lines):
			fields = line.split(",")
			#skip header line then starts collecting data
			if fields[0] != 'address':
				part_inst = Parts.objects.create(internal_pn = fields[1], manufacturing_pn = fields[2], description = fields[3], color = fields[6], vendor1 = fields[7], vendor2 = fields[9], vendor3 = fields[11])
				if fields[5] != '':
					part_inst.weight = float(fields[5])
				if fields[8] != '':
					part_inst.cost1 = float(fields[8])
				if fields[10] != '':
					part_inst.cost2 = float(fields[10])
				if fields[12] != '':
					part_inst.cost3 = float(fields[12])
				#This '3' eventually needs to be made dynamic to match the number of routing phases currently set to three CVS template handles 4
				for i in range(4):
					val = 12 + i
					if fields[val].upper() in routing_fields:
						if val == 13:
							part_inst.routing1 = routing_conversion(fields[val])
						if val == 14:
							part_inst.routing2 = routing_conversion(fields[val])
						if val == 15:
							part_inst.routing3 = routing_conversion(fields[val])
						if val == 16:
							part_inst.routing4 = routing_conversion(fields[val])
				if fields[17] != '':
					part_inst.routing1_time = int(fields[17])
				if fields[18] != '':
					part_inst.routing2_time = int(fields[18])
				if fields[19] != '':
					part_inst.routing3_time = int(fields[19])
				if fields[20] != '':
					part_inst.routing4_time = int(fields[20])
				if fields[21] == 'ASSEM':
					part_inst.is_assembly = True
				elif fields[21] == 'PUR':
					part_inst.is_purchased = True
				part_inst.save()
				line_item_inst = LineItemPart.objects.create(line_item_part = part_inst, qty = int(fields[4]))
				line_item_inst.save()
				address_book[fields[0]] = line_item_inst.id
				bom_inst.line_items.add(line_item_inst)
		indented_bom_assembly(address_book)
		bom_inst.save()
	except Exception as e:
		#logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		print(e)
		print(traceback.format_exc())
	return 0

def bom_upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'], request.POST)
			return HttpResponseRedirect(reverse('schedule:schedule_display'))
	else:
		form = UploadFileForm()
	return render(request, 'bom/bom_upload.html', {'form' : form})
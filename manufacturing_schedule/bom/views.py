from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .forms import UploadFileForm
import logging

from .models import Parts, LineItemPart, BOM

logger = logging.getLogger(__name__)

# Create your views here.
# Imaginary function to handle an uploaded file.
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
	

def handle_uploaded_file(csv_file, form_data):
	name = form_data['title']
	routing_fields = ['LASER', 'WELD', 'PRESS', 'MACHINE', 'CUT', 'PAINT']
	print('entered upload procressing function')
	try:
		if not csv_file.name.endswith('.csv'):
			logging.getLogger("error_logger").error('File is not CSV type')
			return HttpResponseRedirect(reverse('bom:bom_upload/'))
		if csv_file.multiple_chunks():
			logging.getLogger("error_logger").error("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse('bom:bom_upload/'))
		print('passed csv checks')
		bom_inst = BOM.objects.create(bom_name=name)
		file_data = csv_file.read().decode("utf-8")
		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for count, line in enumerate(lines):
			print('entered lines for loop')
			print(count)
			fields = line.split(",")
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
				print('passed part inst 1')
				for i in range(3):
					val = 12 + i
					print('inside routing loop')
					if fields[val].upper() in routing_fields:
						print('inside routing types')
						if val == 13:
							part_inst.routing1 = routing_conversion(fields[val])
						elif val == 14:
							part_inst.routing2 = routing_conversion(fields[val])
						elif val == 15:
							part_inst.routing3 = routing_conversion(fields[val])
						elif val == 16:
							part_inst.routing4 = routing_conversion(fields[val])
				if fields[17] == 'ASSEM':
					part_inst.is_assembly = True
				elif fields[17] == 'PUR':
					part_inst.is_purchased = True
				part_inst.save()
				line_item_inst = LineItemPart.objects.create(line_item_part = part_inst, qty = int(fields[4]))
				line_item_inst.save()
				bom_inst.line_items.add(line_item_inst)
		bom_inst.save()
	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
	return HttpResponse('success')

def bom_upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'], request.POST)
			return HttpResponse('success')
	else:
		form = UploadFileForm()
	return render(request, 'bom/bom_upload.html', {'form' : form})
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
def handle_uploaded_file(csv_file, form_data):
	name = form_data['title']

	try:
		print('ran3')
		if not csv_file.name.endswith('.csv'):
			logging.getLogger("error_logger").error('File is not CSV type')
			return HttpResponseRedirect(reverse('bom:bom_upload/'))
        #if file is too large, return
		if csv_file.multiple_chunks():
			logging.getLogger("error_logger").error("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse('bom:bom_upload/'))
		
		bom_inst = BOM.objects.create(bom_name=name)

		file_data = csv_file.read().decode("utf-8")		

		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display

		for line in lines:						
			fields = line.split(",")
			part_inst = Parts.objects.create(internal_pn = fields[0], manufacturing_pn = fields[1], description = fields[2], weight = fields[3])
			part_inst.save()
			line_item_inst = LineItemPart.objects.create(line_item_part = part_inst, qty = 2)
			line_item_inst.save()
			bom_inst.line_items.add(line_item_inst)

			pass
		
		bom_inst.save()
    
	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))

	return HttpResponse('success')

def bom_upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			print('test2')
			handle_uploaded_file(request.FILES['file'], request.POST)
			return HttpResponse('success')
	else:
		form = UploadFileForm()
	return render(request, 'bom/bom_upload.html', {'form' : form})
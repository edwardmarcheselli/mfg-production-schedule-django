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
def handle_uploaded_file(csv_file):
	print('ran2')
	try:
		print('ran3')
		if not csv_file.name.endswith('.csv'):
			logging.getLogger("error_logger").error('File is not CSV type')
			return HttpResponseRedirect(reverse('bom:bom_upload/'))
        #if file is too large, return
		if csv_file.multiple_chunks():
			logging.getLogger("error_logger").error("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse('bom:bom_upload/'))

		file_data = csv_file.read().decode("utf-8")		

		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:						
			fields = line.split(",")
			data_dict = {}
			data_dict["name"] = fields[0]
			data_dict["start_date_time"] = fields[1]
			data_dict["end_date_time"] = fields[2]
			data_dict["notes"] = fields[3]
			logger.info(data_dict)
			print(data_dict)
			pass
			# try:
			# 	form = EventsForm(data_dict)
			# 	if form.is_valid():
			# 		form.save()					
			# 	else:
			# 		logging.getLogger("error_logger").error(form.errors.as_json())												
			# except Exception as e:
			# 	logging.getLogger("error_logger").error(repr(e))					
			# 	pass

	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))

	return HttpResponse('success')

def bom_upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		print('test1')
		print(form)
		if form.is_valid():
			print('test2')
			handle_uploaded_file(request.FILES['file'])
			return HttpResponse('success')
	else:
		form = UploadFileForm()
	return render(request, 'bom/bom_upload.html', {'form' : form})
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from reports.tools import *
from reports.forms import *
from django.views.decorators.csrf import csrf_exempt

def reports(request):

	form = DateFilterReport(request.POST or request.GET)
	_dict = {}
	initial_date = None
	final_date = None

	provinces = {
		"Valle del Cauca": "CO-VAC", "Bolivar": "CO-BOY",
		"Cesar": "CO-COR", "Huila": "CO-HUI",
		"Vaupes": "CO-VAU", "Norte de Santander": "CO-NSA",
		"Risaralda": "CO-RIS", "Vichada": "CO-VID",
		"Bogota": "CO-BOL", "Choco": "CO-CUN",
		"Guaviare": "CO-GUV", "Casanare":"CO-CAU",
		"Caqueta":"CO-CAS", "Caldas": "CO-CAQ",
		"Cauca": "CO-CES", "Santander": "CO-SAN",
		"Atlantico":"CO-ATL", "Amazonas": "CO-AMA",
		"Meta": "CO-MET", "Magdalena": "CO-MAG",
		"Arauca":"CO-ARA", "Guainia":"CO-GUA",
		"San Andres y Providencia":"CO-SAP", "Boyaca": "CO-CAL",
		"Quindio": "CO-QUI", "La Guajira": "CO-LAG",
		"Tolima": "CO-TOL", "Sucre": "CO-SUC",
		"Putumayo": "CO-PUT", "Narino": "CO-NAR",
		"Cordoba": "CO-CHO", "Cundinamarca": "CO-DC",
		"Antioquia": "CO-ANT",
	}

	if not form.is_valid():
		raise Exception("Form did not validate")
	
	if form.cleaned_data["initial_date"]:
		initial_date = form.cleaned_data["initial_date"]

	if form.cleaned_data["final_date"]:
		final_date = form.cleaned_data["final_date"]

	print "initial_date", initial_date
	print "final_date", final_date
	
	avg_time_medical = avgTimeMedical(initial_date, final_date)
	if avg_time_medical[0]['promedio_citas_medicas']:
		avg_time_medical = round(avg_time_medical[0]['promedio_citas_medicas'], 2)
	else:
		avg_time_medical = 0.0

	avg_time_surgeries = avgTimeSurgeries(initial_date, final_date)
	if avg_time_surgeries[0]['tiempo_espera_urgencia']:
		avg_time_surgeries = round(avg_time_surgeries[0]['tiempo_espera_urgencia'], 2)
	else:
		avg_time_surgeries = 0.0
	
	hospitals, regions = patientCare(initial_date, final_date)
	
	
	for i in regions:
		if provinces[i['departamento']]:
			_dict[provinces[i['departamento']]] = int(i['suma'])
	

	variables = RequestContext(request, {
		"avg_time_medical": avg_time_medical,
		"avg_time_surgeries": avg_time_surgeries,
		"hospitals": hospitals,
		"regions": _dict,
		"form": form,
		})
	return render_to_response("reports/home.html", variables)

#atencion de pacientes por periodo del anio
def attention_period(request):
	form = DateFilterReport(request.POST or request.GET)
	initial_date = None
	final_date = None
	data = attentionByPeriodOfYear(initial_date, final_date)
	by_clinic, by_medico = patientCarePeriodYear(initial_date, final_date)


	variables = RequestContext(request, {
		"data": data,
		"form": form,
		"by_clinic": by_clinic,
		"by_medico": by_medico,		
		})

	return render_to_response("reports/attention_period.html", variables)

@csrf_exempt
#atencion de pacientes por dia de la semana
def attention_day(request):
	form = DateFilterReport(request.POST or request.GET)
	initial_date = None
	final_date = None

	if not form.is_valid():
		raise Exception("Form did not validate")
	
	if form.cleaned_data["initial_date"]:
		initial_date = form.cleaned_data["initial_date"]

	if form.cleaned_data["final_date"]:
		final_date = form.cleaned_data["final_date"]


	print "initial_date==========", str(initial_date)
	print "final_date============", str(final_date)

	data = attentionByDayOfWeek(initial_date, final_date)

	variables = RequestContext(request, {
		"data": data,
		"form": form,
		})

	return render_to_response("reports/attention_day.html", variables)

#@csrf_exempt
def medicine_prescription(request):

	form = DateFilterReport(request.POST or request.GET)
	initial_date = None
	final_date = None

	if not form.is_valid():
		raise Exception("Form did not validate")
	
	if form.cleaned_data["initial_date"]:
		initial_date = form.cleaned_data["initial_date"]

	if form.cleaned_data["final_date"]:
		final_date = form.cleaned_data["final_date"]

	print "initial_date==========", str(initial_date)
	print "final_date============", str(final_date)

	avg_medicines = avgMedicines(initial_date, final_date)
	if avg_medicines[0]['precio']:
		avg_medicines = round(avg_medicines[0]['precio'], 2)
	else:
		avg_medicines = 0.0

	data = medicinePrescription(initial_date, final_date)


	variables = RequestContext(request, {
		"data": data,
		"avg_medicines": avg_medicines,
		"form": form,
		})
	
	return render_to_response("reports/medicine_prescription.html", variables)
	

def paymentsByCompany(request):
	form = DateFilterReport(request.POST or request.GET)
	initial_date = None
	final_date = None

	if not form.is_valid():
		raise Exception("Form did not validate")
	
	if form.cleaned_data["initial_date"]:
		initial_date = form.cleaned_data["initial_date"]

	if form.cleaned_data["final_date"]:
		final_date = form.cleaned_data["final_date"]

	print "initial_date==========", str(initial_date)
	print "final_date============", str(final_date)

	contributor, company = payments(initial_date, final_date)

	variables = RequestContext(request, {
		"contributor": contributor,
		"company": company,
		"form": form,
		})

	return render_to_response("reports/payments.html", variables)



def products_together(request):

	form = DateFilterReport(request.POST or request.GET)
	initial_date = None
	final_date = None

	if not form.is_valid():
		raise Exception("Form did not validate")
	
	if form.cleaned_data["initial_date"]:
		initial_date = form.cleaned_data["initial_date"]

	if form.cleaned_data["final_date"]:
		final_date = form.cleaned_data["final_date"]

	print "initial_date==========", str(initial_date)
	print "final_date============", str(final_date)

	data = productsTogether(initial_date, final_date)

	variables = RequestContext(request, {
		"data": data,
		"form": form,
		})

	return render_to_response("reports/products_together.html", variables)

def profilesEps(request):

	form = LimitFilterReport(request.POST or request.GET)
	limit = None

	if not form.is_valid():
		raise Exception("Form did not validate")

	if form.cleaned_data["limit"]:
		limit = form.cleaned_data["limit"]

	data = profiles(limit)

	estado_civil = {}
	sexo = {}
	escolaridad = {}
	estrato = {}
	_estado_civil = {}
	_sexo = {}
	_escolaridad = {}
	_estrato = {}
	l_estado_civil = []
	l_sexo = []
	l_escolaridad = []
	l_estrato = []
	total = 0

	for i in data:
		total += i['total']
		if i['estado_civil'] in estado_civil:
			estado_civil[i['estado_civil']] += i['total']
		else:
			estado_civil[i['estado_civil']] = i['total']
		
		if i['sexo'] in sexo:
			sexo[i['sexo']] += i['total']
		else:
			sexo[i['sexo']] = i['total']
		
		if i['nivel_escolaridad'] in escolaridad:
			escolaridad[i['nivel_escolaridad']] += i['total']
		else:
			escolaridad[i['nivel_escolaridad']] = i['total']
		
		if i['estrato'] in estrato:
			estrato[i['estrato']] += i['total']
		else:
			estrato[i['estrato']] = i['total']

	print "antes", estado_civil
	
	for key, value in estado_civil.iteritems():
		_estado_civil["value"] = round(float((value*100)/total), 2)
		_estado_civil["label"] = key.encode('utf-8')
		l_estado_civil.append(dict.copy(_estado_civil))

	for key, value in sexo.iteritems():
		_sexo["value"] = round(float((value*100)/total), 2)
		_sexo["label"] = key.encode('utf-8')
		l_sexo.append(dict.copy(_sexo))

	for key, value in escolaridad.iteritems():
		_escolaridad["value"] = round(float((value*100)/total), 2)
		_escolaridad["label"] = key.encode('utf-8')
		l_escolaridad.append(dict.copy(_escolaridad))

	for key, value in estrato.iteritems():
		_estrato["value"] = round(float((value*100)/total), 2)
		_estrato["label"] = key
		l_estrato.append(dict.copy(_estrato))
	
	print "despues", _estado_civil

	variables = RequestContext(request, {
		"data": data,
		"form": form,
		"estado_civil": l_estado_civil,
		"sexo": l_sexo,
		"escolaridad": l_escolaridad,
		"estrato": l_estrato,
		"total": total,
		})

	return render_to_response("reports/profiles.html", variables)


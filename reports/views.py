from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from reports.tools import attentionByPeriodOfYear,attentionByDayOfWeek,medicinePrescription
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def reports(request):
	from reports.tools import avgTimeMedical, avgTimeSurgeries, patientCare, patientCarePeriodYear
	_dict = {}
	provinces = {
		"Valle del Cauca": "CO-VAC",
		"Bolivar": "CO-BOY",
		"Cesar": "CO-COR",
		"Huila": "CO-HUI",
		"Vaupes": "CO-VAU",
		"Norte de Santander": "CO-NSA",
		"Risaralda": "CO-RIS",
		"Vichada": "CO-VID",
		"Bogota": "CO-BOL",
		"Choco": "CO-CUN",
		"Guaviare": "CO-GUV",
		"Casanare":"CO-CAU",
		"Caqueta":"CO-CAS",
		"Caldas": "CO-CAQ",
		"Cauca": "CO-CES",
		"Santander": "CO-SAN",
		"Atlantico":"CO-ATL",
		"Amazonas": "CO-AMA",
		"Meta": "CO-MET",
		"Magdalena": "CO-MAG",
		"Arauca":"CO-ARA",
		"Guainia":"CO-GUA",
		"San Andres y Providencia":"CO-SAP",
		"Boyaca": "CO-CAL",
		"Quindio": "CO-QUI",
		"La Guajira": "CO-LAG",
		"Tolima": "CO-TOL",
		"Sucre": "CO-SUC",
		"Putumayo": "CO-PUT",
		"Narino": "CO-NAR",
		"Cordoba": "CO-CHO",
		"Cundinamarca": "CO-DC",
		"Antioquia": "CO-ANT",
	}
	
	avg_time_medical = avgTimeMedical()
	avg_time_medical = round(avg_time_medical[0]['promedio_citas_medicas'], 2)

	avg_time_surgeries = avgTimeSurgeries()
	avg_time_surgeries = round(avg_time_surgeries[0]['tiempo_espera_urgencia'], 2)
	
	hospitals, regions = patientCare()
	by_clinic, by_medico = patientCarePeriodYear()
	
	for i in regions:
		if provinces[i['departamento']]:
			_dict[provinces[i['departamento']]] = int(i['suma'])
	
	"""
    data_graphic = {
        "labels": [],
        "datasets": [],
    }
    data_set = {
        "label": "",
        "type": "",
        "data": "",
        "backgroundColor": "#F7BE81",
    }

    list_data_set = []
    index = 0
    for c in by_clinic:
        #index += 1
        data_label = []
        for i in list_data:
            for j in i["data"]:
                if j["label"] == c.name:
                    data_label.append(j["percentage"])
        data_set["label"] = c.name
        data_set["type"] = "bar"
        data_set["data"] = data_label
        data_set["backgroundColor"] = list_colors[index]
        list_data_set.append(dict.copy(data_set))
        index += 1
    data_graphic["labels"] = labels
    data_graphic["datasets"] = list_data_set
    """

	variables = RequestContext(request, {
		"avg_time_medical": avg_time_medical,
		"avg_time_surgeries": avg_time_surgeries,
		"hospitals": hospitals,
		"regions": _dict,
		"by_clinic": by_clinic,
		"by_medico": by_medico,
		})
	return render_to_response("reports/home.html", variables)

#atencion de pacientes por periodo del anio
def attention_period(request):
	data = attentionByPeriodOfYear()
	return render_to_response("reports/attention_period.html",{"data":data})

@csrf_exempt
#atencion de pacientes por dia de la semana
def attention_day(request):	
	if request.method == 'POST':
		data = attentionByDayOfWeek(request.POST['fecha1'], request.POST['fecha2'])
	else:
		data = attentionByDayOfWeek()
	return render_to_response("reports/attention_day.html",{"data":data})

@csrf_exempt
def medicine_prescription(request):
	if request.method == 'POST':
		data = medicinePrescription(request.POST['fecha1'], request.POST['fecha2'])
	else:
		data = medicinePrescription()
	return render_to_response("reports/medicine_prescription.html",{"data":data})

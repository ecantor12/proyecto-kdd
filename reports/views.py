from django.shortcuts import render

# Create your views here.

def reports(request):
	from reports.tools import avgTime
	avg_time = avgTime()
	avg_time = round(avg_time[0]['promedio_citas_medicas'], 2)

	return render(request, 'reports/home.html', {"avg_time": avg_time})


#def avg():
	
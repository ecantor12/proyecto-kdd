from django.db import connection, transaction

#Function to convert tuple's lists of dict's objects
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def avgTimeMedical():
	#from django.db import connection, transaction
	cursor = connection.cursor()
	query = "SELECT avg(tiempo_espera/3600) AS promedio_citas_medicas FROM citas_medicas"

	cursor.execute(query)
	rows = dictfetchall(cursor)
	
	return rows

def avgTimeSurgeries():
	#from django.db import connection, transaction
	cursor = connection.cursor()
	query = "SELECT avg(tiempo_espera)/3600 as tiempo_espera_urgencia from urgencia"

	cursor.execute(query)
	rows = dictfetchall(cursor)
	
	return rows

def patientCare():
	cursor1 = connection.cursor()
	cursor2 = connection.cursor()
	query1 = "SELECT departamento,municipio,nombre,idips, sum(conteo) as suma from ((SELECT ips.nombre, ips.municipio, ips.departamento, ips.idips, hospitalizacion.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN hospitalizacion ON ips.idips = hospitalizacion.ips_idips GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, hospitalizacion.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN citas_medicas ON ips.idips = citas_medicas.ips_idips GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN urgencia ON ips.idips = urgencia.ips_idips GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips ))as tmp group by departamento,municipio,nombre,idips order by departamento,municipio,suma;"
	query2 = "SELECT departamento, sum(conteo) as suma from ((SELECT ips.departamento, ips.idips, hospitalizacion.ips_idips,count(ips.idips) as conteo FROM ips INNER JOIN hospitalizacion ON ips.idips = hospitalizacion.ips_idips GROUP BY ips.departamento, ips.idips, hospitalizacion.ips_idips)union(SELECT ips.departamento, ips.idips, citas_medicas.ips_idips,count(ips.idips) as conteo FROM ips INNER JOIN citas_medicas ON ips.idips = citas_medicas.ips_idips GROUP BY ips.departamento, ips.idips, citas_medicas.ips_idips)union(SELECT ips.departamento, ips.idips, urgencia.ips_idips,count(ips.idips) as conteo FROM ips INNER JOIN urgencia ON ips.idips = urgencia.ips_idips GROUP BY ips.departamento, ips.idips, urgencia.ips_idips))as tmp group by departamento order by departamento,suma;"

	cursor1.execute(query1)
	cursor2.execute(query2)
	hospitals = dictfetchall(cursor1)
	regions = dictfetchall(cursor2)
	
	return hospitals, regions

def patientCarePeriodYear():
	cursor1 = connection.cursor()
	cursor2 = connection.cursor()
	query1 = "SELECT concat(ips.nombre,' - ',ips.municipio) as nombre_ips,period_year,count(ips.idips)FROM ips INNER JOIN hospitalizacion ON ips.idips = hospitalizacion.ips_idips INNER JOIN fecha ON hospitalizacion.fecha1 = fecha.idfecha where fecha.period_year='NAVIDAD' or fecha.period_year='VACACIONES' or fecha.period_year='SEMANA SANTA' GROUP BY nombre_ips, period_year order by nombre_ips;"
	query2 = "SELECT medico.nombre, period_year, count(medico.idmedico) FROM medico INNER JOIN hospitalizacion ON medico.idmedico = hospitalizacion.medico_idmedico INNER JOIN fecha ON hospitalizacion.fecha1 = fecha.idfecha where fecha.period_year='NAVIDAD' or fecha.period_year='VACACIONES' or fecha.period_year='SEMANA SANTA' GROUP BY medico.nombre, period_year order by medico.nombre;"

	cursor1.execute(query1)
	cursor2.execute(query2)
	by_clinic = dictfetchall(cursor1)
	by_medico = dictfetchall(cursor2)
	
	return by_clinic, by_medico

#atencion de pacientes por periodo del anio
def attentionByPeriodOfYear():
	cursor1 = connection.cursor()
	query = "select period_year, sum(cantidad_pacientes) as cantidad_pacientes from(select period_year, count(period_year) as cantidad_pacientes from citas_medicas join fecha on citas_medicas.fecha2 = fecha.idfecha where period_year !='' group by period_year union select period_year, count(period_year) as cantidad_pacientes from urgencia join fecha on urgencia.fecha2 = fecha.idfecha where period_year !=''    group by period_year union select period_year, count(period_year) as cantidad_pacientes from hospitalizacion join fecha on hospitalizacion.fecha1 = fecha.idfecha where period_year !='' group by period_year) as tmp group by period_year"
	cursor1.execute(query)
	return dictfetchall(cursor1)

#atencion de pacientes por dia de la semana
def attentionByDayOfWeek(fecha1=None,fecha2=None):
	cursor1 = connection.cursor()
	if fecha1!=None and fecha2!=None:
		query = "select dayname, sum(cantidad_pacientes) as cantidad_pacientes from(select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from citas_medicas join fecha on citas_medicas.fecha2 = fecha.idfecha where fecha.date_actual>='"+fecha1+"' and fecha.date_actual<='"+fecha2+"' group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from urgencia join fecha on urgencia.fecha2 = fecha.idfecha where fecha.date_actual>='"+fecha1+"' and fecha.date_actual<='"+fecha2+"' group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from hospitalizacion join fecha on hospitalizacion.fecha2 = fecha.idfecha where fecha.date_actual>='"+fecha1+"' and fecha.date_actual<='"+fecha2+"' group by fecha.day_name) as tmp group by dayname"
	else:
		query = "select dayname, sum(cantidad_pacientes) as cantidad_pacientes from(select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from citas_medicas join fecha on citas_medicas.fecha2 = fecha.idfecha group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from urgencia join fecha on urgencia.fecha2 = fecha.idfecha group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from hospitalizacion join fecha on hospitalizacion.fecha2 = fecha.idfecha group by fecha.day_name) as tmp group by dayname"
	cursor1.execute(query)
	return dictfetchall(cursor1)

#medicinas mas recetadas
def medicinePrescription(fecha1=None,fecha2=None):
	cursor1 = connection.cursor()
	print fecha1
	if fecha1!=None and fecha2!=None:
		print "xx"
		query = "select nombre_generico,count(nombre_generico)as cantidad from medicamentos_resetados join medicamento on medicamento.idmedicamento=medicamentos_resetados.medicamento_idmedicamento join fecha on fecha_idfecha=idfecha where date_actual >='"+fecha1+"' and date_actual <='"+fecha2+"' group by nombre_generico order by cantidad DESC limit 10"
	else:
		print "2xx"
		query = "select nombre_generico,count(nombre_generico)as cantidad from medicamentos_resetados join medicamento on medicamento.idmedicamento=medicamentos_resetados.medicamento_idmedicamento join fecha on fecha_idfecha=idfecha group by nombre_generico order by cantidad DESC limit 10"
	cursor1.execute(query)
	return dictfetchall(cursor1)
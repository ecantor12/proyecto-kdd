from django.db import connection, transaction

#Function to convert tuple's lists of dict's objects
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def avgTimeMedical(initial_date, final_date):

	cursor = connection.cursor()
	if initial_date!=None and final_date!=None:
		query = "select avg(tiempo_espera/3600) as promedio_citas_medicas from citas_medicas INNER JOIN fecha ON citas_medicas.fecha2 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"'"
	else:
		query = "SELECT avg(tiempo_espera/3600) AS promedio_citas_medicas FROM citas_medicas"

	cursor.execute(query)
	rows = dictfetchall(cursor)
	
	return rows

def avgTimeSurgeries(initial_date, final_date):
	
	cursor = connection.cursor()
	if initial_date!=None and final_date!=None:
		query = "select avg(tiempo_espera/3600) as tiempo_espera_urgencia from urgencia INNER JOIN fecha ON urgencia.fecha2 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+ "' and fecha.date_actual <= '"+str(final_date)+"'"
	else:
		query = "SELECT avg(tiempo_espera)/3600 as tiempo_espera_urgencia from urgencia"

	cursor.execute(query)
	rows = dictfetchall(cursor)
	
	return rows

def patientCare(initial_date, final_date):
	cursor1 = connection.cursor()
	cursor2 = connection.cursor()

	if initial_date!=None and final_date!=None:
		query1 = "select departamento,municipio,nombre,idips, sum(conteo) as suma from ((SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, hospitalizacion.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN hospitalizacion ON ips.idips = hospitalizacion.ips_idips INNER JOIN fecha ON hospitalizacion.fecha1 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, hospitalizacion.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN citas_medicas ON ips.idips = citas_medicas.ips_idips INNER JOIN fecha ON citas_medicas.fecha2 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN urgencia ON ips.idips = urgencia.ips_idips INNER JOIN fecha ON urgencia.fecha2 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips))as tmp group by departamento,municipio,nombre,idips order by departamento,municipio,suma;"
		query2 = "select departamento, sum(conteo) as suma from ((SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, hospitalizacion.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN hospitalizacion ON ips.idips = hospitalizacion.ips_idips INNER JOIN fecha ON hospitalizacion.fecha1 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, hospitalizacion.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN citas_medicas ON ips.idips = citas_medicas.ips_idips INNER JOIN fecha ON citas_medicas.fecha2 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN urgencia ON ips.idips = urgencia.ips_idips INNER JOIN fecha ON urgencia.fecha2 = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips))as tmp group by departamento order by departamento,suma;"
	else:
		query1 = "SELECT departamento,municipio,nombre,idips, sum(conteo) as suma from ((SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, hospitalizacion.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN hospitalizacion ON ips.idips = hospitalizacion.ips_idips GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, hospitalizacion.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN citas_medicas ON ips.idips = citas_medicas.ips_idips GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, citas_medicas.ips_idips)union(SELECT ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips, count(ips.idips) as conteo FROM ips INNER JOIN urgencia ON ips.idips = urgencia.ips_idips GROUP BY ips.departamento, ips.municipio, ips.nombre, ips.idips, urgencia.ips_idips ))as tmp group by departamento,municipio,nombre,idips order by departamento,municipio,suma;"
		query2 = "SELECT departamento, sum(conteo) as suma from ((SELECT ips.departamento, ips.idips, hospitalizacion.ips_idips,count(ips.idips) as conteo FROM ips INNER JOIN hospitalizacion ON ips.idips = hospitalizacion.ips_idips GROUP BY ips.departamento, ips.idips, hospitalizacion.ips_idips)union(SELECT ips.departamento, ips.idips, citas_medicas.ips_idips,count(ips.idips) as conteo FROM ips INNER JOIN citas_medicas ON ips.idips = citas_medicas.ips_idips GROUP BY ips.departamento, ips.idips, citas_medicas.ips_idips)union(SELECT ips.departamento, ips.idips, urgencia.ips_idips,count(ips.idips) as conteo FROM ips INNER JOIN urgencia ON ips.idips = urgencia.ips_idips GROUP BY ips.departamento, ips.idips, urgencia.ips_idips))as tmp group by departamento order by departamento,suma;"

	cursor1.execute(query1)
	cursor2.execute(query2)
	hospitals = dictfetchall(cursor1)
	regions = dictfetchall(cursor2)
	
	return hospitals, regions

def patientCarePeriodYear(initial_date, final_date):
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
def attentionByPeriodOfYear(initial_date, final_date):
	cursor1 = connection.cursor()
	query = "select period_year, sum(cantidad_pacientes) as cantidad_pacientes from(select period_year, count(period_year) as cantidad_pacientes from citas_medicas join fecha on citas_medicas.fecha2 = fecha.idfecha where period_year !='' group by period_year union select period_year, count(period_year) as cantidad_pacientes from urgencia join fecha on urgencia.fecha2 = fecha.idfecha where period_year !=''    group by period_year union select period_year, count(period_year) as cantidad_pacientes from hospitalizacion join fecha on hospitalizacion.fecha1 = fecha.idfecha where period_year !='' group by period_year) as tmp group by period_year"
	cursor1.execute(query)
	return dictfetchall(cursor1)

#atencion de pacientes por dia de la semana
def attentionByDayOfWeek(initial_date, final_date):

	cursor1 = connection.cursor()
	if initial_date!=None and final_date!=None:
		query = "select dayname, sum(cantidad_pacientes) as cantidad_pacientes from(select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from citas_medicas join fecha on citas_medicas.fecha2 = fecha.idfecha where fecha.date_actual>='"+str(initial_date)+"' and fecha.date_actual<='"+str(final_date)+"' group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from urgencia join fecha on urgencia.fecha2 = fecha.idfecha where fecha.date_actual>='"+str(initial_date)+"' and fecha.date_actual<='"+str(final_date)+"' group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from hospitalizacion join fecha on hospitalizacion.fecha2 = fecha.idfecha where fecha.date_actual>='"+str(initial_date)+"' and fecha.date_actual<='"+str(final_date)+"' group by fecha.day_name) as tmp group by dayname"
	else:
		query = "select dayname, sum(cantidad_pacientes) as cantidad_pacientes from(select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from citas_medicas join fecha on citas_medicas.fecha2 = fecha.idfecha group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from urgencia join fecha on urgencia.fecha2 = fecha.idfecha group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from hospitalizacion join fecha on hospitalizacion.fecha2 = fecha.idfecha group by fecha.day_name) as tmp group by dayname"

	#query = "select dayname, sum(cantidad_pacientes) as cantidad_pacientes from(select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from citas_medicas join fecha on citas_medicas.fecha2 = fecha.idfecha group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from urgencia join fecha on urgencia.fecha2 = fecha.idfecha group by fecha.day_name union select fecha.day_name as dayname, count(fecha.day_name) as cantidad_pacientes from hospitalizacion join fecha on hospitalizacion.fecha2 = fecha.idfecha group by fecha.day_name) as tmp group by dayname"
	cursor1.execute(query)
	return dictfetchall(cursor1)

#medicinas mas recetadas
def medicinePrescription(initial_date, final_date):
	cursor1 = connection.cursor()

	if initial_date!=None and final_date!=None:
		query = "select nombre_generico,count(nombre_generico)as cantidad from medicamentos_resetados join medicamento on medicamento.idmedicamento=medicamentos_resetados.medicamento_idmedicamento join fecha on fecha_idfecha=idfecha where date_actual >='"+str(initial_date)+"' and date_actual <='"+str(final_date)+"' group by nombre_generico order by cantidad DESC limit 10"
	else:
		query = "select nombre_generico,count(nombre_generico)as cantidad from medicamentos_resetados join medicamento on medicamento.idmedicamento=medicamentos_resetados.medicamento_idmedicamento join fecha on fecha_idfecha=idfecha group by nombre_generico order by cantidad DESC limit 10"

	#query = "select nombre_generico,count(nombre_generico)as cantidad from medicamentos_resetados join medicamento on medicamento.idmedicamento=medicamentos_resetados.medicamento_idmedicamento join fecha on fecha_idfecha=idfecha where date_actual >='1995-01-01' and date_actual <='2017-01-01' group by nombre_generico order by cantidad DESC limit 10"
	cursor1.execute(query)
	return dictfetchall(cursor1)



def payments(initial_date, final_date):

	cursor1 = connection.cursor()
	cursor2 = connection.cursor()

	if initial_date!=None and final_date!=None:
		query1 = "select nombre, sum(valor_pago) as pagos from pagos join cotizante on cotizante_idcotizante=idcotizante INNER JOIN fecha ON pagos.fecha_idfecha = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' group by nombre order by pagos"
		query2 = "select empresa, sum(valor_pago) as pagos from pagos join cotizante on cotizante_idcotizante=idcotizante INNER JOIN fecha ON pagos.fecha_idfecha = fecha.idfecha where fecha.date_actual >= '"+str(initial_date)+"' and fecha.date_actual <= '"+str(final_date)+"' group by empresa"
	else:
		query1 = "select nombre, sum(valor_pago) as pagos from pagos join cotizante on cotizante_idcotizante=idcotizante INNER JOIN fecha ON pagos.fecha_idfecha = fecha.idfecha group by nombre order by pagos"
		query2 = "select empresa, sum(valor_pago) as pagos from pagos join cotizante on cotizante_idcotizante=idcotizante INNER JOIN fecha ON pagos.fecha_idfecha = fecha.idfecha group by empresa"

	cursor1.execute(query1)
	cursor2.execute(query2)
	contributor = dictfetchall(cursor1)
	company = dictfetchall(cursor2)
	
	return contributor, company

#algoritmo apriori para medicamentos que se venden juntos
def productsTogether(initial_date, final_date):
	cursor1 = connection.cursor()
	query = "select id_formula,medicamento_idmedicamento,concat (nombre_generico,' ',presentacion) as nombre_medicamento from medicamentos_resetados inner join medicamento on medicamentos_resetados.medicamento_idmedicamento = medicamento.idmedicamento order by id_formula"
	cursor1.execute(query)
	results = dictfetchall(cursor1)

	datos = []
	elementos_por_formula =[]
	idformula = results[0]['id_formula']
	
	for obj in results:
		
		if idformula == obj['id_formula']:
			elementos_por_formula.append(obj['nombre_medicamento'])
		else:
			#guardamos el grupo de medicamentos
			datos.append(elementos_por_formula)
			idformula = obj['id_formula']
			elementos_por_formula = []
			elementos_por_formula.append(obj['nombre_medicamento'])

	from apyori import apriori
	results = list(apriori(datos))

	medicamentos = []
	for obj in results:
		for x in obj.items:
			#print x
			medicamentos.append(x)
	
	return medicamentos
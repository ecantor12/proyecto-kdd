#Function to convert tuple's lists of dict's objects
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def avgTime():
	from django.db import connection, transaction
	cursor = connection.cursor()
	query = "SELECT avg(tiempo_espera) AS promedio_citas_medicas FROM citas_medicas"

	cursor.execute(query)
	rows = dictfetchall(cursor)
	
	return rows


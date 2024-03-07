import sqlite3
# Conexión a la base de datos SQLite3, permitiendo múltiples hilos con `check_same_thread=False`
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

# Función para crear la tabla de tareas si no existe
# Creación de la tabla `taskstable` con campos para la tarea, estado y fecha de vencimiento
def create_table():
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,task_status TEXT,task_due_date DATE)')



# Función para añadir datos a la tabla
def add_data(task,task_status,task_due_date):
	# Inserta una nueva tarea en la tabla
	c.execute('INSERT INTO taskstable(task,task_status,task_due_date) VALUES (?,?,?)',(task,task_status,task_due_date))
	conn.commit()
# Función para ver todos los datos de la tabla	
def view_all_data():
	# Selecciona y retorna todos los registros de la tabla
	c.execute('SELECT * FROM taskstable')
	data = c.fetchall()
	return data
	
# Función para ver tareas únicas sin duplicados
def view_unique_tasks():
	# Selecciona y retorna tareas únicas por su nombre
	c.execute('SELECT DISTINCT task FROM taskstable')
	data = c.fetchall()
	return data 
	
# Función para obtener detalles de una tarea específica
def get_task(task):
	# Selecciona y retorna datos de una tarea específica
	c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data
	
# Función para editar los datos de una tarea existente
def edit_task_data(new_task,new_task_status,new_task_date,task,task_status,task_due_date):
	# Actualiza la información de la tarea basándose en criterios específicos
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_date,task,task_status,task_due_date))
	conn.commit()
	data = c.fetchall()
	return data
	
# Función para eliminar una tarea
def delete_data(task):
	# Elimina una tarea específica de la tabla
	c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
	conn.commit()

 
	   
    

    

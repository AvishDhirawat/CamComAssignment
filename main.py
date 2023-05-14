from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",  # Enter your MySQL username here
    password="Kavish@0901",  # Enter your MySQL password here
    database="qc_database"
)


def execute_query(query):
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    db.commit()
    return cursor


def execute_insert_query(query, values):
    cursor2 = db.cursor(buffered=True)
    cursor2.execute(query, values)
    db.commit()
    return cursor2


@app.route('/qc_persons', methods=['GET'])
def get_qc_persons():
    query = "SELECT * FROM qc_persons"
    results = execute_query(query)
    persons = []
    for result in results:
        person = {
            "id": result[0],
            "name": result[1],
            "is_busy": result[2],
            "current_task": result[3]
        }
        persons.append(person)
    return jsonify(persons)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    query = "SELECT * FROM tasks"
    results = execute_query(query)
    tasks = []
    for result in results:
        task = {
            "id": result[0],
            "taks_name": result[1],
            "status": result[2],
            "assigned_to": result[3]
        }
        tasks.append(task)
    return jsonify(tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_id = request.json['task_id']
    task_name = request.json['task_name']
    query = "INSERT INTO tasks(id, task_name) VALUES (%s, %s)"
    try:
        execute_insert_query(query, (task_id, task_name)).close()
        return "New task added to database"
    except mysql.connector.Error as error:
        result = {'status': 'error', 'message': 'Insert failed: {}'.format(error)}
        return jsonify(result)


@app.route('/add_qc_person', methods=['POST'])
def add_qc_person():
    person_id = request.json['id']
    person_name = request.json['name']
    query = "INSERT INTO qc_persons(id, name) VALUES (%s, %s)"
    try:
        execute_insert_query(query, (person_id, person_name)).close()
        return "New QCPerson added to database"
    except mysql.connector.Error as error:
        result = {'status': 'error', 'message': 'Insert failed: {}'.format(error)}
        return jsonify(result)


@app.route('/assign_task', methods=['POST'])
def assign_task():
    task_id = request.json['task_id']
    query = f"SELECT * FROM tasks WHERE id = {task_id} AND status = 'pending'"
    task_results = execute_query(query).fetchall()
    execute_query(query).close()
    if len(task_results) == 0:
        return "Task already assigned", 400
    query = "SELECT * FROM qc_persons WHERE is_busy = FALSE AND logged_in = TRUE ORDER BY rand()"
    results = execute_query(query).fetchall()
    execute_query(query).close()
    if len(results) == 0:
        return "No QC persons are free/logged-in to assign the task", 400
    qc_person = results[0]
    query = "SELECT * FROM tasks WHERE status = 'pending' ORDER BY rand()"
    tasks_result = execute_query(query).fetchall()
    execute_query(query).close()
    if len(tasks_result) == 0:
        return "No pending tasks found", 400
    query = f"UPDATE qc_persons SET is_busy = TRUE, current_task = {task_id} WHERE id = {qc_person[0]}"
    rows_affected = execute_query(query).rowcount
    execute_query(query).close()
    if rows_affected == 0:
        return "There's some error in qc_persons table", 400
    query = f"UPDATE tasks SET status = 'in progress', assigned_to = {qc_person[0]} WHERE id = {task_id}"
    rows_affected_tasks = execute_query(query).rowcount
    execute_query(query).close()
    if rows_affected_tasks == 0:
        return "There's some error in tasks table", 400
    return "Task assigned successfully"


@app.route('/task_completed', methods=['POST'])
def task_completed():
    qc_person_id = request.json['qc_person_id']
    task_id = request.json['task_id']
    query = f"UPDATE qc_persons SET is_busy = FALSE, current_task = NULL WHERE id = {qc_person_id} AND current_task = {task_id}"
    rows_affected = execute_query(query).rowcount
    execute_query(query).close()
    if rows_affected == 0:
        return "Task not found or not assigned to the given QC person", 400
    query = f"UPDATE tasks SET status = 'completed' WHERE id = {task_id} AND status = 'in progress'"
    rows_affected = execute_query(query).rowcount
    execute_query(query).close()
    if rows_affected == 0:
        return "Task not assigned or it is already completed", 400
    return "Task marked as completed successfully"


@app.route('/login', methods=['POST'])
def login():
    qc_person_id = request.json['qc_person_id']
    query = f"UPDATE qc_persons SET logged_in = TRUE WHERE id = {qc_person_id} AND logged_in = FALSE"
    try:
        response = execute_query(query).rowcount
        if response == 0:
            return "QCPerson already Logged-In!", 400
        execute_query(query).close()
        return f"QCPerson with id {qc_person_id}, is now logged in successfully!"
    except mysql.connector.Error as error:
        result = {'status': 'error', 'message': 'Insert failed: {}'.format(error)}
        return jsonify(result)


@app.route('/logout', methods=['POST'])
def logout():
    qc_person_id = request.json['qc_person_id']
    query = f"SELECT * FROM qc_persons WHERE id = {qc_person_id} AND is_busy = TRUE"
    results = execute_query(query).fetchall()
    execute_query(query).close()
    query = f"UPDATE qc_persons SET logged_in = FALSE, current_task = NULL WHERE id = {qc_person_id} AND logged_in = TRUE"
    try:
        response = execute_query(query).rowcount
        if response == 0:
            return "QCPerson already Logged-Out!", 400
        execute_query(query).close()
        if len(results) > 0:
            query = f"UPDATE tasks SET status = 'pending', assigned_to = NULL WHERE id = {results[0][3]}"
            execute_query(query).close()
        return f"QCPerson with id {qc_person_id}, is now logged out successfully!"
    except mysql.connector.Error as error:
        result = {'status': 'error', 'message': 'Insert failed: {}'.format(error)}
        return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

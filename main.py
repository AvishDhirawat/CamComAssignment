from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kavish@0901",
    database="qc_database"
)


def execute_query(query):
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    db.commit()
    return cursor


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


@app.route('/assign_task', methods=['POST'])
def assign_task():
    task_id = request.json['task_id']
    query = "SELECT * FROM qc_persons WHERE is_busy = FALSE ORDER BY rand()"
    results = execute_query(query).fetchall()
    execute_query(query).close()
    if len(results) == 0:
        return "No QC persons are free to assign the task", 400
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


if __name__ == '__main__':
    app.run(debug=True)

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


@app.route('/assign_task', methods=['POST'])
def assign_task():
    # Get the data from the request
    task_id = request.json['task_id']
    # Check which QC persons are free
    query = "SELECT * FROM qc_persons WHERE is_busy = FALSE"
    results = execute_query(query).fetchall()
    execute_query(query).close()
    if len(results) == 0:
        return "No QC persons are free to assign the task", 400
    # Assign the task to the first free QC person
    qc_person = results[0]
    query = f"UPDATE qc_persons SET is_busy = TRUE, current_task = {task_id} WHERE id = {qc_person[0]}"
    execute_query(query).close()
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
    query = f"SELECT id FROM tasks WHERE status = 'pending' LIMIT 1"
    results = execute_query(query).fetchall()
    execute_query(query).close()
    if len(results) > 0:
        task_id = results[0][0]
        query = f"UPDATE qc_persons SET is_busy = TRUE, current_task = {task_id} WHERE id = {qc_person_id}"
        execute_query(query).close()
    return "Task marked as completed successfully"


if __name__ == '__main__':
    app.run(debug=True)

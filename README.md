# CamComAssignment
CamCom Assignment for QC Person
In a manual QC (Quality Check) process, there is a portal from which each individual QC task is assigned. 
The portal needs to check how many QC persons are logged in and which of the logged in persons are free, as in not on a task, and automatically assign tasks. 
Once the task is finished the person will automatically get assigned the next task if any is pending. 
How would you architect this? I want to understand step by step the methodology you used to come to the final solution. 
Illustrate a basic API framework written in Python using Flask and MySql as the database.

 Solution : 
1. At first,  We need to identify the entities in the system. Based on the requirements, we have two entities: QC tasks and QC persons.
2. Create the database schema: The database schema can be created based on the entities. Tasks and qc_persons are two tables that can be built. Id, task_name, status, and assigned_to columns will be included in the tasks table. Columns in the qc_persons table include id, name, is_busy, and current_task.
3. Develop the API using Flask: By using Flask, we can create a REST API that exposes the endpoints needed to assign and perform QC tasks. 
The following activities will require endpoints to be created:
    Obtain a list of all QC employees.
    Give a QC employee a job to do.
    Mark a task as finished, and if any, assign the following one.
4. Make use of MySQL Connector to establish a connection to the database: SQL queries can be run on the MySQL database by using MySQL Connector.
5. Develop the logic to assign tasks: We need to develop the logic to check how many QC persons are logged in and which of the logged in persons are free. We can query the qc_persons table to get the list of all QC persons who are not busy, and then assign the task to a random available person in the list.
6. Develop the logic to mark tasks as completed: We need to develop the logic to mark a task as completed and assign the next task if any is pending. We can query the tasks table to get the list of all pending tasks, and then automatically assign the next task to the person who just completed the previous task.
7. Test the system: We can test the system by running the Flask API and making HTTP requests to the endpoints to assign and complete tasks and test different scenarios.
Overall, we can use Flask to create an API that connects to a MySQL database, and use SQL queries and Python code to manage the QC tasks and QC persons.

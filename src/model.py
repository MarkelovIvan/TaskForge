import psycopg

class tasks:
    def __init__(self):
        try:
            self.connection = psycopg.connect(
                dbname="Markelov_lab6",
                user="postgres",
                password="2323",
                host="127.0.0.1",  # Use localhost IP address
                port="5432"
            )
            print("Connection to database established successfully!")
            self.cursor = self.connection.cursor()
        except psycopg.Error as error:
            print("Failed to connect to the database:", str(error))
            raise

    def get_all_tasks(self):
        try:
            self.cursor.execute("SELECT * FROM task")
            result = self.cursor.fetchall()
            if self.cursor.rowcount == 0:
                return {"message": "There are no tasks", "error": "Not Found", "status_code": 404}
            return {"data": result, "status_code": 200}
        except psycopg.Error as error:
            return {"message": str(error), "error": "Database Error", "status_code": 500}

    def get_task(self, id):
        if not str(id).isdigit():
            return {"message": "Invalid task id", "error": "Bad Request", "status_code": 400}
        try:
            self.cursor.execute("SELECT * FROM task WHERE id = %s", (id,))
            result = self.cursor.fetchall()
            if self.cursor.rowcount == 0:
                return {"message": f"There is no task with id {id}", "error": "Not Found", "status_code": 404}
            return {"data": result, "status_code": 200}
        except psycopg.Error as error:
            return {"message": str(error), "error": "Database Error", "status_code": 500}

    def add_task(self, data):
        data = dict(data)
        required_keys = {'id', 'project_id', 'description', 'status', 'name', 'price'}
        if not required_keys.issubset(data):
            return {"message": "Invalid or missing keys", "error": "Bad Request", "status_code": 400}
        try:
            print("hellotry")
            query = "INSERT INTO task (id, project_id, description, status, name, price) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (data['id'], data['project_id'], data['description'], data['status'], data['name'], data['price'])
            self.cursor.execute(query, values)
            self.connection.commit()
            if self.cursor.rowcount > 0:
                return {"message": "task added successfully", "status_code": 200}
            else:
                return {"message": "task wasn`t added to database", "error": "Not Acceptable", "status_code": 406}
        except psycopg.Error as error:
            self.connection.rollback()
            return {"message": "Add task failed: " + str(error), "error": "Database Error", "status_code": 500}

    def update_task(self, data):
        data = dict(data)
        if 'id' not in data:
            return {"message": "No task id provided", "error": "Bad Request", "status_code": 400}
        task_id = data['id']
        del data['id']
        if not data:
            return {"message": "No data provided", "error": "Bad Request", "status_code": 400}
        set_clause = ', '.join([f"{key} = %s" for key in data])
        values = list(data.values())
        values.append(task_id)
        try:
            query = f"UPDATE task SET {set_clause} WHERE id = %s"
            self.cursor.execute(query, values)
            self.connection.commit()

            if self.cursor.rowcount > 0:
                return {"message": "task updated successfully", "status_code": 200}
            else:
                return {"message": "task wasn`t updated", "error": "Not Found", "status_code": 404}
        except psycopg.Error as error:
            self.connection.rollback()
            return {"message": "task update failed: " + str(error), "error": "Database Error", "status_code": 500}

    def delete_task(self, id):
        if not str(id).isdigit():
            return {"message": "Invalid task id", "error": "Bad Request", "status_code": 400}
        try:
            self.cursor.execute("DELETE FROM task WHERE id = %s", (id,))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                return {"message": "task deleted successfully", "status_code": 200}
            else:
                return {"message": "Nothing to delete", "error": "Not Found", "status_code": 404}
        except Exception as error:
            self.connection.rollback()
            return {"message": "Delete task failed", "error": str(error), "status_code": 500}

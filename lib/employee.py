# Importing the cursor and connection from the __init__ file
from __init__ import CURSOR, CONN
# Importing the Department class from the department module
from department import Department

# The Employee class represents an employee in the organization
class Employee:

    # A dictionary to store all employee objects with their id as the key
    all = {}

    # The constructor for the Employee class
    def __init__(self, name, job_title, department_id, id=None):
        # The id, name, job title, and department id attributes for an employee
        self.id = id
        self.name = name
        self.job_title = job_title
        self.department_id = department_id

    # The string representation of the employee object
    def __repr__(self):
        return (
            f"<Employee {self.id}: {self.name}, {self.job_title}, " +
            f"Department ID: {self.department_id}>"
        )
    
    # Getter for the name attribute
    @property
    def name(self):
        return self._name

    # Setter for the name attribute
    @name.setter
    def name(self, name):
        # Check if the name is a non-empty string
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    # Getter for the job title attribute
    @property
    def job_title(self):
        return self._job_title

    # Setter for the job title attribute
    @job_title.setter
    def job_title(self, job_title):
        # Check if the job title is a non-empty string
        if isinstance(job_title, str) and len(job_title):
            self._job_title = job_title
        else:
            raise ValueError(
                "job_title must be a non-empty string"
            )

    # Getter for the department id attribute
    @property
    def department_id(self):
        return self._department_id

    # Setter for the department id attribute
    @department_id.setter
    def department_id(self, department_id):
        # Check if the department id is an integer and references a department in the database
        if type(department_id) is int and Department.find_by_id(department_id):
            self._department_id = department_id
        else:
            raise ValueError(
                "department_id must reference a department in the database")

    # Class method to create a new table for the Employee class
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            job_title TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Class method to drop the table for the Employee class
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS employees;
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Method to save an employee object to the database
    def save(self):
        sql = """
                INSERT INTO employees (name, job_title, department_id)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.job_title, self.department_id))
        CONN.commit()

        # Update the id of the employee object with the id of the new row
        self.id = CURSOR.lastrowid
        # Add the employee object to the dictionary
        type(self).all[self.id] = self

    # Method to update an employee object in the database
    def update(self):
        sql = """
            UPDATE employees
            SET name = ?, job_title = ?, department_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.job_title,
                             self.department_id, self.id))
        CONN.commit()

    # Method to delete an employee object from the database
    def delete(self):
        sql = """
            DELETE FROM employees
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the employee object from the dictionary
        del type(self).all[self.id]

        # Set the id of the employee object to None
        self.id = None

    # Class method to create a new employee object and save it to the database
    @classmethod
    def create(cls, name, job_title, department_id):
        employee = cls(name, job_title, department_id)
        employee.save()
        return employee

    # Class method to create an employee object from a row in the database
    @classmethod
    def instance_from_db(cls, row):
        # Check if an employee object with the same id already exists
        employee = cls.all.get(row[0])
        if employee:
            # Update the attributes of the employee object
            employee.name = row[1]
            employee.job_title = row[2]
            employee.department_id = row[3]
        else:
            # Create a new employee object and add it to the dictionary
            employee = cls(row[1], row[2], row[3])
            employee.id = row[0]
            cls.all[employee.id] = employee
        return employee

    # Class method to get all employee objects from the database
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM employees
        """

        rows = CURSOR.execute(sql).fetchall()

        # Create an employee object for each row in the database
        return [cls.instance_from_db(row) for row in rows]

    # Class method to find an employee object by id
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM employees
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        # Return the employee object if it exists, otherwise return None
        return cls.instance_from_db(row) if row else None

    # Class method to find an employee object by name
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM employees
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        # Return the employee object if it exists, otherwise return None
        return cls.instance_from_db(row) if row else None

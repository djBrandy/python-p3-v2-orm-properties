# Importing the cursor and connection from the __init__ file
from __init__ import CURSOR, CONN

# The Department class represents a department in the organization
class Department:

    # A dictionary to store all department objects with their id as the key
    all = {}

    # The constructor for the Department class
    def __init__(self, name, location, id=None):
        # The id, name, and location attributes for a department
        self.id = id
        self.name = name
        self.location = location

    # The string representation of the department object
    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"
    
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

    # Getter for the location attribute
    @property
    def location(self):
        return self._location

    # Setter for the location attribute
    @location.setter
    def location(self, location):
        # Check if the location is a non-empty string
        if isinstance(location, str) and len(location):
            self._location = location
        else:
            raise ValueError(
                "Location must be a non-empty string"
            )

    # Class method to create a new table for the Department class
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Class method to drop the table for the Department class
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Method to save a department object to the database
    def save(self):
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        # Update the id of the department object with the id of the new row
        self.id = CURSOR.lastrowid
        # Add the department object to the dictionary
        type(self).all[self.id] = self

    # Class method to create a new department object and save it to the database
    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    # Method to update a department object in the database
    def update(self):
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    # Method to delete a department object from the database
    def delete(self):
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the department object from the dictionary
        del type(self).all[self.id]

        # Set the id of the department object to None
        self.id = None

    # Class method to create a department object from a row in the database
    @classmethod
    def instance_from_db(cls, row):
        # Check if a department object with the same id already exists
        department = cls.all.get(row[0])
        if department:
            # Update the attributes of the department object
            department.name = row[1]
            department.location = row[2]
        else:
            # Create a new department object and add it to the dictionary
            department = cls(row[1], row[2])
            department.id = row[0]
            cls.all[department.id] = department
        return department

    # Class method to get all department objects from the database
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM departments
        """

        rows = CURSOR.execute(sql).fetchall()

        # Create a department object for each row in the database
        return [cls.instance_from_db(row) for row in rows]

    # Class method to find a department object by id
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM departments
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        # Return the department object if it exists, otherwise return None
        return cls.instance_from_db(row) if row else None

    # Class method to find a department object by name
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM departments
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        # Return the department object if it exists, otherwise return None
        return cls.instance_from_db(row) if row else None

    # Method to get all employees of a department
    def employees(self):
        from employee import Employee
        sql = """
            SELECT * FROM employees
            WHERE department_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        # Create an employee object for each row in the database
        return [
            Employee.instance_from_db(row) for row in rows
        ]

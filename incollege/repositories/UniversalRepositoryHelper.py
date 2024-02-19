import copy

from incollege.repositories.DBConnector import get_connection


class UniversalRepositoryHelper:

    def __init__(self, table_name, cls):
        self.TABLE_NAME = table_name
        self.CLASS = cls

    def is_alive(self):
        query = f"SELECT 1"
        return get_connection().cursor().execute(query).fetchone()[0] == 1

    def get_record_count(self):
        query = f"SELECT COUNT(1) FROM {self.TABLE_NAME}"
        return get_connection().cursor().execute(query).fetchone()[0]

    def get_objects(self, keys):
        condition_string = self.create_condition_string(keys)
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {condition_string}"

        cursor = get_connection().cursor()
        cursor.execute(query, self.create_tuple(keys))

        results = cursor.fetchall()

        if results:
            column_names = [description[0] for description in cursor.description]
            result_list = [dict(zip(column_names, row)) for row in results]

            return [self.convert_to_instance(data) for data in result_list]
        else:
            return []

    def does_record_exist(self, keys):
        condition_string = self.create_condition_string(keys)
        query = f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE {condition_string}"
        cursor = get_connection().cursor()
        result = cursor.execute(query, self.create_tuple(keys))
        return result[0] >= 1

    def create_object(self, obj):
        dictionary = self.create_dict(obj)
        placeholders_string, keys_string = self.generate_input_parameters(dictionary)
        query = f"INSERT INTO {self.TABLE_NAME} {keys_string} VALUES {placeholders_string}"
        get_connection().cursor().execute(query, self.create_tuple(dictionary))
        get_connection().commit()

    def delete_entry(self, keys):
        condition_string = self.create_condition_string(keys)
        query = f"DELETE FROM {self.TABLE_NAME} WHERE {condition_string}"
        get_connection().cursor().execute(query, self.create_tuple(keys))
        get_connection().commit()

    def generate_input_parameters(self, dictionary):
        if not dictionary:
            return "()", "()"

        placeholders_string = "(" + ", ".join(["?" for _ in dictionary]) + ")"
        keys_string = "(" + ", ".join(dictionary.keys()) + ")"

        return placeholders_string, keys_string

    def create_tuple(self, input_dict):
        return tuple(input_dict.values())

    def create_condition_string(self, data):
        conditions = []
        for key, value in data.items():
            conditions.append(f"{key} = (?)")

        condition_string = " AND ".join(conditions)
        return condition_string

    def convert_to_instance(self, data):
        return self.CLASS(**data)

    def create_dict(self, obj):
        return copy.copy(vars(obj))
    
    def update_object(self, keys, update_data):
       
        set_clause = ", ".join([f"{column} = ?" for column, value in update_data.items()])
        condition_string = self.create_condition_string(keys)

        query = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE {condition_string}"
        values_tuple = tuple(update_data.values()) + tuple(keys.values())
        
        cursor = get_connection().cursor()
        cursor.execute(query, values_tuple)

        get_connection().commit()

    

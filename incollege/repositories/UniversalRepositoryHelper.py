import copy

from incollege.repositories.DBConnector import get_connection
from incollege.entity.RequestConn import connectionRequest


def generate_input_parameters(dictionary):
    if not dictionary:
        return "()", "()"

    placeholders_string = "(" + ", ".join(["?" for _ in dictionary]) + ")"
    keys_string = "(" + ", ".join(dictionary.keys()) + ")"

    return placeholders_string, keys_string


def create_tuple(input_dict):
    return tuple(input_dict.values())


def create_condition_string(data):
    conditions = []
    for key, value in data.items():
        conditions.append(f"{key} = (?)")

    condition_string = " AND ".join(conditions)
    return condition_string


def create_dict(obj):
    return copy.copy(vars(obj))


def dict_diff(dict1, dict2):
    return {key: dict2[key] for key in dict1 if dict1[key] != dict2[key]}



####### temp v2 for partial return #############################
def create_condition_string2(data):
    conditions = []
    for key, value in data.items():
        conditions.append(f"{key} = (?)")

    condition_string = " OR ".join(conditions)
    return condition_string




class UniversalRepositoryHelper:

    def __init__(self, table_name, cls, primary_keys):
        self.TABLE_NAME = table_name
        self.CLASS = cls
        self.PRIMARY_KEYS = primary_keys

    def is_alive(self):
        query = f"SELECT 1"
        cursor = get_connection().cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result == 1

    def get_record_count(self):
        query = f"SELECT COUNT(1) FROM {self.TABLE_NAME}"
        cursor = get_connection().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

    def get_objects(self, keys, limit=20, offset=0):
        condition_string = create_condition_string(keys)
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {condition_string} LIMIT (?) OFFSET (?)"

        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys) + tuple([limit, offset]))

        results = cursor.fetchall()

        if results:
            column_names = [description[0] for description in cursor.description]
            result_list = [dict(zip(column_names, row)) for row in results]
            return [self.__convert_to_instance(data) for data in result_list]
        else:
            return []

    def does_record_exist(self, keys):
        condition_string = create_condition_string(keys)
        query = f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE {condition_string}"
        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys))
        result = cursor.fetchall()
        return result[0] >= 1

    def create_object(self, obj):
        dictionary = create_dict(obj)
        placeholders_string, keys_string = generate_input_parameters(dictionary)
        query = f"INSERT INTO {self.TABLE_NAME} {keys_string} VALUES {placeholders_string}"
        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(dictionary))
        get_connection().commit()

    def __update_keys(self, keys, update_data):
        set_clause = ", ".join([f"{column} = ?" for column, value in update_data.items()])
        condition_string = create_condition_string(keys)
        query = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE {condition_string}"
        values_tuple = tuple(update_data.values()) + tuple(keys.values())
        cursor = get_connection().cursor()
        cursor.execute(query, values_tuple)
        get_connection().commit()

    def insert_update_object(self, mutated):
        mutated_dictionary = create_dict(mutated)
        mutated_primary_keys = \
            {attr: mutated_dictionary[attr] for attr in self.PRIMARY_KEYS if attr in mutated_dictionary}
        original = self.get_objects(mutated_primary_keys)
        if not original:
            self.create_object(mutated)
        else:
            original_dictionary = create_dict(original[0])
            diff = dict_diff(original_dictionary, mutated_dictionary)
            self.__update_keys(mutated_primary_keys, diff) 

    def delete_entry(self, keys):
        condition_string = create_condition_string(keys)
        query = f"DELETE FROM {self.TABLE_NAME} WHERE {condition_string}"
        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys))
        get_connection().commit()

    def __convert_to_instance(self, data):
        return self.CLASS(**data)
    




    ####### temp v2 for partial return #############################
    
    def get_objects2(self, keys, limit=20, offset=0):
        condition_string = create_condition_string2(keys)
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {condition_string} LIMIT (?) OFFSET (?)"

        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys) + tuple([limit, offset]))

        results = cursor.fetchall()

        if results:
            column_names = [description[0] for description in cursor.description]
            result_list = [dict(zip(column_names, row)) for row in results]
            return [self.__convert_to_instance(data) for data in result_list]
        else:
            return []


    def updateConnection(self, change_data):

        cursor = get_connection().cursor()

        request_ID = change_data.get('request_id')
        status = change_data.get('status')
        query = "UPDATE connections SET status = ? WHERE request_id = ?"
        cursor.execute(query, (status, request_ID))
        get_connection().commit()
        print("Connection updated successfully.")


    def printTable(self):
        cursor = get_connection().cursor()
        cursor.execute("SELECT * FROM connections")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print column names (optional)
        column_names = [description[0] for description in cursor.description]
        print("\n HERE ARE ALL THE PEOPLES")
        print(column_names)

        # Print each row in the result set
        for row in rows:
            print(row)

        

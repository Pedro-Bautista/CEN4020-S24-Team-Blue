import copy
from typing import Tuple, TypeVar, Generic, List

from incollege.repositories.DBConnector import get_connection


def generate_input_parameters(dictionary: dict) -> Tuple[str, str]:
    """Generate a set of input parameters based on an input dictionary.

    Args:
        dictionary: A dictionary of the form [key: value, ...] representing database columns and values \
        to set or compare.

    Returns:
        Tuple[str, str]: A tuple of strings where the first is the "(?, ?, ...)" string for the SQL query \
        and the second is the "(key, key, ...)" string.
    """
    if not dictionary:
        return "()", "()"

    placeholders_string = "(" + ", ".join(["?" for _ in dictionary]) + ")"
    keys_string = "(" + ", ".join(dictionary.keys()) + ")"

    return placeholders_string, keys_string


def create_tuple(input_dict: dict, fuzzy: bool = False) -> Tuple:
    """Creates a tuple based on the values from the input dict.

    Args:
        input_dict (dict): The dict containing the values to be placed into the output Tuple.
        fuzzy (bool, optional): Whether to apply partial matching to the values.
            Defaults to False.

    Returns:
        Tuple: A tuple containing all values from the dict, with partial matching flags if specified.
    """
    if fuzzy:
        return tuple(f'%{value}%' for value in input_dict.values())
    else:
        return tuple(input_dict.values())


def create_condition_string(data: dict, joiner: str = 'AND', fuzzy: bool = False) -> str:
    """Create a SQL WHERE clause based on input matching data.

    Args:
        data (dict): A dict containing the keys and values to match on.
        joiner (str, optional): The joining keyword.
            Defaults to 'AND'.
        fuzzy (bool, optional): Whether to enable partial matching (with LIKE and %).
            Defaults to False.

    Returns:
        str: A condition string matching the input data, fuzzily if specified.
    """
    conditions = []
    for key, value in data.items():
        if fuzzy:
            condition = f'{key} LIKE (?)'
        else:
            condition = f'{key} = (?)'
        conditions.append(condition)

    condition_string = f" {joiner} ".join(conditions)
    return f'({condition_string})'


def create_dict(obj: object) -> dict:
    """Create a dict based on an object instance.

    Args:
        obj (object): Any data object.

    Returns:
        dict: A dictionary with all visible keys and values from obj.
    """
    return copy.copy(vars(obj))


def dict_diff(dict1: dict, dict2: dict) -> dict:
    """Produces a dict representing all keys in dict2 which do not exist in dict1 or do not match the \
    value in dict1.

    Args:
        dict1 (dict): The reference dict to be compared against.
        dict2 (dict): The dict to compare with.

    Returns:
        dict: A dict of only the keys from dict2 which do not match those of dict1.
    """
    return {key: dict2[key] for key in dict1 if dict1[key] != dict2[key]}


def is_alive() -> bool:
    """Checks if the database is operational.

    Returns:
        bool: True if the database was reachable, False if not.
    """
    query = f"SELECT 1"
    cursor = get_connection().cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result == 1


T = TypeVar('T')
"""TypeVar: The class related to the database specified in this helper instance.
"""


class UniversalRepositoryHelper(Generic[T]):
    """Universal repository transaction manager. Call this. Do not query the database directly.

    This class accepts a table name, relational type, and list of primary keys. Using that \
    information, all necessary database functionality is provided through an instance of this \
    class, removing the need for any simple direct database calls. Direct interfacing is still \
    provided by :func:`call_sql_query` but should only be used if no internal methods satisfy \
    the need themselves.

    Attributes:
        CLASS (T): The relational class for the database table being interfaced with.
        TABLE_NAME (str): The name of the database table that this instance will operate on.
        PRIMARY_KEYS (List[str]): The primary keys for the specified database table.
    """

    def __init__(self, cls: T, table_name: str, primary_keys: List[str]):
        """Initialize an instance based on the specified parameters.

        Args:
            cls: The entity class which corresponding to the database table to be interfaced with.
            table_name: The name of the table to be interfaced with.
            primary_keys: The primary keys for the table specified.
        """
        self.TABLE_NAME = table_name
        self.CLASS = cls
        self.PRIMARY_KEYS = primary_keys

    def call_sql_query(self, query: str, values: List[str], map_to_object: bool = False) -> 'List[T] | List[dict]':
        """[UNSAFE] Directly call a SQL query.

        This method directly calls the database, allowing any SQL query to be performed. This is \
        highly unsafe and should only be used if absolutely necessary for the execution of a \
        complex behavior not otherwise supported herein. If this method must be used, all input \
        values should be fed through the values parameter such that opportunities for \
        injection are reduced.

        Args:
            query (str): The query to be executed.
            values (List[str]): The values to be resolved into the query.
            map_to_object (bool, optional): Whether to map the results to the entity class.
                Defaults to False.

        Returns:
            List[T]: If map_to_object is set.
            List[dict]: If map_to_object is not set.

        Examples:
            >>> from incollege.entity.User import User
            >>> helper = UniversalRepositoryHelper(User, 'users', ['user_id'])
            >>> some_users = helper.call_sql_query(f'SELECT * FROM users WHERE user_id = (?)',
            >>> ['some_user_id'], True)
            >>> print(some_users[0].username)
            'some_username'
        """
        query = f"{query}"
        cursor = get_connection().cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        if results:
            column_names = [description[0] for description in cursor.description]
            result_list = [dict(zip(column_names, row)) for row in results]
            if map_to_object:
                return [self.__convert_to_instance(data) for data in result_list]
            else:
                return result_list
        else:
            return []

    def get_record_count(self) -> int:
        """Get the number of database rows for this table.

        Returns:
            int: Number of database rows for this table.

        Examples:
            >>> from incollege.entity.User import User
            >>> helper = UniversalRepositoryHelper(User, 'users', ['user_id'])
            >>> print(helper.get_record_count())
            >>> # Assume there are 35 record in the database
            '35'
        """
        query = f"SELECT COUNT(1) FROM {self.TABLE_NAME}"
        cursor = get_connection().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

    def __get_objects_conditional(self, condition_string: str, keys: dict, limit: int = 20,
                                  offset: int = 0, fuzzy: bool = False) -> List[T]:
        """Get the objects from the table matching the condition string.

        Args:
            condition_string (str): The WHERE clause to match on.
            keys (dict): The dictionary to obtain the matchable values from.
            limit (int): Result count limit.
            offset (int): Pagination offset.
            fuzzy (bool): Whether to enable partial matching (using LIKE and %).

        Returns:
            List[T]: A list of objects matching the input criteria.
        """
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {condition_string} LIMIT (?) OFFSET (?)"

        cursor = get_connection().cursor()
        cursor.execute(query, create_tuple(keys, fuzzy) + tuple([limit, offset]))

        results = cursor.fetchall()

        if results:
            column_names = [description[0] for description in cursor.description]
            result_list = [dict(zip(column_names, row)) for row in results]
            return [self.__convert_to_instance(data) for data in result_list]
        else:
            return []

    def get_objects_fuzzy(self, keys: dict, limit: int = 20, offset: int = 0) -> List[T]:
        """Get fuzzy-matching objects based on keys.

        Args:
            keys (dict): The keys to match against.
            limit (int): Result count limit.
            offset (int): Pagination offset.

        Returns:
            List[T]: List of objects matching criteria.

        Examples:
            >>> from incollege.entity.User import User
            >>> helper = UniversalRepositoryHelper(User, 'users', ['user_id'])
            >>> print(helper.get_objects_fuzzy({'first_name': 'aust'}))

        """
        condition_string = create_condition_string(keys, 'AND', True)
        return self.__get_objects_conditional(condition_string, keys, limit, offset, True)

    def get_objects_intersection(self, keys: dict, limit: int = 20, offset: int = 0) -> List[T]:
        """Get fully-matching objects based on keys.

        Args:
            keys (dict): The keys to match against.
            limit (int): Result count limit.
            offset (int): Pagination offset.

        Returns:
            List[T]: List of objects matching criteria.
        """
        condition_string = create_condition_string(keys, 'AND', False)
        return self.__get_objects_conditional(condition_string, keys, limit, offset)

    def get_objects_union(self, keys: dict, limit: int = 20, offset: int = 0) -> List[T]:
        """Get partially-matching objects based on keys.

        Args:
            keys (dict): The keys to match against.
            limit (int): Result count limit.
            offset (int): Pagination offset.

        Returns:
            List[T]: List of objects matching criteria.
        """
        condition_string = create_condition_string(keys, 'OR', False)
        return self.__get_objects_conditional(condition_string, keys, limit, offset)

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
        original = self.get_objects_intersection(mutated_primary_keys)
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

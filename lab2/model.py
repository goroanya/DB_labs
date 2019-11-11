import psycopg2


class Model:
    def __init__(self, database, user, password):
        try:
            self.connection = psycopg2.connect(host="localhost", port="5432",
                                               database=database, user=user, password=password)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Помилка при з'єднанні з PostgreSQL", error)

    def create_db(self):
        f = open("create_db.txt", "r")

        self.cursor.execute(f.read())
        self.connection.commit()

    def insert(self, tname, **kwargs):
        columns = kwargs.keys()
        values = [f"'{val}'" for val in kwargs.values()]

        query = f'INSERT INTO {tname} ({", ".join(columns)}) VALUES ({", ".join(values)});'

        self.cursor.execute(query)
        self.connection.commit()

    def delete(self, tname, **kwargs):
        col_value_array = [f"{key}='{kwargs[key]}'" for key in kwargs]

        query = f'DELETE FROM {tname} WHERE {" and".join(col_value_array)}'

        self.cursor.execute(query)
        self.connection.commit()

    def update(self, tname, condition,  **kwargs):
        col_value_array = [f"{key}='{kwargs[key]}'" for key in kwargs]
        key, value = condition

        query = f'UPDATE {tname} SET {", ".join(col_value_array)} WHERE {key}={value}'

        self.cursor.execute(query)
        self.connection.commit()

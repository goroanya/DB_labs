import psycopg2


class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost", port="5432",
                                               database='db_lab2', user='goroanya', password='goroanya99')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Помилка при з'єднанні з PostgreSQL", error)

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def create_db(self):
        f = open("create_db.txt", "r")

        self.cursor.execute(f.read())
        self.connection.commit()

    def get(self, tname, condition):
        try:
            query = f'SELECT * FROM {tname}'

            if condition:
                query += ' WHERE ' + condition

            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, tname, columns, values):
        try:
            query = f'INSERT INTO {tname} ({columns}) VALUES ({values});'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def delete(self, tname, condition):
        try:
            query = f'DELETE FROM {tname} WHERE {condition};'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, tname, condition, statement):
        try:
            query = f'UPDATE {tname} SET {statement} WHERE {condition}'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def search_task_by_worker_position(self, positions):
        try:
            query = f'''
            SELECT * from task
            WHERE id in(
                SELECT task_id FROM worker_task
                JOIN worker on worker_task.worker_id=worker.id
                WHERE LOWER(position) in ({positions.lower()})
            );'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def search_worker_by_task_is_done(self, is_done):
        try:
            query = f'''
            SELECT * from worker
            WHERE id in(
                SELECT worker_id FROM worker_task
                JOIN task on task.id=worker_task.task_id
                WHERE isDone={is_done});'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fts_without_word(self, word):
        query = f'''
        select project_name, task_name, task_description from (
        select
            p.name as project_name,
            task.name as task_name,
            task.description as task_description,
            to_tsvector(p.name) ||
            to_tsvector(task.name) ||
            to_tsvector(task.description) as document,
            to_tsquery('!{word}') as query
        from task
        join project p on task.project_id = p.id
        ) search
        where document @@ query;
        '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fts_phrase(self, phrase):
        query = f'''
        select
        ts_headline(project_name, query, 'StartSel=\033[94m, StopSel=\033[0m'),
        ts_headline(task_name, query, 'StartSel=\033[94m, StopSel=\033[0m'),
        ts_headline(task_description, query, 'StartSel=\033[94m, StopSel=\033[0m')l
        from (
        select
            p.name as project_name,
            task.name as task_name,
            task.description as task_description,
            to_tsvector(p.name) ||
            to_tsvector(task.name) ||
            to_tsvector(task.description) as document,
            phraseto_tsquery('{phrase}') as query
        from task
        join project p on task.project_id = p.id
        ) search
        where document @@ query;
        '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fillTaskByRandomData(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomDepartments()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > 10;
                INSERT INTO department (name, number_of_workers, manager)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    (random() * (50 - 1) + 1)::integer,
                    substring(md5(random()::text), 1, 15)
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomDepartments();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()

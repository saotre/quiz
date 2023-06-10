from models import Question, Category


class PostgresSaver:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_question(self, questions: list[Question], categories: list[Category]) -> None:
        self._insert_data('category', categories)
        self._insert_data('questions', questions)

    def _insert_data(self, table: str, extract_data: list[Question] | list[Category]) -> None:
        cursor = self.pg_conn.cursor()
        fields_table = extract_data[0].__fields__

        str_fields = ','.join(field for field in fields_table)
        str_s = ','.join('%s' for _ in fields_table)

        args = ','.join(cursor.mogrify(f"({str_s})", tuple(item.__dict__.values())).decode() for item in extract_data)

        query_str = f"""INSERT INTO content.{table}
            ({str_fields})
            VALUES {args}
            ON CONFLICT (id) DO NOTHING;"""

        cursor.execute(query_str)


class PostgresReader:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def get_last_record(self):
        query_str = """
        select
            q.id,
            q.question,
            q.answer,
            q.created_at,
            c.title as category
        from content.questions as q
        inner join content.category as c
        on q.category_id = c.id
        ORDER BY q.created_rec DESC
        limit 1        
        """
        cursor = self.pg_conn.cursor()
        cursor.execute(query_str)
        rec = cursor.fetchone()

        return {} if rec is None else dict(rec)


class PostgresChecker:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def _check_exist(self, table: str, check_value: int) -> bool:
        cursor = self.pg_conn.cursor()
        exists_query = f'''
            select exists (
                select 1
                from content.{table}
                where id = {check_value}
            )'''
        cursor.execute(exists_query)
        return cursor.fetchone()[0]

    def check_question(self, question_id: int) -> bool:
        return self._check_exist('questions', question_id)

    def check_category(self, category_id: int) -> bool:
        return self._check_exist('category', category_id)

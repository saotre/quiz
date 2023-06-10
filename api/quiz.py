import requests
from models import Question, Category, POSTGRES_DSN
from db import PostgresSaver, PostgresChecker, PostgresReader
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
import datetime


def get_random_question_from_api(questions_num: int) -> dict:
    #"https://jservice.io/api/random?count=1"
    url = "https://jservice.io/api/random"

    payload = {"count": questions_num}

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()


def get_question(questions_num: int) -> dict:
    #last question existing in DB. we will return it as a response to a post request to our API
    last_question = {}

    with psycopg2.connect(**POSTGRES_DSN, cursor_factory=DictCursor) as pg_conn:
        try:

            pg_reader = PostgresReader(pg_conn)
            last_question = pg_reader.get_last_record()


            pg_checker = PostgresChecker(pg_conn)

            questions = []
            categories = []

            while True:
                response_json = get_random_question_from_api(questions_num)

                more_quest = 0

                for question in response_json:
                    if pg_checker.check_question(question["id"]):
                        more_quest += 1
                        continue

                    questions.append(Question(**question, created_rec=datetime.datetime.now()))

                    if question["category"]:
                        category = Category(**question["category"])
                    else:
                        category = Category(id=99999, title='incognito')

                    categories.append(category)

                if more_quest == 0:
                    break

            pg_saver = PostgresSaver(pg_conn)
            pg_saver.save_question(questions, categories)
            print("data recorded successfully...")

        finally:
            if pg_conn.closed:
                pg_conn.close()

    return last_question


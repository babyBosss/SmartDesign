import psycopg2


def get_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        port='5432',
        user="postgres",
        password="mysecretpassword",
        database="postgres")


with get_connection() as db:
    cur = db.cursor()
    with open("script.sql", "r") as file:
        cur.execute(file.read())
        db.commit()


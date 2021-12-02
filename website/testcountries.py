import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    c = conn.cursor()
    c.execute("SELECT * FROM country")

    rows = c.fetchall()

    for row in rows:
        print(row)





def main():
    database = r"database.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("2. Query all tasks")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()

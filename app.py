from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'mydatabase.db'  # Replace with your actual database filename

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row['name'] for row in cursor.fetchall()]
    return tables

def get_table_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM '{table_name}'")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return columns, rows

@app.route('/')
def index():
    conn = get_db_connection()
    tables = get_all_tables(conn)
    conn.close()
    return render_template('index.html', tables=tables)

@app.route('/table/<table_name>')
def view_table(table_name):
    conn = get_db_connection()
    tables = get_all_tables(conn)
    if table_name not in tables:
        return f"Table '{table_name}' not found.", 404
    columns, rows = get_table_data(conn, table_name)
    conn.close()
    return render_template('table.html', table_name=table_name, columns=columns, rows=rows, tables=tables)

if __name__ == '__main__':
    app.run(debug=True)

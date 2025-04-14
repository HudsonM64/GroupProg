from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'mydatabase.db'  

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [row['name'] for row in cur.fetchall()]

@app.route('/')
def index():
    conn = get_db_connection()
    tables = get_all_tables(conn)
    conn.close()
    return render_template('index.html', tables=tables)

@app.route('/table/<table_name>', methods=['GET', 'POST'])
def view_table(table_name):
    conn = get_db_connection()
    tables = get_all_tables(conn)

    if table_name not in tables:
        return f"Table '{table_name}' not found.", 404

    cursor = conn.cursor()
    message = None
    error = None

    if request.method == 'POST':
        columns = request.form.getlist('column')
        values = request.form.getlist('value')
        placeholders = ','.join(['?'] * len(values))
        col_clause = ','.join(columns)
        try:
            cursor.execute(f'INSERT INTO "{table_name}" ({col_clause}) VALUES ({placeholders})', values)
            conn.commit()
            message = "Row added successfully!"
        except Exception as e:
            error = f"Error adding row: {str(e)}"

    cursor.execute(f'SELECT * FROM "{table_name}"')
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return render_template('table.html', table_name=table_name, tables=tables,
                           columns=columns, rows=rows, message=message, error=error)

@app.route('/query', methods=['GET', 'POST'])
def query():
    result = None
    error = None
    query_text = ''
    if request.method == 'POST':
        query_text = request.form['query']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query_text)

            if query_text.strip().lower().startswith('select'):
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
            else:
                conn.commit()
                result = f"Query executed successfully."

            conn.close()
        except Exception as e:
            error = str(e)
            result = None

        return render_template('query.html', result=result, columns=columns if result and isinstance(result, list) else [], error=error, query_text=query_text)

    return render_template('query.html', result=result, columns=[], error=error, query_text=query_text)

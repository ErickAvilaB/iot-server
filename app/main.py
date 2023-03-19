""" Main file for the Flask server """
from flask import Flask, jsonify, render_template, request
import mysql.connector
from dotenv import load_dotenv
from os import environ

app = Flask(__name__)
load_dotenv()

# Load the environment variables
db_user = environ.get('DB_USER')
db_password = environ.get('DB_PASSWORD')
db_name = environ.get('DB_NAME')
db_host = environ.get('DB_HOST')
db_port = environ.get('DB_PORT')


def connect_db():
    """ Connect to the database """

    # MySQL credentials
    data_base = mysql.connector.connect(
        user=db_user,
        password=db_password,
        database=db_name,
        host=db_host,
        port=db_port
    )
    return data_base


@app.get('/')
def main():
    """ Render the main page """
    return render_template('index.html')


@app.get('/get_state/<int:identifier>')
def get_state(identifier):
    """ Get the state of the led """

    # Get the state in the database
    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    cursor.execute(f"SELECT id, state FROM led WHERE id = {identifier}")
    result = cursor.fetchone()  # Get the query result

    # Return error message if the id is not found
    if result is None:
        return jsonify({'message': 'Error getting the state'})

    # Return result
    return jsonify(result)


@app.put('/put_state')
def put_state():
    """ Update the state of the led """

    # Get the data from the request
    request_data = request.get_json()
    identifier = request_data['id']
    state = request_data['state']

    # Update the state in the database
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE led SET state = {state} WHERE id = {identifier}")
    updated = cursor.rowcount  # Get the number of rows updated
    connect.commit()
    connect.close()
    cursor.close()

    # Return error message if rows are not updated
    if updated == 0:
        return jsonify({'message': 'Error updating the state'})

    succes_result = {
        "message": 'State updated successfully.',
        "rows_updated": updated
    }

    # Return result
    return jsonify(succes_result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

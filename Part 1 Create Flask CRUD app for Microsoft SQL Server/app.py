from flask import Flask, render_template, request
import pyodbc
from credentials import conn_str

app = Flask(__name__)

# Connection details for Azure SQL Database
#conn_str =f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:mybankssqlserver.database.windows.net,1433;Database=BanksDatabase;Uid=azureuser;Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# Define the route for creating a new record
@app.route('/create', methods=['GET', 'POST'])
def create_bank():
    if request.method == 'POST':
        # Retrieve form data
        id = request.form['id']
        name = request.form['name']
        location = request.form['location']
        
        # Create a new connection to Azure SQL Server
        conn = pyodbc.connect(conn_str)
        
        # Insert new record into the "Banks" table
        cursor = conn.cursor()
        query = "INSERT INTO Banks (id, name, location) VALUES (?, ?, ?);"
        cursor.execute(query, (id, name, location))
        conn.commit()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Redirect to a success page or display a success message
        return "Record created successfully!"
    
    # Render the form for creating a new record
    return render_template('create.html')


# Route to list all banks
@app.route('/banks', methods =['GET'])
def list_banks():
    # Create a new connection to Azure SQL Server
    conn = pyodbc.connect(conn_str)
    
    # Query all banks from the "Banks" table
    cursor = conn.cursor()
    query = "SELECT * FROM Banks"
    cursor.execute(query)
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    # Render the template with the list of banks
    return render_template('banks.html', banks=rows)


# Route to retrieve a bank record
@app.route('/banks/<int:bank_id>')
def get_bank(bank_id):
    # Create a new connection to Azure SQL Server
    conn = pyodbc.connect(conn_str)

    # Query the database to retrieve the bank details
    cursor = conn.cursor()
    query = "SELECT * FROM Banks WHERE id = ?"
    cursor.execute(query, (bank_id,))

    # Fetch the row
    row = cursor.fetchone()

    if row:
        # Extract the bank details from the row
        bank_id = row[0]
        bank_name = row[1]
        bank_location = row[2]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Render the template with the bank details
        return render_template('bank_details.html', bank_id=bank_id, bank_name=bank_name, bank_location=bank_location)
    else:
        # Handle the case where the bank ID is not found
        cursor.close()
        conn.close()
        return "Bank not found."


# Route to update a bank record
@app.route('/updatebank', methods=['GET','POST'])
def update_bank():
    
    if request.method == 'POST': 
    # Retrieve form data
        bank_id = request.form['id']
        name = request.form['name']
        location = request.form['location']
        
        try:
            # Create a connection to the Azure SQL Database
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Update the bank record
            query = "UPDATE Banks SET name=?, location=? WHERE id = ?;"
            cursor.execute(query, (name, location, bank_id))

            if cursor.rowcount == 0:
                return "No bank record found for the specified ID. Update unsuccessful."
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            return "Bank record updated successfully!"
        except pyodbc.Error as e:
            return f"An error occurred: {str(e)}"
    else:
        return render_template('update.html')


# Route to delete a bank record
@app.route('/deletebank/<int:bank_id>', methods=['GET','POST'])
def delete_bank(bank_id):
    # Create a new connection to Azure SQL Server
    conn = pyodbc.connect(conn_str)

    # Create a cursor to execute the SQL query
    cursor = conn.cursor()

    # Execute the SQL query to delete the bank record
    query = "DELETE FROM Banks WHERE id = ?"

    try:
        conn.autocommit = False
        cursor.execute(query, bank_id)
    except pyodbc.DatabaseError as e:
        raise e
        cursor.rollback()
    else:
        cursor.commit()
    finally:
        conn.autocommit = True

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return "Bank deleted successfully!"


if __name__ == '__main__':
    app.run()

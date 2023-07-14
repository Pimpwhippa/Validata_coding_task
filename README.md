# Validata_coding_task

For Part 1

1.initialization of Azure SQL Server can be done by following the instructions in this link
https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql-db&source=recommendations&tabs=azure-portal
note your Azure SQL Database password to connect to it

2.instructions on how to set up and run the application, including any necessary dependencies or libraries

git clone

cd 'Part 1 Create Flask CRUD app for Microsoft SQL Server'

create credentials.py and put your Azure SQL Database password in like this 
password= "yourpassword"

virtualenv .env && source .env/bin/activate && pip install -r requirements.txt

flask run


For Part 2

Loan_Train.csv is the original data. Run the preprocessing part of the preprocessing_script.py on it, you will get preprocessed_dataset.csv
The training and evaluation code is also inside preprocessing_script.py. The summary and insights report is in .ipynb file.

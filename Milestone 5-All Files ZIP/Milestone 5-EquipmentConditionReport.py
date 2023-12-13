"""
Group Four Kevin Meza, Dominique Monroe, Shane Tinsley
12/8/23 Module 11 Milestone 3
Script to perform an annual inspection of equipment in the database.
Queries the database to find items with specific condition descriptions 
indicating items aged 5 years and older and items that have been damaged. 
Displays report of all items meeting criteria and then automatically updates to 'Out of Order'. 
References Textbook and trial and error.
***Warning Running this report updates the database****
"""

import mysql.connector
from tabulate import tabulate
from datetime import datetime, timedelta


# Function to connect to the database
def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Limecows02!Lime!",
            database="TravelAgencyFinal",            
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def conduct_annual_inspection(mydb):
    try:
        cursor = mydb.cursor()

        
        

        # Find items with specific condition descriptions
        query = """
            SELECT EquipmentID, EquipmentName, EquipmentWholeSalePrice, EquipmentStatus, ConditionDescription, EquipmentPurchaseDate
            FROM Equipment
            WHERE EquipmentStatus LIKE '%Out of Order%' 
                OR ConditionDescription LIKE '%tear%' 
                OR ConditionDescription LIKE '%scratch%' 
                OR EquipmentPurchaseDate < DATE_SUB(NOW(), INTERVAL 5 YEAR)
        """ 
        
        cursor.execute(query)
        outdated_items = cursor.fetchall()

        if outdated_items:
            print("\n------------------------------------------------------------------------------------------------------------------------")
            print("\033[1;32mReport: Outdated and defective items identified:\033[0m")
            headers = ["Equipment ID", "Equipment Name", "Wholesale Price", "Equipment Status", "Condition Description", "Equipment Purchase Date"]
            print(tabulate(outdated_items, headers=headers, tablefmt="pretty"))
            print("\033[1;32m'Equipment Status' has been *AUTOMATICALLY UPDATED* to \033[0m\033[1;31m'Out of Order'\033[0m\033[1;32m... Report DOES NOT reflect changes.\033[0m")
            print("------------------------------------------------------------------------------------------------------------------------\n")

            # Update EquipmentStatus for outdated items
            update_query = """
                UPDATE Equipment
                SET EquipmentStatus = 'Out of Order'
                WHERE EquipmentID IN (%s)
            """
            outdated_ids = ", ".join([str(item[0]) for item in outdated_items])
            update_query = update_query % outdated_ids

            cursor.execute(update_query)
            mydb.commit()
        else:
            print("No outdated items found.")

    except mysql.connector.Error as err:
        print(f"Error during annual inspection: {err}")
    finally:
        cursor.close()

def main():
    try:
        # Connect to the database
        mydb = connect_to_database()

        # Perform the annual inspection
        conduct_annual_inspection(mydb)

        # Close the database connection
        mydb.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

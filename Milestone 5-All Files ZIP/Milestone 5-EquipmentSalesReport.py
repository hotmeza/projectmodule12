"""
Group Four Kevin Meza, Dominique Monroe, Shane Tinsley 
12/8/23 Module 11 Milestone 3
Python script connects to a database, retrieves sales data for two quarters in 2022, 
calculates equipment sales percentages for each quarter, and 
provides recommendations based on the sales criteria. 
References Textbook and Trial and Error.
"""

import mysql.connector
from datetime import datetime
from tabulate import tabulate

def connect_to_database():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Limecows02!Lime!",
            database="TravelAgencyFinal"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def execute_query(cursor, query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return []

def evaluate_sales():
    mydb = connect_to_database()
    if mydb:
        cursor = mydb.cursor()
        try:
            start_date_1 = datetime(2022, 7, 1).date()
            end_date_1 = datetime(2022, 9, 30).date()
            start_date_2 = datetime(2022, 10, 1).date()
            end_date_2 = datetime(2022, 12, 31).date()

            total_payments_query = """
                SELECT SUM(PaymentAmount) AS TotalPayments
                FROM Payment
                WHERE PaymentDate BETWEEN %s AND %s AND PaymentStatus = 'Paid'
            """

            cursor.execute(total_payments_query, (start_date_1, end_date_2))
            total_payments = cursor.fetchone()[0]

            if total_payments is not None:  
                print(tabulate([["Total payments collected:", f"${total_payments:.2f}"]],
                               headers=["Total Payments Collected", "Total"], tablefmt="pretty"))

                def fetch_equipment_sales(query, date_start, date_end):
                    result = execute_query(cursor, query, (date_start, date_end))
                    return result[0][0] if result[0][0] is not None else 0

                equipment_sales_query_1 = """
                    SELECT SUM(e.EquipmentRetailPrice) AS TotalEquipmentRetailPrice
                    FROM Customer_Order co
                    JOIN Equipment e ON co.EquipmentID = e.EquipmentID
                    JOIN Payment p ON co.PaymentID = p.PaymentID
                    WHERE p.PaymentDate BETWEEN %s AND %s AND p.PaymentStatus = 'Paid'
                """

                total_equipment_sales_1 = fetch_equipment_sales(equipment_sales_query_1, start_date_1, end_date_1)
                total_equipment_sales_2 = fetch_equipment_sales(equipment_sales_query_1, start_date_2, end_date_2)

                sales_percentage_1 = (total_equipment_sales_1 / total_payments) * 100 if total_payments != 0 else 0
                sales_percentage_2 = (total_equipment_sales_2 / total_payments) * 100 if total_payments != 0 else 0

                sales_data = [
                    ["First Quarter", f"${total_equipment_sales_1:.2f}", f"{sales_percentage_1:.2f}%"],
                    ["Second Quarter", f"${total_equipment_sales_2:.2f}", f"{sales_percentage_2:.2f}%"]
                ]
                headers = ["Quarter", "Total Equipment Sales", "Equipment Sales Percentage"]

                print(tabulate(sales_data, headers=headers, tablefmt="pretty"))

                if sales_percentage_1 < 40 and sales_percentage_2 < 40:
                    recommendation = [
                        ["Equipment sales contribute less than 40% for two consecutive quarters."],
                        ["Reevaluate marketing strategy, consider e-commerce expansion, or adjust inventory levels."]
                    ]
                    recommendation_headers = ["Recommendations"]
                    print("\nRecommendation:")
                    print(tabulate(recommendation, headers=recommendation_headers, tablefmt="pretty"))
                else:
                    print("\nEquipment sales meet criteria.")
            else:
                print("No total payments found for the specified period.")
            
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            mydb.close()

if __name__ == "__main__":
    evaluate_sales()

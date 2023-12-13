""" 
Group Four Kevin Meza, Dominique Monroe, Shane Tinsley
12/8/23 Module 11 Milestone 3
This Python script connects to a MySQL database representing a travel agency's system.
It retrieves booking data by continent for the fiscal year 2022, 
analyzes quarterly downward trends in bookings, and displays the results using 
tabulated formats. The code consists of functions to handle database connections,
fetch booking data, display table results, analyze trends, and finally, 
present the information. References text book and trial and error.
"""
import mysql.connector
from tabulate import tabulate 


def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Limecows02!Lime!",
            database="TravelAgencyFinal"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def fetch_booking_data_by_continent(cursor):
    query = """
        SELECT
            YEAR(BookingDate) AS BookingYear,
            QUARTER(BookingDate) AS BookingQuarter,
            Location.LocationName AS Continent,
            COUNT(Booking.BookingID) AS TotalBookings
        FROM
            Booking
        JOIN Trip ON Booking.TripID = Trip.TripID
        JOIN Location ON Trip.LocationID = Location.LocationID
        WHERE
            YEAR(BookingDate) = 2022
        GROUP BY
            YEAR(BookingDate), QUARTER(BookingDate), Location.LocationName
        ORDER BY
            Location.LocationName, YEAR(BookingDate), QUARTER(BookingDate)
    """
    cursor.execute(query)
    return cursor.fetchall()

def display_table_results(result):
    headers = ["BookingYear", "BookingQuarter", "Continent", "TotalBookings"]
    print(tabulate(result, headers=headers, tablefmt="grid"))
    print()  # Add a newline for space between tables

def analyze_downward_trend(result):
    continent_data = {}
    for row in result:
        continent = row[2]
        if continent not in continent_data:
            continent_data[continent] = []
        continent_data[continent].append(row)

    trend_data = []
    for continent, data in continent_data.items():
        trend_downward = "Yes" if len(data) >= 2 and all(data[i][3] > data[i + 1][3] for i in range(len(data) - 1)) else "No"
        trend_data.append([continent, trend_downward])

    print(tabulate(trend_data, headers=["Continent", "Downward Trend"], tablefmt="grid"))

def display_booking_data_by_continent():
    try:
        mydb = connect_to_database()
        if mydb:
            cursor = mydb.cursor()
            result = fetch_booking_data_by_continent(cursor)

            print("\nBooking Data by Continent:")
            display_table_results(result)

            print("Analyzing Downward Trend for Each Continent:")
            analyze_downward_trend(result)

            cursor.close()
            mydb.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Displaying table results for bookings by continent in fiscal year 2022
display_booking_data_by_continent()

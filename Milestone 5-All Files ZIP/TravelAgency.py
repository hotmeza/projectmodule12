"""
Group Four Kevin Meza, Dominique Monroe, Shane Tinsley
12/8/23 Module 11 Milestone 3 Updated, Python Script that Creates TravelAgency Database
and imports data into tables using different function and methods including random number generation
to generate sample data then displays the tables in neatly organized output. 
Uses main method and error checking. 
References text books and lots of trial and error.
"""

import mysql.connector
import random
from random import sample
from tabulate import tabulate
from datetime import datetime, timedelta

#Function to create Database
def connect_to_database():
    # Replace 'YourPassword' with your actual database password
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Limecows02!Lime!"
    )
    return mydb

#Function to crate tables
def create_tables(mydb):
    cursor = mydb.cursor()

    create_db_query = "CREATE DATABASE IF NOT EXISTS TravelAgencyFinal"

    try:
        cursor.execute(create_db_query)
        print("Database 'TravelAgencyFinal' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

    cursor.execute("USE TravelAgencyFinal")

    create_tables_query = [
    """
    CREATE TABLE IF NOT EXISTS Location (
        LocationID INT AUTO_INCREMENT PRIMARY KEY,
        LocationName VARCHAR(100),
        Country VARCHAR(50),
        City VARCHAR(50),
        StateProvidence VARCHAR(50),
        PostalCode VARCHAR(20)
    )""",
    """
    CREATE TABLE IF NOT EXISTS Guide (
        GuideID INT AUTO_INCREMENT PRIMARY KEY,
        LegalFirstName VARCHAR(50),
        LegalMiddleName VARCHAR(50),
        LegalLastName VARCHAR(50),
        PreferredName VARCHAR(50),
        Specialty VARCHAR(100),
        ExperienceLevel VARCHAR(50),
        ContactNumber VARCHAR(20),
        EmailAddress VARCHAR(100)
    )""",
    """
    CREATE TABLE IF NOT EXISTS Trip (
        TripID INT AUTO_INCREMENT PRIMARY KEY,
        LocationID INT,
        GuideID INT,
        StartDate DATE,
        EndDate DATE,
        TripCategory ENUM('Adventure', 'Camping', 'Hiking', 'Biking'),
        TripDescription TEXT,
        FOREIGN KEY (LocationID) REFERENCES Location(LocationID),
        FOREIGN KEY (GuideID) REFERENCES Guide(GuideID)
    )""",
    """
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        LegalFirstName VARCHAR(50),
        LegalMiddleName VARCHAR(50),
        LegalLastName VARCHAR(50),
        PreferredName VARCHAR(50),
        Email VARCHAR(100),
        Phone VARCHAR(20),
        Address VARCHAR(100),
        Country VARCHAR(50),
        City VARCHAR(50),
        State VARCHAR(50),
        PostalCode VARCHAR(20)
    )""",
    """
    CREATE TABLE IF NOT EXISTS Payment (
        PaymentID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        PaymentType ENUM('Cash', 'Card', 'Wire', 'EFT'),
        Description TEXT,
        PaymentAmount DECIMAL(10,2),
        PaymentStatus ENUM('Pending', 'Paid', 'Declined'),
        PaymentDate DATE,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    )""",    
    """
    CREATE TABLE IF NOT EXISTS Booking (
        BookingID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        TripID INT,
        PaymentID INT,
        BookingDate DATE,
        BookingNotes TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (TripID) REFERENCES Trip(TripID),
        FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID)
    )""",
    """
    CREATE TABLE IF NOT EXISTS Equipment (
        EquipmentID INT AUTO_INCREMENT PRIMARY KEY,
        EquipmentName VARCHAR(100),
        EquipmentWholeSalePrice DECIMAL(10, 2),
        EquipmentRetailPrice DECIMAL(10,2),
        EquipmentStatus ENUM('Available', 'Rented', 'Out of Order'),
        ConditionDescription VARCHAR(100),
        Quantity INT,
        EquipmentPurchaseDate DATE
    )""",
    """
    CREATE TABLE IF NOT EXISTS Review (
        ReviewID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        TripID INT,
        GuideID INT,
        ReviewDate DATE,
        Rating INT,
        ReviewComment TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (TripID) REFERENCES Trip(TripID),
        FOREIGN KEY (GuideID) REFERENCES Guide(GuideID)
    )""",
    """
    CREATE TABLE IF NOT EXISTS Customer_Order ( 
        OrderID INT AUTO_INCREMENT PRIMARY KEY,
        BookingID INT,
        EquipmentID INT,
        CustomerID INT,
        PaymentID INT,
        FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID),
        FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID),
        FOREIGN KEY (BookingID) REFERENCES Booking(BookingID),
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    
    )"""
]

    try:
        for query in create_tables_query:
            cursor.execute(query)
        print("Tables created successfully.")
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
    finally:
        cursor.close()

#Function to generate and insert table data, some date is pulled from the case study while others are randomly generated.
def insert_data(mydb):
    try:
        cursor = mydb.cursor()
        
        insert_customer_query = """
            INSERT INTO Customer (
                LegalFirstName,
                LegalMiddleName,
                LegalLastName,
                PreferredName,
                Email,
                Phone,
                Address,
                Country,
                City,
                State,
                PostalCode
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Insert 10 customers into the 'Customer' table
        customers = [
            ("John", "Doe", "Smith", "John", "johndoe@email.com", "123-456-7890", "123 Main St.", "USA", "New York", "NY", "10001"),
            ("Jane", "Joanne", "Smith", "Jane", "janedoe@email.com", "987-654-3210", "456 Elm St.", "USA", "Los Angeles", "CA", "90210"),
            ("Bruce", " ", "Brown", "Bucky", "peterjones@email.com", "123-456-7890", "789 Oak St.", "USA", "Chicago", "IL", "60601"),
            ("Mary", "Jane", "Brown", "Mary Jane", "mary@email.com", "987-654-3210", "1011 Pine St.", "USA", "Houston", "TX", "77001"),
            ("David","Jerry", "Scott", "Candy", "davidwilliams@email.com", "123-456-7890", "1234 Maple St.", "USA", "Phoenix", "AZ", "85001"),
            ("Sarah", "Tammy", "Williams", "Sarah Williams", "sarahwilliams@email.com", "987-654-3210", "5678 Birch St.", "USA", "Philadelphia", "PA", "19101"),
            ("Michael", "Brown", "Davis", "Michael", "michaelbrown@email.com", "123-456-7890", "9012 Ash St.", "USA", "San Antonio", "TX", "78229"),
            ("Jessica", "Gigi", "Davis", "Gigi", "jessica@email.com", "987-654-3210", "1314 Elm St.", "USA", "San Diego", "CA", "92101"),
            ("James", "Miller", "Taylor", "James", "james@email.com", "123-456-7890", "1516 Oak St.", "USA", "Dallas", "TX", "75201"),
            ("Jennifer", "Bobby", "Taylor", "Jennifer Miller", "jennifermiller@email.com", "987-654-3210", "1718 Pine St.", "USA", "San Jose", "CA", "95112"),
        ]

        cursor.executemany(insert_customer_query, customers)
        print("Customers inserted successfully.")
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting customers: {err}")
    finally:
        cursor.close()  # Close the cursor in the finally block

    try:
        cursor = mydb.cursor()

        insert_location_query = """
            INSERT INTO Location (
                LocationName,
                Country,
                City,
                StateProvidence,
                PostalCode
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        # Define the locations data
        locations = [
            ("Europe", "France", "Paris", "Ile-de-France", "75000"),
            ("Europe", "Spain", "Madrid", "Madrid", "28001"),
            ("Europe", "Italy", "Rome", "Lazio", "00118"),
            ("Europe", "Germany", "Berlin", "Berlin", "10115"),
            ("Europe", "United Kingdom", "London", "England", "SW1A 1AA"),
            ("Asia", "China", "Beijing", "Beijing", "100000"),
            ("Asia", "Japan", "Tokyo", "Tokyo", "100-8111"),
            ("Asia", "India", "New Delhi", "Delhi", "110001"),
            ("Asia", "South Korea", "Seoul", "Seoul", "04524"),
            ("Asia", "United Arab Emirates", "Dubai", "Dubai", "12345"),
            ("Africa", "South Africa", "Cape Town", "Western Cape", "8000"),
            ("Africa", "Nigeria", "Lagos", "Lagos", "100001"),
            ("Africa", "Kenya", "Nairobi", "Nairobi", "00100"),
            ("Africa", "Egypt", "Cairo", "Cairo", "11511"),
            ("Africa", "Morocco", "Casablanca", "Casablanca-Settat", "20250"),
        ]

        # Execute the insert location query for each location
        cursor.executemany(insert_location_query, locations)

        # Commit changes to the database
        mydb.commit()

        print("Locations inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting locations: {err}")
    finally:
        # Close cursor in the finally block
        cursor.close()

    try:
        cursor = mydb.cursor()

        insert_guide_query = """
            INSERT INTO Guide (
                LegalFirstName, 
                LegalMiddleName, 
                LegalLastName, 
                PreferredName, 
                Specialty, 
                ExperienceLevel, 
                ContactNumber, 
                EmailAddress
            )             
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Guide data to be inserted
        guides_data = [
            ('John', '', 'MacNell', 'Mac', 'Hiking', 'Expert', '+1234567890', 'johnmac@example.com'),
            ('D.B.', '', 'Marland', 'Duke', 'Camping', 'Intermediate', '+1987654321', 'duke@example.com')
        ]

        # Execute the insert query for each guide
        cursor.executemany(insert_guide_query, guides_data)

        # Commit changes to the database
        mydb.commit()

        print("Guide data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data into Guide table: {err}")
    finally:
        # Close cursor in the finally block
        cursor.close()

    try:
        cursor = mydb.cursor()

        cursor.execute("SELECT LocationID FROM Location")
        location_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT GuideID FROM Guide")
        guide_ids = [row[0] for row in cursor.fetchall()]

        # Calculate the list of available dates within the date range
        available_dates = [
            datetime(2022, 1, 1) + timedelta(days=i) for i in range((datetime(2023, 11, 15) - datetime(2022, 1, 1)).days)
        ]

        # Shuffle the available dates to make them random
        random_dates = sample(available_dates, len(available_dates))

        trips = []
        for _ in range(100):
            location_id = random.choice(location_ids)
            guide_id = random.choice(guide_ids)
            start_date = random_dates.pop()  # Retrieve a random date from the shuffled list
            end_date = start_date + timedelta(weeks=2)
            trip_category = random.choice(['Adventure', 'Camping', 'Hiking', 'Biking'])
            trip_description = f"Trip to LocationID: {location_id} with GuideID: {guide_id}"
            trips.append((location_id, guide_id, start_date, end_date, trip_category, trip_description))

        insert_trip_query = """
            INSERT INTO Trip (
                LocationID, 
                GuideID, 
                StartDate, 
                EndDate, 
                TripCategory, 
                TripDescription)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.executemany(insert_trip_query, trips)
            print("Trips inserted successfully.")
            mydb.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data into Trip table: {err}")
        finally:
            cursor.close()  # Close the cursor after the insertions
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    try:
        cursor = mydb.cursor()

        # Fetching all CustomerIDs from the Customer table
        cursor.execute("SELECT CustomerID FROM Customer")
        customer_ids = [row[0] for row in cursor.fetchall()]

        # Fetch the start date of the chosen trip
        cursor.execute("SELECT StartDate FROM Trip")
        start_dates = [row[0] for row in cursor.fetchall()]

        # Generating unique payments
        payments = []
        for _ in range(200):
            start_date = random.choice(start_dates)
            customer_id = random.choice(customer_ids)  # Assuming customer_ids exist (IDs from Customer table)
            payment_type = random.choice(['Cash', 'Card', 'Wire', 'EFT'])
            description = f"Payment for CustomerID: {customer_id}"
            payment_amount = random.uniform(50, 500)  # Assuming payment amount range
            payment_date = start_date - timedelta(weeks=2)    # Replace this with actual end date
            payment_status = random.choice(['Pending', 'Paid', 'Declined'])
            payments.append((customer_id, payment_type, description, payment_amount, payment_status, payment_date))

        # SQL query to insert data into the Payment table
        insert_payment_query = """
            INSERT INTO Payment (
                CustomerID, 
                PaymentType, 
                Description, 
                PaymentAmount, 
                PaymentStatus, 
                PaymentDate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            # Execute the insert query for each payment
            cursor.executemany(insert_payment_query, payments)
            print("Payments inserted successfully.")

            # Commit changes to the database
            mydb.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data into Payment table: {err}")
        finally:
            # Close cursor and database connections
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}") 

    try:
        cursor = mydb.cursor()

        # Fetching all BookingIDs from the Booking table
        cursor.execute("SELECT BookingID FROM Booking")
        booking_ids = [row[0] for row in cursor.fetchall()]

        # Fetching all TripIDs from the Trip table
        cursor.execute("SELECT TripID FROM Trip")
        trip_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT StartDate, TripID FROM Trip")
        trip_data = cursor.fetchall()
        start_dates = {trip[1]: trip[0] for trip in trip_data}

        cursor.execute("SELECT PaymentID FROM Payment")
        payment_ids = [row[0] for row in cursor.fetchall()]

        bookings = []
        for _ in range(100):
            trip_id = random.choice(list(start_dates.keys()))
            start_date = start_dates[trip_id]
            customer_id = random.choice(customer_ids)  # Assuming customer_ids exist (IDs from Customer table)
            payment_id = random.choice(payment_ids)    # Assuming payment_ids exist (IDs from Payment table)
            booking_date = start_date - timedelta(weeks=4)    # Replace this with actual booking date
            booking_notes = "Some notes about the booking..."

            bookings.append((customer_id, trip_id, payment_id, booking_date, booking_notes))

        # SQL query to insert data into the Booking table
        insert_booking_query = """
            INSERT INTO Booking (CustomerID, TripID, PaymentID, BookingDate, BookingNotes)
            VALUES (%s, %s, %s, %s, %s)
        """

        try:
            # Execute the insert query for each booking
            cursor.executemany(insert_booking_query, bookings)
            print("Bookings inserted successfully.")

            # Commit changes to the database
            mydb.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data into Booking table: {err}")
        finally:
            # Close cursor and database connections
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
 

    try:
        cursor = mydb.cursor()

        # SQL query to insert data into the Equipment table
        insert_equipment_query = """
            INSERT INTO Equipment (
                EquipmentName,
                EquipmentWholeSalePrice,
                EquipmentRetailPrice,
                EquipmentStatus,
                ConditionDescription,
                Quantity,
                EquipmentPurchaseDate
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        # Equipment data
        equipment_data = [
            ("Tent", 80.00, 120.00, "Available", "Good condition", 50, datetime(2020, 1, 5)),
            ("Backpack", 40.00, 60.00, "Rented", "Slight wear", 100, datetime(2022, 1, 5)),
            ("Sleeping Bag", 50.00, 80.00, "Available", "Excellent condition", 75, datetime(1995, 1, 5)),
            ("Hiking Boots", 60.00, 100.00, "Available", "New", 30, datetime(2023, 1, 5)),
            ("Camping Stove", 70.00, 110.00, "Available", "Used, functional", 25, datetime(2020, 1, 5)),
            ("Headlamp", 25.00, 45.00, "Rented", "Lightly used", 80, datetime(2023, 1, 5)),
            ("Water Filter", 45.00, 70.00, "Available", "Like new", 40, datetime(2023, 1, 5)),
            ("Trekking Poles", 35.00, 55.00, "Available", "Good condition", 60, datetime(2023, 1, 5)),
            ("Cookware Set", 55.00, 90.00, "Out of Order", "Slight scratches", 45, datetime(2000, 1, 5)),
            ("First Aid Kit", 20.00, 35.00, "Out of Order", "Sealed, unopened", 90, datetime(2023, 1, 5)),
            ("Portable Chair", 30.00, 50.00, "Available", "Used but sturdy", 70, datetime(2023, 1, 5)),
            ("Navigation Compass", 15.00, 25.00, "Available", "Excellent condition", 100, datetime(2023, 1, 5)),
            ("Tarpaulin", 20.00, 40.00, "Available", "Minor tears, usable", 55, datetime(2023, 1, 5)),
            ("Camp Pillow", 10.00, 20.00, "Available", "Washed, clean", 120, datetime(2023, 1, 5)),
            ("Fire Starter Kit", 18.00, 30.00, "Available", "Unused", 85, datetime(2023, 1, 5)),
            ("Dry Bags", 22.00, 38.00, "Available", "Waterproof, intact", 65, datetime(2023, 1, 5)),
            ("Mosquito Net", 28.00, 48.00, "Available", "Like new", 75, datetime(2023, 1, 5)),
            ("Camp Shower", 32.00, 55.00, "Available", "Gently used", 50, datetime(2023, 1, 5)),
            ("Multi-tool", 40.00, 65.00, "Available", "Functional, good shape", 70, datetime(2023, 1, 5)),
            ("Camping Hammock", 50.00, 85.00, "Available", "Slight stains", 40, datetime(2023, 1, 5)),
            ("Emergency Whistle", 8.00, 15.00, "Available", "Compact, loud", 95, datetime(2023, 1, 5)),
            ("Solar Charger", 60.00, 100.00, "Available", "Efficient, reliable", 30, datetime(2023, 1, 5)),
            ("Handheld GPS", 70.00, 120.00, "Available", "Used for navigation", 25, datetime(2023, 1, 5)),
            ("Bear Canister", 40.00, 70.00, "Available", "Scratched, functional", 60, datetime(2023, 1, 5)),
            ("Camp Axe", 55.00, 95.00, "Available", "Sharp, used", 35, datetime(2023, 1, 5)),
        ]
        
        try:
            #Execute the insert query for each equipment entry
            cursor.executemany(insert_equipment_query, equipment_data)
            
            # Commit changes to the database
            mydb.commit()

            print("Equipment inserted successfully.")
        except mysql.connector.Error as err:
                print(f"Error inserting data into Equipment table: {err}")
        finally:
            # Close cursor and database connections
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")    
    
    try:
        cursor = mydb.cursor()

        reviews = [
            ("My experience with this travel agency was exceptional! From booking to the actual trip, everything was seamless. The staff was incredibly helpful and made sure every detail was taken care of. Highly recommended!"),
            ("I've used many travel agencies before, but this one stands out. Their attention to customer preferences and personalized recommendations made my vacation unforgettable. I'll definitely be using their services again."),
            ("The team at this travel agency went above and beyond to accommodate our last-minute changes. Their flexibility and professionalism were commendable. Our trip was fantastic, thanks to their efforts."),
            ("I cannot thank this travel agency enough for organizing such a fantastic tour. Every aspect was well-planned, and the tour guides were knowledgeable. It was a worry-free experience, and I enjoyed every moment."),
            ("Booking through this travel agency was a breeze. They offered competitive prices and a wide range of options. The communication was excellent, and they were quick to respond to any queries. Impressive service!"),
            ("My family and I had a wonderful vacation, all thanks to this travel agency. They suggested the perfect destinations based on our preferences, and the itinerary was well thought out. It was a truly memorable experience."),
            ("I had a fantastic solo trip organized by this agency. They catered to my specific requests and made sure I felt safe and comfortable throughout the journey. I'm grateful for their expertise and attention to detail."),
            ("The cruise package arranged by this travel agency exceeded my expectations. The onboard activities and excursions were well-organized. It was a luxurious experience, and I couldn't have asked for more."),
            ("The professionalism of this travel agency was impressive. They guided us through the entire process, providing valuable insights and recommendations. Our trip was flawless, and we're already planning our next one with them."),
            ("I had an amazing adventure trip, all thanks to the impeccable planning by this travel agency. The guides were knowledgeable, accommodations were top-notch, and the overall experience was simply incredible. Highly recommended for adventure seekers!"),
        ]
        
        # SQL query to insert data into the Review table
        insert_review_query = """
            INSERT INTO Review (
                CustomerID,
                TripID,
                GuideID,
                ReviewDate,
                Rating,
                ReviewComment
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # For each review, generate mock data for CustomerID, TripID, GuideID, ReviewDate, and Rating
        for review_text in reviews:
            customer_id = random.choice(customer_ids)  # Assuming customer_ids exist (IDs from Customer table)
            trip_id = random.choice(trip_ids)          # Assuming trip_ids exist (IDs from Trip table)
            guide_id = random.choice(guide_ids)        # Assuming guide_ids exist (IDs from Guide table)
            review_date = start_date + timedelta(weeks=2)               # Replace this with the actual review date
            rating = random.randint(3, 5)             # Assuming the rating is between 1 and 5
            review_comment = review_text
            # Execute the insert query for each review
            cursor.execute(insert_review_query, (customer_id, trip_id, guide_id, review_date, rating, review_comment))

        # Commit changes to the database
        mydb.commit()
        print("Reviews inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data into Review table: {err}")
    finally:
        # Close cursor and database connections
        cursor.close()

    try:
        cursor = mydb.cursor()

        # Fetching all IDs from respective tables
        cursor.execute("SELECT BookingID FROM Booking")
        booking_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT EquipmentID FROM Equipment")
        equipment_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT CustomerID FROM Customer")
        customer_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT PaymentID FROM Payment")
        payment_ids = [row[0] for row in cursor.fetchall()]

        customer_order_data = []
        for _ in range(200):
            # Generate mock data for BookingID, EquipmentID, PaymentID, CustomerID
            booking_id = random.choice(booking_ids)
            equipment_id = random.choice(equipment_ids)
            customer_id = random.choice(customer_ids)
            payment_id = random.choice(payment_ids)
            
            customer_order_data.append((booking_id, equipment_id, customer_id, payment_id))

        # SQL query to insert data into the Customer_Order table
        insert_customer_order_query = """
            INSERT INTO Customer_Order (
                BookingID,
                EquipmentID,
                CustomerID,
                PaymentID
            )
            VALUES (%s, %s, %s, %s)
        """

        try:
            # Execute the insert query for each customer order entry
            cursor.executemany(insert_customer_order_query, customer_order_data)
            print("Customer Order entries inserted successfully.")

            # Commit changes to the database
            mydb.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data into Customer_Order table: {err}")
            mydb.rollback()  # Rollback changes in case of an error
        finally:
            # Close cursor
            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

#Function that display's table data in a detailed and neat table form            
def display_table_data(mydb):
    try:
        cursor = mydb.cursor()
        # List of tables in your database
        tables = [
            "Location",
            "Guide",
            "Trip",
            "Customer",
            "Payment",
            "Booking",
            "Equipment",
            "Review",
            "Customer_Order"
        ]

        for table in tables:
            # Query to retrieve and display data from each table
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            result = cursor.fetchall()

            # Displaying data from each table
            print(f"\n{table} Table Data:")
            if len(result) > 0:
                # Fetching column names to display as headers
                column_names = [i[0] for i in cursor.description]
                
                # Using tabulate for better formatting and alignment
                table_data = [column_names] + list(result)
                print(tabulate(table_data, headers='firstrow', tablefmt='pretty'))
            else:
                print("No data available in the table.")

    except mysql.connector.Error as err:
        print(f"Error displaying table data: {err}")
    finally:
        if mydb.is_connected():
            cursor.close()



def main():
    mydb = connect_to_database()
    create_tables(mydb)
    insert_data(mydb)
    display_table_data(mydb)
    mydb.close()


if __name__ == "__main__":
    main()



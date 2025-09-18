import os
import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Text, Entry, Button, END, WORD
import argparse


def connect_server():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "travelbot"),
            password=os.environ.get("DB_PASSWORD", "password123"),
            charset=os.environ.get("DB_CHARSET", "utf8"),
        )
    except Error as err:
        print(f"Server connection error: {err}")
        return None


def ensure_database():
    server_conn = connect_server()
    if server_conn is None:
        return False
    try:
        cur = server_conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS TravelBot")
        server_conn.commit()
        return True
    except Error as err:
        print(f"Error creating database: {err}")
        return False
    finally:
        server_conn.close()


def connect_db():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "travelbot"),
            password=os.environ.get("DB_PASSWORD", "password123"),
            database=os.environ.get("DB_NAME", "TravelBot"),
            charset=os.environ.get("DB_CHARSET", "utf8"),
        )
    except Error as err:
        print(f"Database connection error: {err}")
        return None


def create_tables():
    conn = connect_db()
    if conn is None:
        return
    try:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Places (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(100),
                nearest_airport VARCHAR(255),
                distance_from_airport FLOAT,
                entry_fees FLOAT,
                age_restriction VARCHAR(50),
                specializations TEXT,
                type VARCHAR(100)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Hotels (
                place_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                nearest_airport VARCHAR(255) NOT NULL,
                cost DECIMAL(10, 2) NOT NULL,
                facilities TEXT,
                phone VARCHAR(20),
                rating DECIMAL(3, 2),
                PRIMARY KEY (place_id, name),
                FOREIGN KEY (place_id) REFERENCES Places(id)
            )
            """
        )

        conn.commit()
    except Error as err:
        print(f"Error creating tables: {err}")
    finally:
        conn.close()


def seed_sample_data(mode='short'):
    conn = connect_db()
    if conn is None:
        return
    try:
        cur = conn.cursor()

        if mode == 'short':
            places_data = [
                (
                    'Mysore Palace', 'Sightseeing', 'Kempegowda International Airport',
                    184, 70, 'None', 'Historical palace, architecture', 'Historical'
                ),
                (
                    'Coorg', 'Adventure', 'Mangalore International Airport',
                    160, 0, 'None', 'Trekking, Coffee Plantations', 'Natural Beauty'
                ),
                (
                    'Marina Beach', 'Sightseeing', 'Chennai International Airport',
                    16, 0, 'None', 'Beach, Sunrise', 'Beach'
                ),
            ]
        else:
            places_data = [
                ('Mysore Palace', 'Sightseeing', 'Kempegowda International Airport', 184, 70, 'None', 'Historical palace, architecture', 'Historical'),
                ('Coorg', 'Adventure', 'Mangalore International Airport', 160, 0, 'None', 'Trekking, Coffee Plantations', 'Natural Beauty'),
                ('Marina Beach', 'Sightseeing', 'Chennai International Airport', 16, 0, 'None', 'Beach, Sunrise', 'Beach'),
                ('Ramoji Film City', 'Entertainment', 'Rajiv Gandhi International Airport', 37, 1000, 'None', 'Film sets, Amusement park', 'Theme Park'),
                ('Meenakshi Temple', 'Sightseeing', 'Madurai International Airport', 10, 50, 'None', 'Temple, Architecture', 'Religious'),
                ('Ooty', 'Adventure', 'Coimbatore International Airport', 88, 0, 'None', 'HillStation, Tea Gardens', 'Natural Beauty'),
                ('Backwaters', 'Sightseeing', 'Cochin International Airport', 54, 0, 'None', 'Houseboats, Waterways', 'Natural Beauty'),
                ('Hampi', 'Sightseeing', 'Hubli Airport', 144, 40, 'None', 'Ancient Ruins, Temples', 'Historical'),
                ('Kanyakumari', 'Sightseeing', 'Trivandrum International Airport', 93, 10, 'None', 'Sunrise, Sunset', 'Natural Beauty'),
                ('Alleppey', 'Adventure', 'Cochin International Airport', 82, 0, 'None', 'Backwaters, Houseboats', 'Natural Beauty'),
                ('Munnar', 'Adventure', 'Cochin International Airport', 110, 0, 'None', 'TeaGardens, Trekking', 'Natural Beauty'),
                ('Rameswaram', 'Sightseeing', 'Madurai International Airport', 163, 50, 'None', 'Temple, Bridge', 'Religious'),
                ('Kabini', 'Adventure', 'Kempegowda International Airport', 214, 0, 'None', 'Wildlife Safari, River', 'Wildlife'),
                ('Mahabalipuram', 'Sightseeing', 'Chennai International Airport', 55, 40, 'None', 'Shore Temple, Architecture', 'Historical'),
                ('Varkala Beach', 'Sightseeing', 'Trivandrum International Airport', 42, 0, 'None', 'Beach, Cliff', 'Beach'),
                ('Periyar Wildlife Sanctuary', 'Adventure', 'Cochin International Airport', 190, 40, 'None', 'Wildlife Safari, Boating', 'Wildlife'),
                ('Kodaikanal', 'Adventure', 'Madurai International Airport', 120, 0, 'None', 'HillStation, Lake', 'Natural Beauty'),
                ('Chikmagalur', 'Adventure', 'Mangalore International Airport', 151, 0, 'None', 'Coffee Plantations, Trekking', 'Natural Beauty'),
                ('Pondicherry', 'Sightseeing', 'Chennai International Airport', 135, 0, 'None', 'French Colony, Beaches', 'Beach'),
                ('Bandipur National Park', 'Adventure', 'Kempegowda International Airport', 220, 300, '12+', 'Wildlife Safari, Tigers', 'Wildlife'),
                ('Gokarna', 'Adventure', 'Goa International Airport', 140, 0, 'None', 'Beaches, Temples', 'Beach'),
                ('Hogenakkal Falls', 'Sightseeing', 'Kempegowda International Airport', 180, 10, 'None', 'Waterfalls, Boating', 'Natural Beauty'),
                ('Yercaud', 'Adventure', 'Salem Airport', 38, 0, 'None', 'Hill Station, Lake', 'Natural Beauty'),
                ('Wayanad', 'Adventure', 'Calicut International Airport', 90, 0, 'None', 'Trekking, Waterfalls', 'Natural Beauty'),
                ('Nandi Hills', 'Sightseeing', 'Kempegowda International Airport', 42, 5, 'None', 'Sunrise, Hills', 'Natural Beauty'),
                ('Bekal Fort', 'Sightseeing', 'Mangalore International Airport', 60, 5, 'None', 'Fort, Beach', 'Historical'),
                ('Shivanasamudra Falls', 'Sightseeing', 'Kempegowda International Airport', 130, 5, 'None', 'Waterfalls, River', 'Natural Beauty'),
                ('Jog Falls', 'Sightseeing', 'Hubli Airport', 134, 10, 'None', 'Waterfalls, Scenic Views', 'Natural Beauty'),
                ('Madurai', 'Sightseeing', 'Madurai International Airport', 12, 0, 'None', 'Temples, Architecture', 'Religious'),
                ('Hassan', 'Adventure', 'Kempegowda International Airport', 182, 10, 'None', 'Temples, Trekking', 'Historical'),
                ('Chennai', 'Sightseeing', 'Chennai International Airport', 12, 0, 'None', 'CityLife, Beaches', 'Urban'),
                ('Belur and Halebidu', 'Sightseeing', 'Mangalore International Airport', 170, 20, 'None', 'Temples, Sculptures', 'Historical'),
                ('Coonoor', 'Adventure', 'Coimbatore International Airport', 70, 0, 'None', 'TeaGardens, Trekking', 'Natural Beauty'),
                ('Varkala', 'Sightseeing', 'Trivandrum International Airport', 44, 0, 'None', 'Beach, Temple', 'Beach'),
                ('Horsley Hills', 'Adventure', 'Bengaluru International Airport', 160, 0, 'None', 'HillStation, Trekking', 'Natural Beauty'),
                ('Pamban Bridge', 'Sightseeing', 'Madurai International Airport', 169, 0, 'None', 'Bridge, Scenic Views', 'Historical'),
                ('Trivandrum', 'Sightseeing', 'Trivandrum International Airport', 5, 0, 'None', 'Temples, Museums', 'Urban'),
                ('Kumarakom', 'Sightseeing', 'Cochin International Airport', 78, 0, 'None', 'Backwaters, Bird Sanctuary', 'Natural Beauty'),
                ('Kollam', 'Sightseeing', 'Trivandrum International Airport', 70, 0, 'None', 'Backwaters, Beaches', 'Natural Beauty'),
                ('Silent Valley National Park', 'Adventure', 'Coimbatore International Airport', 130, 50, 'None', 'Wildlife, Trekking', 'Wildlife'),
                ('Vellore Fort', 'Sightseeing', 'Chennai International Airport', 130, 5, 'None', 'Fort, Architecture', 'Historical'),
                ('Agumbe', 'Adventure', 'Mangalore International Airport', 96, 0, 'None', 'Rainforest, Trekking', 'Natural Beauty'),
                ('Yelagiri', 'Adventure', 'Bengaluru International Airport', 145, 0, 'None', 'HillStation, Adventure Sports', 'Natural Beauty'),
                ('Araku Valley', 'Adventure', 'Visakhapatnam Airport', 120, 10, 'None', 'Coffee Plantations, Trekking', 'Natural Beauty'),
                ('Srirangapatna', 'Sightseeing', 'Mysore Airport', 14, 5, 'None', 'Temples, River', 'Historical'),
                ('Kalpetta', 'Adventure', 'Calicut International Airport', 90, 0, 'None', 'Trekking, Waterfalls', 'Natural Beauty'),
                ('Chettinad', 'Sightseeing', 'Madurai International Airport', 90, 20, 'None', 'Mansions, Cuisine', 'Cultural'),
                ('Auroville', 'Sightseeing', 'Chennai International Airport', 140, 0, 'None', 'Community, Meditation', 'Cultural'),
                ('Bhadrachalam', 'Sightseeing', 'Rajahmundry Airport', 185, 10, 'None', 'Temple, River', 'Religious')
            ]

        cur.executemany(
            """
            INSERT INTO Places (name, category, nearest_airport, distance_from_airport,
            entry_fees, age_restriction, specializations, type)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            places_data,
        )

        conn.commit()

        # Map place names to IDs for hotel seeding
        cur.execute("SELECT id, name FROM Places")
        id_by_name = {name: pid for (pid, name) in cur.fetchall()}

        if mode == 'short':
            hotels_data = [
                (id_by_name.get('Mysore Palace', 1), 'Royal Orchid Metropole', 'Kempegowda International Airport', 120.00, 'Wi-Fi, Pool, Restaurant', '1234567890', 4.5),
                (id_by_name.get('Coorg', 2), 'Taj Madikeri Resort & Spa', 'Mangalore International Airport', 200.00, 'Wi-Fi, Spa, Restaurant', '0987654321', 4.7),
            ]
        else:
            hotels_data = [
                (id_by_name.get('Mysore Palace', 1), 'Royal Orchid Metropole', 'Kempegowda International Airport', 120.00, 'Wi-Fi, Pool, Restaurant', '1234567890', 4.5),
                (id_by_name.get('Coorg', 2), 'Taj Madikeri Resort & Spa', 'Mangalore International Airport', 200.00, 'Wi-Fi, Spa, Restaurant', '0987654321', 4.7),
                (id_by_name.get('Marina Beach', 3), 'Radisson Blu Resort', 'Chennai International Airport', 150.00, 'Beachfront, Pool, Gym', '1122334455', 4.6),
                (id_by_name.get('Ramoji Film City', 4), 'Dolphin Hotels', 'Rajiv Gandhi International Airport', 100.00, 'Wi-Fi, Parking, Gym', '5566778899', 4.3),
                (id_by_name.get('Meenakshi Temple', 5), 'The Gateway Hotel Pasumalai', 'Madurai International Airport', 80.00, 'Pool, Restaurant, Wi-Fi', '6677889900', 4.4),
                (id_by_name.get('Ooty', 6), 'Savoy Hotel', 'Coimbatore International Airport', 90.00, 'Tea Gardens, Restaurant, Wi-Fi', '7788990011', 4.2),
                (id_by_name.get('Backwaters', 7), 'Coconut Lagoon', 'Cochin International Airport', 175.00, 'Houseboats, Wi-Fi, Spa', '8899001122', 4.8),
                (id_by_name.get('Hampi', 8), 'Evolve Back', 'Hubli Airport', 250.00, 'Spa, Restaurant, Wi-Fi', '9900112233', 4.9),
                (id_by_name.get('Kanyakumari', 9), 'Sparsa Resort', 'Trivandrum International Airport', 110.00, 'Sunrise View, Pool, Restaurant', '1122445566', 4.5),
                (id_by_name.get('Alleppey', 10), 'Lake Palace Resort', 'Cochin International Airport', 180.00, 'Houseboats, Wi-Fi, Spa', '2233445566', 4.7),
                (id_by_name.get('Munnar', 11), 'SpiceTree Munnar', 'Cochin International Airport', 190.00, 'Tea Gardens, Spa, Wi-Fi', '3344556677', 4.6),
                (id_by_name.get('Rameswaram', 12), 'Daiwik Hotels', 'Madurai International Airport', 85.00, 'Temple View, Restaurant, Wi-Fi', '4455667788', 4.3),
                (id_by_name.get('Kabini', 13), 'Kabini River Lodge', 'Kempegowda International Airport', 95.00, 'Wildlife Safari, Wi-Fi', '5566778899', 4.7),
                (id_by_name.get('Mahabalipuram', 14), 'Radisson Blu Resort Temple Bay', 'Chennai International Airport', 140.00, 'Shore Temple View, Wi-Fi, Pool', '6677889900', 4.6),
                (id_by_name.get('Varkala Beach', 15), 'Varkala Marine Palace', 'Trivandrum International Airport', 60.00, 'Cliffside, Wi-Fi, Restaurant', '7788990011', 4.4),
                (id_by_name.get('Periyar Wildlife Sanctuary', 16), 'Spice Village', 'Cochin International Airport', 200.00, 'Wildlife Safari, Wi-Fi, Pool', '8899001122', 4.8),
                (id_by_name.get('Kodaikanal', 17), 'Kodai Resort Hotel', 'Madurai International Airport', 130.00, 'Hill Station, Wi-Fi, Restaurant', '9900112233', 4.5),
                (id_by_name.get('Chikmagalur', 18), 'The Serai Chikmagalur', 'Mangalore International Airport', 210.00, 'Coffee Plantations, Wi-Fi, Spa', '1122334455', 4.7),
                (id_by_name.get('Pondicherry', 19), 'Le Pondy Resort', 'Chennai International Airport', 180.00, 'Beachfront, Wi-Fi, Restaurant', '2233445566', 4.5),
                (id_by_name.get('Bandipur National Park', 20), 'The Windflower Resort & Spa', 'Kempegowda International Airport', 120.00, 'Wildlife Safari, Wi-Fi, Restaurant', '3344556677', 4.4),
                (id_by_name.get('Gokarna', 21), 'Namaste Café', 'Goa International Airport', 65.00, 'Beachfront, Wi-Fi, Restaurant', '4455667788', 4.3),
                (id_by_name.get('Hogenakkal Falls', 22), 'Hogenakkal Resort', 'Kempegowda International Airport', 75.00, 'Waterfall View, Wi-Fi, Restaurant', '5566778899', 4.2),
                (id_by_name.get('Yercaud', 23), 'Grand Palace Hotel & Spa', 'Salem Airport', 105.00, 'Hill Station, Wi-Fi, Restaurant', '6677889900', 4.5),
                (id_by_name.get('Wayanad', 24), 'Vythiri Resort', 'Calicut International Airport', 180.00, 'Trekking, Wi-Fi, Spa', '7788990011', 4.7),
                (id_by_name.get('Nandi Hills', 25), 'Mount Palazzo', 'Kempegowda International Airport', 90.00, 'Sunrise View, Wi-Fi, Restaurant', '8899001122', 4.4),
                (id_by_name.get('Bekal Fort', 26), 'Vivanta by Taj Bekal', 'Mangalore International Airport', 160.00, 'Beachfront, Wi-Fi, Restaurant', '9900112233', 4.6),
                (id_by_name.get('Shivanasamudra Falls', 27), 'Shivanasamudra Lodge', 'Kempegowda International Airport', 50.00, 'Waterfall View, Restaurant', '1122334455', 4.1),
                (id_by_name.get('Jog Falls', 28), 'Sharavathi Adventure Camp', 'Hubli Airport', 75.00, 'Waterfalls, Wi-Fi, Restaurant', '2233445566', 4.3),
                (id_by_name.get('Madurai', 29), 'Heritage Madurai', 'Madurai International Airport', 95.00, 'Temples, Wi-Fi, Restaurant', '3344556677', 4.6),
                (id_by_name.get('Hassan', 30), 'Hassan Ashok Hotel', 'Kempegowda International Airport', 85.00, 'Temples, Wi-Fi, Restaurant', '4455667788', 4.4),
                (id_by_name.get('Chennai', 31), 'Taj Connemara', 'Chennai International Airport', 160.00, 'City Life, Wi-Fi, Pool', '5566778899', 4.6),
                (id_by_name.get('Belur and Halebidu', 32), 'Hoysala Village Resort', 'Mangalore International Airport', 170.00, 'Temples, Wi-Fi, Spa', '6677889900', 4.7),
                (id_by_name.get('Coonoor', 33), 'Kurumba Village Resort', 'Coimbatore International Airport', 120.00, 'Tea Gardens, Wi-Fi, Restaurant', '7788990011', 4.6),
                (id_by_name.get('Varkala', 34), 'The Gateway Hotel Varkala', 'Trivandrum International Airport', 90.00, 'Beach, Wi-Fi, Restaurant', '8899001122', 4.5),
                (id_by_name.get('Horsley Hills', 35), 'Horsley Hills Haritha Resort', 'Bengaluru International Airport', 60.00, 'Hill Station, Wi-Fi, Restaurant', '9900112233', 4.2),
                (id_by_name.get('Pamban Bridge', 36), 'Sangam Hotel', 'Madurai International Airport', 80.00, 'Bridge View, Wi-Fi, Restaurant', '1122334455', 4.3),
                (id_by_name.get('Trivandrum', 37), 'Hilton Garden Inn', 'Trivandrum International Airport', 150.00, 'Temples, Wi-Fi, Restaurant', '2233445566', 4.6),
                (id_by_name.get('Kumarakom', 38), 'Kumarakom Lake Resort', 'Cochin International Airport', 250.00, 'Backwaters, Wi-Fi, Pool', '3344556677', 4.8),
                (id_by_name.get('Kollam', 39), 'The Raviz Ashtamudi', 'Trivandrum International Airport', 140.00, 'Backwaters, Wi-Fi, Spa', '4455667788', 4.7),
                (id_by_name.get('Silent Valley National Park', 40), 'Silent Valley Rainforest Retreat', 'Coimbatore International Airport', 190.00, 'Wildlife, Wi-Fi, Spa', '5566778899', 4.8),
                (id_by_name.get('Vellore Fort', 41), 'Vellore Hotel Saravana', 'Chennai International Airport', 60.00, 'Fort View, Wi-Fi, Restaurant', '6677889900', 4.2),
                (id_by_name.get('Agumbe', 42), 'Agumbe Rainforest Resort', 'Mangalore International Airport', 85.00, 'Rainforest, Wi-Fi, Trekking', '7788990011', 4.5),
                (id_by_name.get('Yelagiri', 43), 'Yelagiri Hills Resort', 'Bengaluru International Airport', 100.00, 'Hill Station, Wi-Fi, Restaurant', '8899001122', 4.3),
                (id_by_name.get('Araku Valley', 44), 'Araku Valley Resort', 'Visakhapatnam Airport', 95.00, 'Trekking, Wi-Fi, Restaurant', '9900112233', 4.6),
                (id_by_name.get('Srirangapatna', 45), 'Srirangapatna Lodge', 'Mysore Airport', 55.00, 'Temple View, Wi-Fi, Restaurant', '1122334455', 4.2),
                (id_by_name.get('Kalpetta', 46), 'Green Gates Hotel', 'Calicut International Airport', 80.00, 'Waterfalls, Wi-Fi, Restaurant', '2233445566', 4.4),
                (id_by_name.get('Chettinad', 47), 'Chettinad Mansion Heritage', 'Madurai International Airport', 120.00, 'Mansions, Wi-Fi, Restaurant', '3344556677', 4.5),
                (id_by_name.get('Auroville', 48), 'Auroville Guesthouse', 'Chennai International Airport', 50.00, 'Meditation, Wi-Fi, Restaurant', '4455667788', 4.1),
                (id_by_name.get('Bhadrachalam', 49), 'Hotel Bhadrachalam', 'Rajahmundry Airport', 70.00, 'Temple View, Wi-Fi, Restaurant', '5566778899', 4.2)
            ]

        cur.executemany(
            """
            INSERT INTO Hotels (place_id, name, nearest_airport, cost, facilities, phone, rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE phone = VALUES(phone), rating = VALUES(rating)
            """,
            hotels_data,
        )

        conn.commit()
    except Error as err:
        print(f"Error seeding data: {err}")
    finally:
        conn.close()


def fetch_places_by_type_or_place(user_choice):
    conn = connect_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        if user_choice == "place":
            cursor.execute("SELECT DISTINCT name FROM Places")
        elif user_choice == "type":
            cursor.execute("SELECT DISTINCT type FROM Places")
        else:
            return []
        results = cursor.fetchall()
        return [row[0] for row in results]
    except Error as err:
        print(f"Database query error: {err}")
        return []
    finally:
        conn.close()


def fetch_place_details(place_name):
    conn = connect_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT p.name AS place_name, p.nearest_airport, p.distance_from_airport, p.entry_fees,
                   p.age_restriction, p.specializations, p.type,
                   h.name, h.phone, h.rating
            FROM Places p
            LEFT JOIN Hotels h ON p.id = h.place_id
            WHERE p.name = %s
            """,
            (place_name,),
        )
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Database query error: {err}")
        return []
    finally:
        conn.close()


def build_gui():
    root = Tk()
    root.title("LACUNA")
    root.geometry("800x600")
    root.minsize(700, 500)

    # Use only default system colors and layout
    chat_frame = __import__("tkinter").Frame(root)
    chat_frame.pack(side="top", fill="both", expand=True, padx=12, pady=12)

    scrollbar = __import__("tkinter").Scrollbar(chat_frame)
    scrollbar.pack(side="right", fill="y")

    txt = Text(
        chat_frame,
        wrap=WORD,
        yscrollcommand=scrollbar.set,
        borderwidth=2,
        relief="groove",
        height=20
    )
    txt.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=txt.yview)

    # Bottom input area
    input_frame = __import__("tkinter").Frame(root)
    input_frame.pack(side="bottom", fill="x", padx=12, pady=(0, 12))

    e = Entry(
        input_frame,
        borderwidth=2,
        relief="groove",
        width=70
    )
    e.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=4)

    def send():
        user_input = e.get().strip()
        if not user_input:
            return
        txt.insert(END, "\nYou -> " + user_input)
        txt.see(END)
        user = user_input.lower()

        if user in ["hello", "hi", "hey"]:
            txt.insert(END, "\nBot -> Hey there! I'm Lacuna, your travel chatbot!")
            txt.insert(END, "\nWould you like to categorize by type or place?")
        elif user == "type":
            types = fetch_places_by_type_or_place("type")
            txt.insert(END, "\nBot -> Here are the types of attractions:")
            for t in types:
                txt.insert(END, f"\n\t- {t}")
        elif user == "place":
            places = fetch_places_by_type_or_place("place")
            txt.insert(END, "\nBot -> Here are the places you can visit:")
            for p in places:
                txt.insert(END, f"\n\t- {p}")
        else:
            place_details = fetch_place_details(user)
            if place_details:
                for details in place_details:
                    txt.insert(END, f"\nBot -> {details[0]}:")
                    txt.insert(END, f"\nNearest Airport: {details[1]} ({details[2]} km)")
                    txt.insert(END, f"\nEntry Fees: ₹{details[3]}")
                    txt.insert(END, f"\nAge Restriction: {details[4]}")
                    txt.insert(END, f"\nThings to do: {details[5]}")
                    txt.insert(END, f"\nReason for visit: {details[6]}")
                    txt.insert(END, f"\nNearby Hotel: {details[7]}, Phone: {details[8]}, Rating: {details[9]}/5")
                    txt.insert(END, f"\n---")
            else:
                txt.insert(END, "\nBot -> Sorry, I don't have information on that place.")
        e.delete(0, END)

    send_button = Button(input_frame, text="Send", command=send, borderwidth=2, relief="groove")
    send_button.pack(side="right", padx=(0, 0), pady=4)

    # Initial greeting and UX niceties
    txt.delete("1.0", END)
    txt.insert(END, "Bot -> Hey there! I'm Lacuna, your travel chatbot!\n")
    txt.insert(END, "Type 'hello' to begin, or say 'type' or 'place'.\n")

    # Placeholder behavior for the entry
    placeholder = "Type your message here..."
    e.insert(0, placeholder)

    def clear_placeholder(_event=None):
        if e.get() == placeholder:
            e.delete(0, END)

    def restore_placeholder(_event=None):
        if not e.get():
            e.insert(0, placeholder)

    e.bind("<FocusIn>", clear_placeholder)
    e.bind("<FocusOut>", restore_placeholder)

    e.focus_set()
    e.bind("<Return>", lambda _event: send())

    return root


def main(seed_mode):
    if not ensure_database():
        return
    create_tables()
    seed_sample_data(seed_mode)

    # Quick verification queries
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Places")
            places_count = cur.fetchone()[0]
            print(f"Places rows: {places_count}")
            cur.execute("SELECT COUNT(*) FROM Hotels")
            hotels_count = cur.fetchone()[0]
            print(f"Hotels rows: {hotels_count}")
        except Error as err:
            print(f"Verification error: {err}")
        finally:
            conn.close()

    root = build_gui()
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Travel Bot Database Seeding')
    parser.add_argument(
        '--seed',
        choices=['short', 'full'],
        default='short',
        help="Select seed data size: 'short' for minimal, 'full' for complete data"
    )
    args = parser.parse_args()

    main(args.seed)
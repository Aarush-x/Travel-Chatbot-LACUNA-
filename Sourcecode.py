import os
import mysql.connector
from mysql.connector import Error
from tkinter import Tk, Text, Entry, Button, END, WORD


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


def seed_sample_data():
    conn = connect_db()
    if conn is None:
        return
    try:
        cur = conn.cursor()

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

        cur.executemany(
            """
            INSERT INTO Places
            (name, category, nearest_airport, distance_from_airport, entry_fees, age_restriction, specializations, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name)
            """,
            places_data,
        )

        # Map place names to IDs for hotel seeding
        cur.execute("SELECT id, name FROM Places")
        id_by_name = {name: pid for (pid, name) in cur.fetchall()}

        hotels_data = [
            (
                id_by_name.get('Mysore Palace', 1), 'Royal Orchid Metropole', 'Kempegowda International Airport',
                120.00, 'Wi-Fi, Pool, Restaurant', '1234567890', 4.50
            ),
            (
                id_by_name.get('Coorg', 2), 'Taj Madikeri Resort & Spa', 'Mangalore International Airport',
                200.00, 'Wi-Fi, Spa, Restaurant', '0987654321', 4.70
            ),
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
            cursor.execute("SELECT DISTINCT name FROM places")
        elif user_choice == "type":
            cursor.execute("SELECT DISTINCT type FROM places")
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
    root.geometry("900x700")

    # Colors and fonts
    bg_gray = "#1f2937"  # entry/button background (dark slate)
    bg_color = "#111827"  # chat background (nearly black)
    text_color = "#e5e7eb"  # light gray text
    font = "Helvetica 14"
    font_bold = "Helvetica 13 bold"

    # Set overall background
    root.configure(bg=bg_color)

    # Chat area fills window
    txt = Text(
        root,
        bg=bg_color,
        fg=text_color,
        insertbackground=text_color,
        font=font,
        wrap=WORD,
        borderwidth=1,
        relief="solid"
    )
    txt.pack(side="top", fill="both", expand=True, padx=12, pady=12)

    # Bottom input area
    input_frame = __import__("tkinter").Frame(root, bg=bg_color)
    input_frame.pack(side="bottom", fill="x", padx=12, pady=(0, 12))

    e = Entry(
        input_frame,
        bg="#ffffff",
        fg="#111111",
        insertbackground="#111111",
        font=font,
        borderwidth=1,
        relief="solid"
    )
    e.pack(side="left", fill="x", expand=True)

    def send():
        user_input = e.get().strip()
        if not user_input:
            return
        txt.insert(END, "\nYou -> " + user_input)
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

    send_button = Button(input_frame, text="Send", font=font_bold, bg=bg_gray, fg=text_color, command=send)
    send_button.pack(side="left", padx=(8, 0))

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


def main():
    if not ensure_database():
        return
    create_tables()
    seed_sample_data()

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
    main()
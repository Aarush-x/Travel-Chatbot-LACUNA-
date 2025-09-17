import mysql.connector
from tkinter import Tk, Text, Entry, Button, END, WORD

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="TravelBot",
            charset="utf8"
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

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
    except mysql.connector.Error as err:
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
        cursor.execute("""
            SELECT p.name AS place_name, p.nearest_airport, p.distance_from_airport, p.entry_fees,
                   p.age_restriction, p.specializations, p.type,
                   h.name, h.phone, h.rating
            FROM Places p
            LEFT JOIN Hotels h ON p.id = h.place_id
            WHERE p.name = %s
        """, (place_name,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
        return []
    finally:
        conn.close()

def send():
    user_input = e.get().strip()
    if not user_input:
        return
    
    send_msg = "You -> " + user_input
    txt.insert(END, "\n" + send_msg)
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

def main():
    """Main function to initialize and run the GUI application."""
    print("Starting Lacuna Travel Chatbot...")
    root = Tk()
    root.title("Lacuna - Travel Chatbot")
    root.geometry("600x500")
    print("GUI window created successfully!")

    # Create text widget for chat display
    global txt, e
    txt = Text(root, width=70, height=20, wrap=WORD)
    txt.pack(pady=10)

    # Create entry widget for user input
    e = Entry(root, width=50)
    e.pack(pady=5)

    # Create send button
    send_button = Button(root, text="Send", command=send)
    send_button.pack(pady=5)

    # Bind Enter key to send function
    e.bind('<Return>', lambda event: send())

    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
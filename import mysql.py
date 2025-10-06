import mysql.connector
conn =mysql.connector.connect( host="localhost",
user="root",
password="root",
charset="utf8"
)
cursor = conn.cursor() #TRAVELBOT
CREATION
cursor.execute("CREATE DATABASE IF NOT EXISTS TravelBot")
cursor.execute("USE TravelBot")
cursor.execute("DROP TABLE Places")
result= cursor.fetchall()
for row in result:
 print(row)
#TABLE PLACES CREATION
cursor.execute("""
CREATE TABLE IF NOT EXISTS Places (
id INT AUTO_INCREMENT PRIMARY KEY, name
VARCHAR(255) NOT NULL,
category VARCHAR(100),
nearest_airport VARCHAR(255),
distance_from_airport FLOAT,
entry_fees FLOAT, age_restriction
VARCHAR(50), specializations
TEXT,
type VARCHAR(100)
)
""")
9
places_data = [
('Mysore Palace', 'Sightseeing', 'Kempegowda International Airport', 184, 70,
'None', 'Historical palace, architecture', 'Historical'),
('Coorg', 'Adventure', 'Mangalore International Airport', 160, 0, 'None',
'Trekking, Coffee Plantations', 'Natural Beauty'),
('Marina Beach', 'Sightseeing', 'Chennai International Airport', 16, 0,
'None', 'Beach, Sunrise', 'Beach'),
('Ramoji Film City', 'Entertainment', 'Rajiv Gandhi International Airport', 37,
1000, 'None', 'Film sets, Amusement park', 'Theme Park'),
('Meenakshi Temple', 'Sightseeing', 'Madurai International Airport', 10, 50,
'None', 'Temple, Architecture', 'Religious'),
('Ooty', 'Adventure', 'Coimbatore International Airport', 88, 0, 'None', 'HillStation, Tea Gardens', 'Natural Beauty'),
('Backwaters', 'Sightseeing', 'Cochin International Airport', 54, 0, 'None',
'Houseboats, Waterways', 'Natural Beauty'),
('Hampi', 'Sightseeing', 'Hubli Airport', 144, 40, 'None', 'Ancient Ruins,Temples', 'Historical'),
('Kanyakumari', 'Sightseeing', 'Trivandrum International Airport', 93, 10, 'None',
'Sunrise, Sunset', 'Natural Beauty'),
('Alleppey', 'Adventure', 'Cochin International Airport', 82, 0, 'None',
'Backwaters, Houseboats', 'Natural Beauty'),
('Munnar', 'Adventure', 'Cochin International Airport', 110, 0, 'None', 'TeaGardens, Trekking', 'Natural Beauty'),
('Rameswaram', 'Sightseeing', 'Madurai International Airport', 163, 50, 'None',
'Temple, Bridge', 'Religious'),
('Kabini', 'Adventure', 'Kempegowda International Airport', 214, 0, 'None',
'Wildlife Safari, River', 'Wildlife'),
('Mahabalipuram', 'Sightseeing', 'Chennai International Airport', 55, 40, 'None',
'Shore Temple, Architecture', 'Historical'),
('Varkala Beach', 'Sightseeing', 'Trivandrum International Airport', 42, 0, 'None',
'Beach, Cliff', 'Beach'),
('Periyar Wildlife Sanctuary', 'Adventure', 'Cochin International Airport', 190,
40, 'None', 'Wildlife Safari, Boating', 'Wildlife'),
('Kodaikanal', 'Adventure', 'Madurai International Airport', 120, 0, 'None', 'HillStation, Lake', 'Natural Beauty'),('Chikmagalur', 'Adventure', 'Mangalore International Airport', 151, 0, 'None',
'Coffee Plantations, Trekking', 'Natural Beauty'),
('Pondicherry', 'Sightseeing', 'Chennai International Airport', 135, 0, 'None',
'French Colony, Beaches', 'Beach'),
('Bandipur National Park', 'Adventure', 'Kempegowda InternationalAirport', 220, 300, '12+', 'Wildlife Safari, Tigers', 'Wildlife'),
('Gokarna', 'Adventure', 'Goa International Airport', 140, 0, 'None',
'Beaches, Temples', 'Beach'),
('Hogenakkal Falls', 'Sightseeing', 'Kempegowda International Airport',
180, 10, 'None', 'Waterfalls, Boating', 'Natural Beauty'),
('Yercaud', 'Adventure', 'Salem Airport', 38, 0, 'None', 'Hill Station, Lake',
'Natural Beauty'),
('Wayanad', 'Adventure', 'Calicut International Airport', 90, 0, 'None', 'Trekking,Waterfalls', 'Natural Beauty'),
('Nandi Hills', 'Sightseeing', 'Kempegowda International Airport', 42, 5, 'None',
'Sunrise, Hills', 'Natural Beauty'),
('Bekal Fort', 'Sightseeing', 'Mangalore International Airport', 60, 5, 'None',
'Fort, Beach', 'Historical'),
('Shivanasamudra Falls', 'Sightseeing', 'Kempegowda International Airport',
130, 5, 'None', 'Waterfalls, River', 'Natural Beauty'),
('Jog Falls', 'Sightseeing', 'Hubli Airport', 134, 10, 'None', 'Waterfalls,Scenic Views', 'Natural Beauty'),
('Madurai', 'Sightseeing', 'Madurai International Airport', 12, 0, 'None',
'Temples, Architecture', 'Religious'),
('Hassan', 'Adventure', 'Kempegowda International Airport', 182, 10,
'None', 'Temples, Trekking', 'Historical'),
('Chennai', 'Sightseeing', 'Chennai International Airport', 12, 0, 'None', 'CityLife, Beaches', 'Urban'),
('Belur and Halebidu', 'Sightseeing', 'Mangalore International Airport', 170, 20,
'None', 'Temples, Sculptures', 'Historical'),
('Coonoor', 'Adventure', 'Coimbatore International Airport', 70, 0, 'None', 'TeaGardens, Trekking', 'Natural Beauty'),
('Varkala', 'Sightseeing', 'Trivandrum International Airport', 44, 0, 'None',
'Beach, Temple', 'Beach'),
11
('Horsley Hills', 'Adventure', 'Bengaluru International Airport', 160, 0, 'None', 'HillStation, Trekking', 'Natural Beauty'),
('Pamban Bridge', 'Sightseeing', 'Madurai International Airport', 169, 0, 'None',
'Bridge, Scenic Views', 'Historical'),
('Trivandrum', 'Sightseeing', 'Trivandrum International Airport', 5, 0,
'None', 'Temples, Museums', 'Urban'),
('Kumarakom', 'Sightseeing', 'Cochin International Airport', 78, 0, 'None',
'Backwaters, Bird Sanctuary', 'Natural Beauty'),
('Kollam', 'Sightseeing', 'Trivandrum International Airport', 70, 0, 'None',
'Backwaters, Beaches', 'Natural Beauty'),
('Silent Valley National Park', 'Adventure', 'Coimbatore International Airport',
130, 50, 'None', 'Wildlife, Trekking', 'Wildlife'),
('Vellore Fort', 'Sightseeing', 'Chennai International Airport', 130, 5, 'None',
'Fort, Architecture', 'Historical'),
('Agumbe', 'Adventure', 'Mangalore International Airport', 96, 0, 'None',
'Rainforest, Trekking', 'Natural Beauty'),
('Yelagiri', 'Adventure', 'Bengaluru International Airport', 145, 0, 'None', 'HillStation, Adventure Sports', 'Natural Beauty'),
('Araku Valley', 'Adventure', 'Visakhapatnam Airport', 120, 10, 'None', 'CoffeePlantations, Trekking', 'Natural Beauty'),
('Srirangapatna', 'Sightseeing', 'Mysore Airport', 14, 5, 'None', 'Temples, River',
'Historical'),
('Kalpetta', 'Adventure', 'Calicut International Airport', 90, 0, 'None', 'Trekking,Waterfalls', 'Natural Beauty'),
('Chettinad', 'Sightseeing', 'Madurai International Airport', 90, 20, 'None',
'Mansions, Cuisine', 'Cultural'),
('Auroville', 'Sightseeing', 'Chennai International Airport', 140, 0, 'None',
'Community, Meditation', 'Cultural'),
('Bhadrachalam', 'Sightseeing', 'Rajahmundry Airport', 185, 10, 'None', 'Temple,River', 'Religious')
]
cursor.executemany("""
INSERT INTO Places (name, category, nearest_airport, distance_from_airport,
entry_fees, age_restriction, specializations, type)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", places_data)
conn.commit()
#TO CHK THE WORKING OF TABLE
cursor = conn.cursor()
cursor.execute("SELECT* FROM PLACES;")
table_description = cursor.fetchall()
for row in table_description:
 print(row)
cursor.close()
conn.close()
print("Database and table created, and data inserted successfully!")
#CREATION OF TABLE HOTEL
import mysql.connector
conn =mysql.connector.connect( host="localhost",
user="root",
password="root",
database="TravelBot",
charset="utf8"
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS hotels (
place_id INT NOT NULL,
13
name VARCHAR(255) NOT NULL,
nearest_airport VARCHAR(255) NOT NULL,
cost DECIMAL(10, 2) NOT NULL,
facilities TEXT,
phone VARCHAR(20),
rating DECIMAL(3, 2), PRIMARY
KEY (place_id, name)
)
""")
hotels_data = [
(1, 'Royal Orchid Metropole', 'Kempegowda International Airport', 120.00, 'Wi-Fi, Pool, Restaurant', '1234567890', 4.5),
(2, 'Taj Madikeri Resort & Spa', 'Mangalore International Airport', 200.00, 'Wi- Fi,Spa, Restaurant', '0987654321', 4.7),
(3, 'Radisson Blu Resort', 'Chennai International Airport', 150.00, 'Beachfront, Pool,Gym', '1122334455', 4.6),
(4, 'Dolphin Hotels', 'Rajiv Gandhi International Airport', 100.00, 'Wi-Fi, Parking,Gym', '5566778899', 4.3),
(5, 'The Gateway Hotel Pasumalai', 'Madurai International Airport', 80.00, 'Pool,Restaurant, Wi-Fi', '6677889900', 4.4),
(6, 'Savoy Hotel', 'Coimbatore International Airport', 90.00, 'Tea Gardens,Restaurant, Wi-Fi', '7788990011', 4.2),
(7, 'Coconut Lagoon', 'Cochin International Airport', 175.00, 'Houseboats, Wi- Fi,Spa', '8899001122', 4.8),
(8, 'Evolve Back', 'Hubli Airport', 250.00, 'Spa, Restaurant, Wi-Fi',
'9900112233', 4.9),
(9, 'Sparsa Resort', 'Trivandrum International Airport', 110.00, 'Sunrise View, Pool,Restaurant', '1122445566', 4.5),
(10, 'Lake Palace Resort', 'Cochin International Airport', 180.00, 'Houseboats, Wi-Fi, Spa', '2233445566', 4.7),
(11, 'SpiceTree Munnar', 'Cochin International Airport', 190.00, 'Tea Gardens, Spa,Wi-Fi', '3344556677', 4.6),(12, 'Daiwik Hotels', 'Madurai International Airport', 85.00, 'Temple View,Restaurant, Wi-Fi', '4455667788', 4.3),
(13, 'Kabini River Lodge', 'Kempegowda International Airport', 95.00, 'WildlifeSafari, Wi-Fi', '5566778899', 4.7),
(14, 'Radisson Blu Resort Temple Bay', 'Chennai International Airport', 140.00,
'Shore Temple View, Wi-Fi, Pool', '6677889900', 4.6),
(15, 'Varkala Marine Palace', 'Trivandrum International Airport', 60.00, 'Cliffside,Wi-Fi, Restaurant', '7788990011', 4.4),
(16, 'Spice Village', 'Cochin International Airport', 200.00, 'Wildlife Safari, Wi-Fi, Pool', '8899001122', 4.8),
(17, 'Kodai Resort Hotel', 'Madurai International Airport', 130.00, 'Hill Station, Wi-Fi, Restaurant', '9900112233', 4.5),
(18, 'The Serai Chikmagalur', 'Mangalore International Airport', 210.00, 'CoffeePlantations, Wi-Fi, Spa', '1122334455', 4.7),
(19, 'Le Pondy Resort', 'Chennai International Airport', 180.00, 'Beachfront, Wi-Fi, Restaurant', '2233445566', 4.5),
(20, 'The Windflower Resort & Spa', 'Kempegowda International Airport', 120.00,
'Wildlife Safari, Wi-Fi, Restaurant', '3344556677', 4.4),
(21, 'Namaste Café', 'Goa International Airport', 65.00, 'Beachfront, Wi-Fi,Restaurant', '4455667788', 4.3),
(22, 'Hogenakkal Resort', 'Kempegowda International Airport', 75.00, 'WaterfallView, Wi-Fi, Restaurant', '5566778899', 4.2),
(23, 'Grand Palace Hotel & Spa', 'Salem Airport', 105.00, 'Hill Station, Wi-Fi,Restaurant', '6677889900', 4.5),
(24, 'Vythiri Resort', 'Calicut International Airport', 180.00, 'Trekking, Wi-Fi, Spa',
'7788990011', 4.7),
(25, 'Mount Palazzo', 'Kempegowda International Airport', 90.00, 'Sunrise View,Wi-Fi, Restaurant', '8899001122', 4.4),
(26, 'Vivanta by Taj Bekal', 'Mangalore International Airport', 160.00, 'Beachfront,Wi-Fi, Restaurant', '9900112233', 4.6),
(27, 'Shivanasamudra Lodge', 'Kempegowda International Airport', 50.00, 'WaterfallView, Restaurant', '1122334455', 4.1),
(28, 'Sharavathi Adventure Camp', 'Hubli Airport', 75.00, 'Waterfalls, Wi-Fi,Restaurant', '2233445566', 4.3),
15
(29, 'Heritage Madurai', 'Madurai International Airport', 95.00, 'Temples, Wi- Fi,Restaurant', '3344556677', 4.6),
(30, 'Hassan Ashok Hotel', 'Kempegowda International Airport', 85.00,
'Temples, Wi-Fi, Restaurant', '4455667788', 4.4),
(31, 'Taj Connemara', 'Chennai International Airport', 160.00, 'City Life, Wi-Fi,Pool', '5566778899', 4.6),
(32, 'Hoysala Village Resort', 'Mangalore International Airport', 170.00, 'Temples,Wi-Fi, Spa', '6677889900', 4.7),
(33, 'Kurumba Village Resort', 'Coimbatore International Airport', 120.00, 'TeaGardens, Wi-Fi, Restaurant', '7788990011', 4.6),
(34, 'The Gateway Hotel Varkala', 'Trivandrum International Airport', 90.00, 'Beach,Wi-Fi, Restaurant', '8899001122', 4.5),
(35, 'Horsley Hills Haritha Resort', 'Bengaluru International Airport', 60.00, 'HillStation, Wi-Fi, Restaurant', '9900112233', 4.2),
(36, 'Sangam Hotel', 'Madurai International Airport', 80.00, 'Bridge View, Wi- Fi,Restaurant', '1122334455', 4.3),
(37, 'Hilton Garden Inn', 'Trivandrum International Airport', 150.00, 'Temples, Wi-Fi, Restaurant', '2233445566', 4.6),
(38, 'Kumarakom Lake Resort', 'Cochin International Airport', 250.00, 'Backwaters,Wi-Fi, Pool', '3344556677', 4.8),
(39, 'The Raviz Ashtamudi', 'Trivandrum International Airport', 140.00, 'Backwaters,Wi-Fi, Spa', '4455667788', 4.7),
(40, 'Silent Valley Rainforest Retreat', 'Coimbatore International Airport',
190.00, 'Wildlife, Wi-Fi, Spa', '5566778899', 4.8),
(41, 'Vellore Hotel Saravana', 'Chennai International Airport', 60.00, 'Fort View,Wi-Fi, Restaurant', '6677889900', 4.2),
(42, 'Agumbe Rainforest Resort', 'Mangalore International Airport', 85.00,
'Rainforest, Wi-Fi, Trekking', '7788990011', 4.5),
(43, 'Yelagiri Hills Resort', 'Bengaluru International Airport', 100.00, 'Hill Station,Wi-Fi, Restaurant', '8899001122', 4.3),
(44, 'Araku Valley Resort', 'Visakhapatnam Airport', 95.00, 'Trekking, Wi-Fi,Restaurant', '9900112233', 4.6),
(45, 'Srirangapatna Lodge', 'Mysore Airport', 55.00, 'Temple View, Wi-Fi,Restaurant', '1122334455', 4.2),
(46, 'Green Gates Hotel', 'Calicut International Airport', 80.00, 'Waterfalls, Wi- Fi,Restaurant', '2233445566', 4.4),
(47, 'Chettinad Mansion Heritage', 'Madurai International Airport', 120.00,
'Mansions, Wi-Fi, Restaurant', '3344556677', 4.5),
(48, 'Auroville Guesthouse', 'Chennai International Airport', 50.00, 'Meditation, Wi-Fi, Restaurant', '4455667788', 4.1),
(49, 'Hotel Bhadrachalam', 'Rajahmundry Airport', 70.00, 'Temple View, Wi-Fi,Restaurant', '5566778899', 4.2)
]
cursor.executemany("""
INSERT INTO hotels
(place_id,name,nearest_airport,cost,facilities,phone,rating) VALUES
(%s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
phone=VALUES(phone), rating=VALUES(rating) """,
hotels_data)
conn.commit()
#TO CHK THE COUNT ADN WORKING OF TABLE
cursor = conn.cursor() 
cursor.execute("SELECT *FROM HOTELS;")
table_description = cursor.fetchall()
for row in table_description:
 print(row)
cursor.close()
conn.close()
print("Database and table created, and data inserted successfully!")
#TKINTERGUI FOR LACUNA
17
import mysql.connector
from tkinter import *
import webbrowser
def connect_db():
 return
mysql.connector.connect( host=
"localhost", user="root",
password="root",
database="TravelBot",
charset="utf8"
)
def fetch_places_by_type_or_place(user_choice):
 conn = connect_db()
 cursor = conn.cursor()
 if user_choice == "place":
  cursor.execute("SELECT DISTINCT name FROM places")
 elif user_choice == "type":
  cursor.execute("SELECT DISTINCT type FROM places")
  results = cursor.fetchall()
 conn.close()
 return [row[0] for row in results]
def fetch_place_details(place_name):
 conn = connect_db()
 cursor = conn.cursor()
 cursor.execute("""
 p.entry_fees,
 SELECT p.name AS place_name, p.nearest_airport, p.distance_from_airport,
 p.age_restriction, p.specializations, p.type,h.name, h.phone, h.rating FROM
 Places p
 LEFT JOIN Hotels h ON p.id = h.place_id
 WHERE p.name = %s
 """, (place_name,))
result = cursor.fetchall()
conn.close()
return result
# Tkinter GUI Setup root
= Tk()
root.title("LACUNA")
root.geometry("2000x1800")
BG_GRAY = "#2c2c2c" 
BG_COLOR= "#003366" 
TEXT_COLOR ="#c0c0c0"
FONT = "Helvetica 14" 
FONT_BOLD= "Helvetica 13 bold"
# Send function
def send():
    send = "You -> " + e.get()
    txt.insert(END, "\n" + send)
    user = e.get().lower()
    if user in ["hello", "hi", "hey"]:
        txt.insert(END, "\nBot -> Hey there! I'm Lacuna, your travel chatbot!")
        txt.insert(END, "\nWould you like to categorize by type or place?")
    elif user == "type":
        types = fetch_places_by_type_or_place("type") 
        txt.insert(END,"\nBot -> Here are the types of attractions:")
        for t in types:
            txt.insert(END, f"\n\t- {t}")
    elif user == "place":
        places = fetch_places_by_type_or_place("place")
        txt.insert(END,"\nBot -> Here are the places you can visit:")
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

# GUI Elements
txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT,
wrap=WORD, width=138, height=33)
txt.grid(row=0, column=0, columnspan=2)
e = Entry(root, bg="#2c2c2c", fg="#c0c0c0", font=FONT, width=132)
e.grid(row=1, column=0)

send_button = Button(root, text="Send", font=FONT_BOLD,
bg="#2c2c2c",fg="#c0c0c0",command=send)
send_button.grid(row=1, column=1)

root.mainloop()
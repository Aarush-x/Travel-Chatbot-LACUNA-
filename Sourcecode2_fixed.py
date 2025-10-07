"""Travel Chatbot - Sourcecode2_fixed.py

Clean, single-file implementation. Use this file to run the app while I avoid editing the corrupted original.
"""

import os
import argparse
from collections import defaultdict

try:
    import mysql.connector
    from mysql.connector import Error
except Exception:
    mysql = None
    Error = Exception

try:
    from tkinter import Tk, Text, Entry, Button, END, WORD, Frame, Scrollbar
except Exception:
    Tk = None


def get_cursor(conn, buffered=True):
    """Return a buffered cursor when possible to avoid "Unread result found".

    Some mysql drivers require buffered cursors if you plan to run another
    query on the same connection before consuming previous results. This
    helper attempts to create a buffered cursor and falls back gracefully.
    """
    try:
        return conn.cursor(buffered=buffered)
    except TypeError:
        # older cursors or alternate drivers may not accept buffered kwarg
        return conn.cursor()


def connect_server():
    if mysql is None:
        return None
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "travelbot"),
            password=os.environ.get("DB_PASSWORD", "password123"),
        )
    except Error as err:
        print("Server connection error:", err)
        return None


def ensure_database():
    srv = connect_server()
    if srv is None:
        return False
    try:
        cur = get_cursor(srv)
        cur.execute("CREATE DATABASE IF NOT EXISTS TravelBot")
        srv.commit()
        return True
    except Error as err:
        print("Error ensuring database:", err)
        return False
    finally:
        try:
            cur.close()
        except Exception:
            pass
        srv.close()


def connect_db():
    if mysql is None:
        return None
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "travelbot"),
            password=os.environ.get("DB_PASSWORD", "password123"),
            database=os.environ.get("DB_NAME", "TravelBot"),
        )
    except Error as err:
        print("Database connect error:", err)
        return None


def create_tables():
    conn = connect_db()
    if conn is None:
        return
    cur = get_cursor(conn)
    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Places (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                type VARCHAR(100),
                nearest_airport VARCHAR(255),
                distance_from_airport FLOAT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Hotels (
                place_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                cost DECIMAL(10,2),
                facilities TEXT,
                rating DECIMAL(3,2),
                PRIMARY KEY (place_id, name),
                FOREIGN KEY (place_id) REFERENCES Places(id)
            )
            """
        )
        conn.commit()
    except Error as err:
        print("Create tables error:", err)
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def seed_sample_data(mode="short"):
    conn = connect_db()
    if conn is None:
        return
    cur = get_cursor(conn)
    try:
        if mode == "short":
            places = [
                ("Mysore Palace", "historical", "Kempegowda International Airport", 184),
                ("Coorg", "natural beauty", "Mangalore International Airport", 160),
            ]
            hotels = [
                ("Mysore Palace", "Royal Orchid Metropole", 120.0, "Wi-Fi, Pool", 4.5),
                ("Coorg", "Taj Madikeri Resort & Spa", 200.0, "Spa, Restaurant", 4.7),
            ]
        else:
            places = [
                ("Mysore Palace", "historical", "Kempegowda International Airport", 184),
                ("Coorg", "natural beauty", "Mangalore International Airport", 160),
                ("Marina Beach", "beach", "Chennai International Airport", 16),
            ]
            hotels = [
                ("Mysore Palace", "Royal Orchid Metropole", 120.0, "Wi-Fi, Pool", 4.5),
                ("Coorg", "Taj Madikeri Resort & Spa", 200.0, "Spa, Restaurant", 4.7),
                ("Marina Beach", "Radisson Blu Resort", 150.0, "Beachfront", 4.6),
            ]

        id_by_name = {}
        # Insert or find places safely (avoid duplicates by name)
        for name, ptype, airport, dist in places:
            cur.execute("SELECT id FROM Places WHERE name = %s", (name,))
            # consume result immediately
            row = cur.fetchone()
            if row:
                pid = row[0]
            else:
                cur.execute(
                    "INSERT INTO Places (name, type, nearest_airport, distance_from_airport) VALUES (%s,%s,%s,%s)",
                    (name, ptype, airport, dist),
                )
                conn.commit()
                pid = cur.lastrowid
            id_by_name[name] = pid

        # Insert hotels only when they don't already exist for that place
        for place_name, hname, cost, facs, rating in [(h[0], h[1], h[2], h[3], h[4]) for h in hotels]:
            pid = id_by_name.get(place_name)
            if pid is None:
                continue
            cur.execute("SELECT 1 FROM Hotels WHERE place_id = %s AND name = %s", (pid, hname))
            exists = cur.fetchone()
            if exists:
                continue
            cur.execute(
                "INSERT INTO Hotels (place_id, name, cost, facilities, rating) VALUES (%s,%s,%s,%s,%s)",
                (pid, hname, cost, facs, rating),
            )
        conn.commit()
    except Error as err:
        print("Seeding error:", err)
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def fetch_places_by_type_or_place(kind):
    conn = connect_db()
    if conn is None:
        return []
    cur = get_cursor(conn)
    try:
        if kind == "place":
            cur.execute("SELECT DISTINCT name FROM Places ORDER BY name")
        elif kind == "type":
            cur.execute("SELECT DISTINCT type FROM Places ORDER BY type")
        else:
            return []
        rows = cur.fetchall()
        return [r[0] for r in rows]
    except Error as err:
        print("Query error:", err)
        return []
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def fetch_place_details(place_name):
    conn = connect_db()
    if conn is None:
        return None
    cur = get_cursor(conn)
    try:
        cur.execute(
            """
            SELECT p.id, p.name, p.type, p.nearest_airport, p.distance_from_airport,
                   h.name, h.cost, h.facilities, h.rating
            FROM Places p
            LEFT JOIN Hotels h ON p.id = h.place_id
            WHERE LOWER(p.name) = %s
            """,
            (place_name.lower(),),
        )
        rows = cur.fetchall()
        if not rows:
            return None
        place = None
        hotels = []
        seen_hotels = set()
        for row in rows:
            pid, pname, ptype, airport, dist, hname, hcost, hfac, hrating = row
            if place is None:
                place = {"id": pid, "name": pname, "type": ptype, "nearest_airport": airport, "distance": dist}
            if hname and hname not in seen_hotels:
                seen_hotels.add(hname)
                hotels.append({"name": hname, "cost": hcost, "facilities": hfac, "rating": hrating})
        return {"place": place, "hotels": hotels}
    except Error as err:
        print("Query error:", err)
        return None
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def fetch_places_by_type(type_name):
    conn = connect_db()
    if conn is None:
        return {}
    cur = get_cursor(conn)
    try:
        cur.execute(
            """
            SELECT p.id, p.name, p.type, p.nearest_airport, p.distance_from_airport,
                   h.name, h.cost, h.facilities, h.rating
            FROM Places p
            LEFT JOIN Hotels h ON p.id = h.place_id
            WHERE LOWER(p.type) = %s
            ORDER BY p.name
            """,
            (type_name.lower(),),
        )
        rows = cur.fetchall()
        if not rows:
            return {}
        by_place = defaultdict(lambda: {"place": None, "hotels": []})
        # track seen hotel names per place to avoid duplicates coming from JOIN
        seen_hotels = defaultdict(set)
        for row in rows:
            pid, pname, ptype, airport, dist, hname, hcost, hfac, hrating = row
            if by_place[pname]["place"] is None:
                by_place[pname]["place"] = {"id": pid, "name": pname, "type": ptype, "nearest_airport": airport, "distance": dist}
            if hname:
                if hname not in seen_hotels[pname]:
                    seen_hotels[pname].add(hname)
                    by_place[pname]["hotels"].append({"name": hname, "cost": hcost, "facilities": hfac, "rating": hrating})
        return dict(by_place)
    except Error as err:
        print("Query error:", err)
        return {}
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def build_gui():
    if Tk is None:
        print("Tkinter not available")
        return None
    root = Tk()
    root.title("LACUNA")
    root.geometry("800x600")

    chat = Frame(root)
    chat.pack(fill="both", expand=True, padx=8, pady=8)
    sb = Scrollbar(chat)
    sb.pack(side="right", fill="y")
    txt = Text(chat, wrap=WORD, yscrollcommand=sb.set)
    txt.pack(fill="both", expand=True)
    sb.config(command=txt.yview)

    inp = Frame(root)
    inp.pack(fill="x", padx=8, pady=6)
    e = Entry(inp, width=70)
    e.pack(side="left", fill="x", expand=True, padx=(0, 8))

    placeholder = "Type 'hello' or ask for a type/place"
    e.insert(0, placeholder)
    def send(_event=None):
        user = e.get().strip()
        if not user or user == placeholder:
            return
        txt.insert(END, "\nYou -> " + user)
        txt.see(END)
        low = user.lower()
        if low in ("hello", "hi", "hey"):
            txt.insert(END, "\nBot -> Hi! Type 'type' or 'place' to list options.")
            return
        if low == "type":
            types = fetch_places_by_type_or_place("type")
            txt.insert(END, "\nBot -> Types:")
            for t in types:
                txt.insert(END, "\n  - " + t)
            return
        if low == "place":
            places = fetch_places_by_type_or_place("place")
            txt.insert(END, "\nBot -> Places:")
            for p in places:
                txt.insert(END, "\n  - " + p)
            return

        types = fetch_places_by_type_or_place("type")
        if low in [t.lower() for t in types]:
            results = fetch_places_by_type(low)
            txt.insert(END, f"\nBot -> Places for type '{low}':")
            for pname, pdata in results.items():
                p = pdata["place"]
                txt.insert(END, f"\n\n{p['name']} — Nearest airport: {p.get('nearest_airport')} | Distance: {p.get('distance')}")
                if pdata["hotels"]:
                    txt.insert(END, "\n  Hotels:")
                    for h in pdata["hotels"]:
                        txt.insert(END, f"\n    - {h['name']} | Rating: {h.get('rating')} | Cost: {h.get('cost')}")
                else:
                    txt.insert(END, "\n  No hotels")
            return

        res = fetch_place_details(user)
        if not res:
            txt.insert(END, "\nBot -> I couldn't find that place or type. Try 'type' or 'place'.")
        else:
            p = res["place"]
            txt.insert(END, f"\nBot -> {p['name']} (type: {p.get('type')})")
            if res["hotels"]:
                txt.insert(END, "\n  Hotels:")
                for h in res["hotels"]:
                    txt.insert(END, f"\n    - {h['name']} | Rating: {h.get('rating')} | Cost: {h.get('cost')}")
            else:
                txt.insert(END, "\n  No hotels")

        # clear the input entry after sending so user doesn't need to delete it manually
        try:
            e.delete(0, END)
            e.focus_set()
        except Exception:
            pass

    # UX: placeholder should disappear when the user focuses the entry and
    # reappear only when the entry loses focus and is empty.
    def on_focus_in(_event=None):
        try:
            if e.get() == placeholder:
                e.delete(0, END)
        except Exception:
            pass

    def on_focus_out(_event=None):
        try:
            if not e.get().strip():
                e.insert(0, placeholder)
        except Exception:
            pass

    e.bind("<FocusIn>", on_focus_in)
    e.bind("<FocusOut>", on_focus_out)

    btn = Button(inp, text="Send", command=send)
    btn.pack(side="right")
    e.bind("<Return>", send)

    return root


def main():
    if not ensure_database():
        print("Cannot create/verify DB; ensure MySQL is running and credentials are set in env vars")
        return
    create_tables()
    # Always seed the full dataset; user no longer chooses short/full
    seed_sample_data('full')
    root = build_gui()
    if root:
        root.mainloop()


if __name__ == "__main__":
    main()
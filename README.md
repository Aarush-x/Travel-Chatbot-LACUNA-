# Travel Chatbot - LACUNA

Lacuna is a smart, interactive chatbot designed to assist travelers exploring the vibrant and culturally rich South India region. By consolidating multiple travel-related queries into one comprehensive platform, Lacuna simplifies trip planning and enhances the travel experience for both domestic and international visitors.

Whether it’s finding the nearest hotel, understanding entry fees for tourist spots, or checking age restrictions at attractions, Lacuna delivers quick, accurate, and reliable information.

---

## Key Features

- **Hotel Information:**
	- Provides detailed information about hotels near your current or desired location.
	- Suggests hotels based on user preferences such as budget, amenities, and proximity to tourist destinations.
	- Offers contact details and reviews.

- **Airport Guidance:**
	- Access information about nearby airports for smooth travel transitions, especially for tourists unfamiliar with the region.

- **Tourist Spot Assistance:**
	- Details about popular tourist destinations, including operating hours, age restrictions, and entry fees.
	- Simplifies finding rules and guidelines for historical monuments, temples, wildlife sanctuaries, and museums.

- **Travel Convenience:**
	- Consolidates a wide range of queries into one platform, eliminating the need to browse multiple websites or apps.
	- Integrates real-time information for ease of use, from transportation services to weather updates.

- **User-Friendly Interaction:**
	- Intuitive and responsive design.
	- Engages in natural conversations, providing relevant information in seconds.

---

## Impact

Lacuna aims to revolutionize travel in South India by offering a seamless and hassle-free experience. By addressing common concerns like accommodation, transport, and attraction details, the chatbot serves as a one-stop solution for travelers, reducing the complexity of trip planning and enabling visitors to enjoy their journey to the fullest.

---

## Main Functions Used

### `connect_db()`
Establishes a connection between the Python program and the MySQL database using the MySQL connector. This connection is essential for performing database operations like querying and updating data. Returns the database connection object for use in other parts of the code.

### `fetch_places_by_type_or_place(user_choice)`
Handles the user's initial input, asking whether they want to explore tourist places by a specific "type" (e.g., beaches, temples) or by a specific "place" (city or region). Retrieves a list of places or types from the database based on the user's choice.

### `fetch_place_details(place_name)`
Retrieves detailed information about a specific tourist destination. Queries the database to gather data about the place, including details like nearest hotels, entry fees, restrictions, and other travel-related information. Returns comprehensive information from both the 'Places' table and any connected tables.

### `send()`
Manages the flow of conversation between the user and the chatbot in the Tkinter GUI. Reads user input, matches it with predefined patterns or responses, and generates appropriate replies. Calls other functions such as `fetch_places_by_type_or_place()` or `fetch_place_details()` to retrieve and display data, ensuring smooth communication and guiding the user through the decision-making process.

## Setup & Run (macOS)

Use these steps to set up a local development environment on macOS and run the project. These commands assume you have Python 3 installed (Homebrew or python.org builds are fine).

1) Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

2) Upgrade pip and install the MySQL connector

```bash
pip install --upgrade pip
pip install mysql-connector-python
```

3) (Optional) If you need to install Tk support on macOS:

- If your Python was installed from python.org it includes Tk. If not, install ActiveTcl or use the official Python installer.

4) Set environment variables for DB access (temporary for this shell):

```bash
export DB_HOST=localhost
export DB_USER=travelbot
export DB_PASSWORD=yourpassword
export DB_NAME=TravelBot
```

5) Seed the database and run the GUI (app now always seeds full dataset automatically):

```bash
python3 Sourcecode2.py
```

Notes
- The repository contains `Sourcecode2_fixed.py` (full, validated implementation). `Sourcecode2.py` is a small runner that delegates to the fixed file to avoid accidental file corruption.
- Seeding is idempotent: running `--seed short` multiple times will not create duplicate rows when the connector and DB are configured correctly.
- If you see `Cannot create/verify DB` make sure `mysql-connector-python` is installed in the active Python environment and env vars are set.

Troubleshooting
- If you get `ModuleNotFoundError: No module named 'mysql'` activate the virtualenv and install `mysql-connector-python` inside it.
- If you get `Unread result found` during seeding, ensure you run the project using the provided venv Python (the code was updated to use buffered cursors to address this). If the error persists, let me know and I can add a DB-cleanup tool.

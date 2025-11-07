
## 🎵 Step 1: Folder Structure

Make sure your project folder looks like this:

```
music_store_project/
│
├── app.py
├── db.py
├── requirements.txt
├── data.sql
│
├── templates/
│   ├── index.html
│   ├── customers.html
│   ├── artists.html
│   ├── albums.html
│   ├── tracks.html
│   ├── orders.html
│   ├── new_order.html
│   ├── invoice.html
│   └── reports.html
│
└── static/
    └── style.css
```

---

## ⚙️ Step 2: Create and Activate a Virtual Environment

### 🪟 On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 🐧 On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Step 3: Install Dependencies

Once the environment is active, run:

```bash
pip install -r requirements.txt
```

This installs Flask, PyMySQL, and other required libraries.

---

## 🗄️ Step 4: Setup MySQL Database

### 1️⃣ Open MySQL command prompt or MySQL Workbench

Create the database:

```sql
CREATE DATABASE music_store;
```

### 2️⃣ Select it:

```sql
USE music_store;
```

### 3️⃣ Run your SQL file (to create tables and insert data):

If using MySQL Workbench:

* Open `data.sql`
* Run it.

If using command prompt:

```bash
mysql -u root -p music_store < data.sql
```

---

## 🧱 Step 5: Configure `db.py`

Make sure your `db.py` file looks like this:

```python
import pymysql

def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1234',   # change this if your MySQL password is different
        database='music_store',
        cursorclass=pymysql.cursors.DictCursor
    )
```

✅ Replace `'1234'` with your actual MySQL root password.

---

## 🚀 Step 6: Run the Flask App

In your terminal (inside the project folder):

```bash
python app.py
```

If everything is correct, you’ll see:

```
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Step 7: Open in Browser

Go to your web browser and open:

```
http://127.0.0.1:5000/
```

You’ll see your **Music Store Management System** home page.

From there, you can:

* Manage customers
* Add artists, albums, and tracks
* Create and delete orders
* Generate reports
* View invoices

---

## 🧩 Step 8: (Optional) Add Environment Variables

Instead of hardcoding the database password, create a `.env` file:

```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=0000
DB_NAME=music_store
```

Then update `db.py`:

```python
import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )
```
Would you like me to generate a **readme.txt** file with all these setup instructions (so you can include it in your project submission)?

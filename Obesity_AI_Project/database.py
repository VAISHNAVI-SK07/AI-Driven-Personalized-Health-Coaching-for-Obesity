import sqlite3

def create_db():
    # This creates a file named 'health_data.db'
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    # Create a table to store daily progress
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                 (date TEXT, weight REAL, bmi REAL, exercise INTEGER)''')
    conn.commit()
    conn.close()

def save_entry(date, weight, bmi, exercise):
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (date, weight, bmi, exercise))
    conn.commit()
    conn.close()

# Run this once to setup
if __name__ == "__main__":
    create_db()
    print("Database created successfully!")
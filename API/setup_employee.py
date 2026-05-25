import psycopg2
import bcrypt
import sys

DB_PARAMS = {
    "dbname": "coffeeshop",
    "user": "postgres",
    "password": "parola",
    "host": "localhost",
    "port": "5432"
}


def seed_employee():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE email = 'employee@gmail.com'")

        password = "Parola123!"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            ('Employee', 'employee@gmail.com', hashed_password, 'employee')
        )

        conn.commit()
        print("Employee account seeded successfully.")

    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
        print("Database error:", e)
        sys.exit(1)
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()


if __name__ == "__main__":
    seed_employee()
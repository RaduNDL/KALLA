import psycopg2
import bcrypt

def create_employee_account():
    conn = psycopg2.connect(
        dbname="coffeeshop",
        user="postgres",
        password="parola",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    password = "Parola123!"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, 'employee')",
        ('Employee', 'employee@gmail.com', hashed_password)
    )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_employee_account()
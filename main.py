import psycopg2
from datetime import datetime


DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "pet_adoption",
    "user": "postgres",
    "password": "postgres123",
    "port": 5432
}


def get_connection():
    try:
        return psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def print_separator():
    print("\n" + "=" * 60)


def safe_int_input(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def safe_status_input(prompt):
    valid_statuses = {"Pending", "Approved", "Rejected", "Withdrawn"}
    while True:
        value = input(prompt).strip().capitalize()
        if value in valid_statuses:
            return value
        print("Invalid status. Use: Pending, Approved, Rejected, or Withdrawn.")


def print_rows(rows, headers):
    if not rows:
        print("No records found.")
        return

    print_separator()
    print(" | ".join(headers))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(item) if item is not None else "NULL" for item in row))
    print_separator()


# ================================
# FIXED FUNCTIONS
# ================================

def view_all_pets():
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT pet_id, name, species, age, available
            FROM Pet
            ORDER BY pet_id;
        """)

        rows = cur.fetchall()
        print_rows(rows, ["pet_id", "name", "species", "age", "available"])

    except Exception as e:
        print(f"Error viewing pets: {e}")
    finally:
        cur.close()
        conn.close()


def view_available_pets():
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT pet_id, name, species, age, available
            FROM Pet
            WHERE available = TRUE
            ORDER BY pet_id;
        """)

        rows = cur.fetchall()
        print_rows(rows, ["pet_id", "name", "species", "age", "available"])

    except Exception as e:
        print(f"Error viewing available pets: {e}")
    finally:
        cur.close()
        conn.close()


def count_applications_per_pet():
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT Pet.pet_id, Pet.name, COUNT(AdoptionApplication.application_id) AS application_count
            FROM Pet
            LEFT JOIN AdoptionApplication
            ON Pet.pet_id = AdoptionApplication.pet_id
            GROUP BY Pet.pet_id, Pet.name
            ORDER BY Pet.pet_id;
        """)

        rows = cur.fetchall()
        print_rows(rows, ["pet_id", "name", "application_count"])

    except Exception as e:
        print(f"Error counting applications per pet: {e}")
    finally:
        cur.close()
        conn.close()


def view_approved_applications():
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT application_id, user_id, pet_id, status, submitted_at, notes
            FROM AdoptionApplication
            WHERE status = 'Approved'
            ORDER BY application_id;
        """)

        rows = cur.fetchall()
        print_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])

    except Exception as e:
        print(f"Error viewing approved applications: {e}")
    finally:
        cur.close()
        conn.close()


# ================================
# ORIGINAL FUNCTIONS
# ================================

def submit_application():
    conn = get_connection()
    if conn is None:
        return

    try:
        user_id = safe_int_input("Enter user_id: ")
        pet_id = safe_int_input("Enter pet_id: ")
        notes = input("Enter notes (optional): ").strip() or None

        cur = conn.cursor()

        cur.execute("SELECT 1 FROM UserTable WHERE user_id = %s;", (user_id,))
        if not cur.fetchone():
            print("Error: user_id does not exist.")
            return

        cur.execute("SELECT available FROM Pet WHERE pet_id = %s;", (pet_id,))
        pet = cur.fetchone()

        if not pet:
            print("Error: pet_id does not exist.")
            return

        if pet[0] is False:
            print("This pet is not currently available.")
            return

        cur.execute("""
            INSERT INTO AdoptionApplication (user_id, pet_id, status, submitted_at, notes)
            VALUES (%s, %s, %s, %s, %s);
        """, (user_id, pet_id, "Pending", datetime.now(), notes))

        conn.commit()
        print("Application submitted successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Error submitting application: {e}")
    finally:
        cur.close()
        conn.close()


def view_all_applications():
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT application_id, user_id, pet_id, status, submitted_at, notes
            FROM AdoptionApplication
            ORDER BY application_id;
        """)

        rows = cur.fetchall()
        print_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])

    except Exception as e:
        print(f"Error viewing applications: {e}")
    finally:
        cur.close()
        conn.close()


def view_applications_by_pet():
    conn = get_connection()
    if conn is None:
        return

    try:
        pet_id = safe_int_input("Enter pet_id: ")
        cur = conn.cursor()

        cur.execute("""
            SELECT application_id, user_id, pet_id, status, submitted_at, notes
            FROM AdoptionApplication
            WHERE pet_id = %s
            ORDER BY application_id;
        """, (pet_id,))

        rows = cur.fetchall()
        print_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])

    except Exception as e:
        print(f"Error viewing applications by pet: {e}")
    finally:
        cur.close()
        conn.close()


def view_applications_by_user():
    conn = get_connection()
    if conn is None:
        return

    try:
        user_id = safe_int_input("Enter user_id: ")
        cur = conn.cursor()

        cur.execute("""
            SELECT application_id, user_id, pet_id, status, submitted_at, notes
            FROM AdoptionApplication
            WHERE user_id = %s
            ORDER BY application_id;
        """, (user_id,))

        rows = cur.fetchall()
        print_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])

    except Exception as e:
        print(f"Error viewing applications by user: {e}")
    finally:
        cur.close()
        conn.close()


def update_application_status():
    conn = get_connection()
    if conn is None:
        return

    try:
        application_id = safe_int_input("Enter application_id: ")
        new_status = safe_status_input("Enter new status: ")

        cur = conn.cursor()

        cur.execute("""
            SELECT pet_id
            FROM AdoptionApplication
            WHERE application_id = %s;
        """, (application_id,))

        row = cur.fetchone()
        if not row:
            print("Error: application_id does not exist.")
            return

        pet_id = row[0]

        cur.execute("""
            UPDATE AdoptionApplication
            SET status = %s
            WHERE application_id = %s;
        """, (new_status, application_id))

        if new_status == "Approved":
            cur.execute("""
                UPDATE Pet
                SET available = FALSE
                WHERE pet_id = %s;
            """, (pet_id,))

        conn.commit()
        print("Application status updated successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Error updating status: {e}")
    finally:
        cur.close()
        conn.close()


def show_menu():
    print_separator()
    print("Pet Adoption Management System")
    print("1. View all pets")
    print("2. View available pets")
    print("3. Submit adoption application")
    print("4. View all applications")
    print("5. View applications by pet ID")
    print("6. View applications by user ID")
    print("7. Update application status")
    print("8. Count applications per pet")
    print("9. View approved applications")
    print("0. Exit")
    print_separator()


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_pets()
        elif choice == "2":
            view_available_pets()
        elif choice == "3":
            submit_application()
        elif choice == "4":
            view_all_applications()
        elif choice == "5":
            view_applications_by_pet()
        elif choice == "6":
            view_applications_by_user()
        elif choice == "7":
            update_application_status()
        elif choice == "8":
            count_applications_per_pet()
        elif choice == "9":
            view_approved_applications()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose from the menu.")


if __name__ == "__main__":
    main()


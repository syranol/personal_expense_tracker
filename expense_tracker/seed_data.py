import sqlite3
from pathlib import Path

from data_class import Expense

DB_PATH = Path(__file__).resolve().parents[1] / "expense_tracker.db"

def insert_user(conn, user_info):
    """ Add user, query user_id and return user_id """

    conn.execute(
        "INSERT OR IGNORE INTO users (name) VALUES (?)",
        (user_info['name'], )
    )
    
    row = conn.execute(
        "SELECT user_id FROM users WHERE name= ?",
        (user_info['name'], )
    ).fetchone()

    user_id = row[0] if row else None

    return user_id

def insert_category(conn, category_info):
    
    conn.execute(
        "INSERT OR IGNORE INTO categories (name) VALUES (?)",
        (category_info['category'], )
    )

    row = conn.execute(
        "SELECT category_id FROM categories WHERE name= ?",
        (category_info['category'], )
    ).fetchone()

    category_id = row[0] if row else None

    return category_id

def insert_merchant(conn, merchant_info):
    """ Add merchant, query merchant_id and return merchant_id """

    conn.execute(
        "INSERT OR IGNORE INTO merchants (name) VALUES (?)",
        (merchant_info['name'], )
    )
    
    row = conn.execute(
        "SELECT merchant_id FROM merchants WHERE name= ?",
        (merchant_info['name'], )
    ).fetchone()

    merchant_id = row[0] if row else None

    return merchant_id

def insert_expense(conn, expense_info):

    e_i = expense_info
    
    conn.execute("""
        INSERT OR IGNORE INTO expenses
        (user_id, category_id, merchant_id, amount_cents, expense_date, note)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        e_i.user_id,
        e_i.category_id,
        e_i.merchant_id,
        e_i.amount_cents,
        e_i.expense_date,
        e_i.note
    ))

def insert_budget(conn, user_id, category_id, month, amount_cents):
    """Insert or ignore a single budget record."""
    conn.execute("""
        INSERT OR IGNORE INTO budgets
        (user_id, category_id, month, amount_cents)
        VALUES (?, ?, ?, ?)
    """, (user_id, category_id, month, amount_cents))

def main():
    
    # Start connection
    conn = sqlite3.connect(DB_PATH)

    # Add seed data
    try:
        user_id = insert_user(conn, {'name': "Sean"})
        coffee_category_id = insert_category(conn, {'category': "Coffee"})
        food_category_id = insert_category(conn, {'category': "Food"})
        transportation_category_id = insert_category(conn, {'category': "Transportation"})
        entertainment_category_id = insert_category(conn, {'category': "Entertainment"})

        merchant_id = insert_merchant(conn, {'name': "SPRO Coffee Lab"})
        merchant_id_1 = insert_merchant(conn, {'name': "Kokkari Estiatorio"})
        merchant_id_2 = insert_merchant(conn, {'name': "House of Prime Rib"})
        merchant_id_3 = insert_merchant(conn, {'name': "Chez Maman West"})
        merchant_id_4 = insert_merchant(conn, {'name': "Bon, Nene"})

        # Seed expenses
        expenses = [
            Expense(user_id, 1, merchant_id, 856, "2025-11-01", "Latte"),
            Expense(user_id, coffee_category_id, merchant_id, 732, "2025-11-03", None),
            Expense(user_id, coffee_category_id, merchant_id, 632, "2025-11-01", None),
            Expense(user_id, coffee_category_id, merchant_id, 742, "2025-11-01", None),
            Expense(1, food_category_id, merchant_id_1, 24700, "2025-10-27", None),
            Expense(1, food_category_id, merchant_id_2, 10500, "2025-09-12", None),
            Expense(1, food_category_id, merchant_id_3, 7200, "2025-04-08", None),
            Expense(1, food_category_id, merchant_id_4, 5600, "2025-11-01", None),
            Expense(1, food_category_id, merchant_id_4, 6300, "2025-07-21", None)
        ]
        for e in expenses:
            insert_expense(conn, e)

        # Seed budgets (NEW)
        insert_budget(conn, user_id, food_category_id, "2025-11", 40000)   # $400
        insert_budget(conn, user_id, coffee_category_id, "2025-11", 10000) # $100

        # Save and End Connection
        conn.commit()
        print("✅ All seed data inserted successfully.")

    except Exception as error:
        print("Exception encountered while seeding:", error)

    # Close connection
    finally:
        conn.close()

    

if __name__ == "__main__":
    main()

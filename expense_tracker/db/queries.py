import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def get_total_by_category():

    # 1. Define SQL
    sql = """
    SELECT c.name AS category, 
           ROUND(SUM(e.amount_cents)/100.0, 2) as total_spent
    FROM expenses e
    JOIN categories c ON e.category_id == c.category_id
    GROUP BY c.name
    ORDER BY total_spent DESC;
    """

    # 2. Call get_connection
    with get_connection() as conn:
        # 3. Execute and return result
        result = conn.execute(sql).fetchall()
        return result
    
    # This is for testing data
    # for row in result:
    #     print(dict(row))
    

def get_monthly_summary():

    sql = """
    SELECT strftime('%Y-%m', expense_date) AS month, 
           ROUND(SUM(amount_cents)/100.0,2) AS total_spent
    FROM expenses
    GROUP BY month
    ORDER BY month;
    """
    
    with get_connection() as conn:
        return conn.execute(sql).fetchall()

def get_top_expenses(limit=3):
    
    sql = """
    SELECT
        e.expense_date,
        c.name AS category,
        e.note,
        ROUND(e.amount_cents/100.0,2) AS amount
    FROM expenses e
    JOIN categories c ON e.category_id = c.category_id
    ORDER BY amount_cents DESC
    LIMIT ?;
    """

    with get_connection() as conn:
        return conn.execute(sql, (limit,)).fetchall()
    
def get_filtered_report(start_date, end_date, category=None):
    """ Filter report by provided date range and category """
    sql = """
    SELECT c.name AS category,
           ROUND(SUM(e.amount_cents)/100.0, 2) AS total_spent
    FROM expenses e
    JOIN CATEGORIES c ON e.category_id = c.category_id
    WHERE expense_date BETWEEN ? AND ?
        AND (? IS NULL OR c.name = ?)
    GROUP BY c.name
    ORDER BY total_spent DESC;
    """

    with get_connection() as conn:
        return conn.execute(sql, (start_date, end_date, category, category)).fetchall()

def get_budget_vs_actual(month):
    sql = """
    SELECT c.name, b.month, 
           ROUND(b.amount_cents/100.0,2) AS budget,
           ROUND(COALESCE(SUM(e.amount_cents),0)/100.0,2) AS spent,
           ROUND((b.amount_cents - COALESCE(SUM(e.amount_cents),0))/100.0,2) AS remaining
    FROM budgets b
    JOIN categories c ON c.category_id = b.category_id
    LEFT JOIN expenses e ON e.category_id = b.category_id
    WHERE b.month = ?
    GROUP BY c.name
    ORDER BY c.name;
    """

    with get_connection() as conn:
        return conn.execute(sql, (month,)).fetchall()
    

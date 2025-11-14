'''
Personal Expense Tracker
'''

from db import queries

def print_table(title, rows):
    print(f"\n📊 {title}")
    print("-" * 60)
    if not rows:
        print("(no results)")
        return

    # Print columns dynamically
    keys = rows[0].keys()
    print(" | ".join(keys))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(row[k] if row[k] is not None else "-") for k in keys))

def main():
    # print_table("Total by Category", queries.get_total_by_category())
    # print_table("Monthly Summary", queries.get_monthly_summary())
    # print_table("Top 3 Expenses", queries.get_top_expenses(3))
    # print_table(
    #     "Filtered Report (Nov 1-30, 2025)",
    #     queries.get_filtered_report('2025-11-01', '2025-11-30', None)
    # )
    print_table("Budget v.s Actual", queries.get_budget_vs_actual('2025-11'))
if __name__ == "__main__":
    main()
from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    user_id: int
    category_id: int
    merchant_id: int
    amount_cents: int
    expense_date: str
    note: Optional[str] = None
    expense_id: Optional[int] = None
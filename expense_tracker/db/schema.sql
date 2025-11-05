CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS merchants (
    merchant_id INTEGER PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS expenses (
    expense_id      INTEGER PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    category_id     INTEGER NOT NULL,
    merchant_id     INTEGER NOT NULL,
    amount_cents    INTEGER NOT NULL CHECK (amount_cents >0),
    expense_date    TEXT NOT NULL,
    note            TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE TABLE IF NOT EXISTS budgets (
    budget_id       INTEGER PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    category_id     INTEGER NOT NULL,
    month           TEXT NOT NULL,                  -- 'YYYY-MM'
    amount_cents    INTEGER NOT NULL CHECK (amount_cents >= 0),
    UNIQUE(user_id, category_id, month),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE INDEX IF NOT EXISTS idx_budgets_month ON budgets(month);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(expense_date);
CREATE INDEX IF NOT EXISTS idx_expenses_cateogry ON expenses(category_id);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    expense_date TEXT NOT NULL
);

INSERT INTO expenses
(description, category, amount, expense_date)
VALUES
('Grocery shopping', 'Food', 1200, '2026-10-01'),
('Bus ticket', 'Travel', 150, '2026-10-02'),
('Electricity bill', 'Utilities', 900, '2026-10-03'),
('Lunch', 'Food', 250, '2026-10-04'),
('Movie ticket', 'Entertainment', 350, '2026-10-05');

-- View all expenses
SELECT * FROM expenses;

-- Calculate total spending
SELECT SUM(amount) AS total_expenses
FROM expenses;

-- Category-wise total
SELECT category, SUM(amount) AS total
FROM expenses
GROUP BY category
ORDER BY total DESC;

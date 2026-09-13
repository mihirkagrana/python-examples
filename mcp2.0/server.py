import os  
import sqlite3  

from mcp.server import MCPServer  


BASE_DIR = os.path.dirname(__file__)  
DB_PATH = os.path.join(BASE_DIR, "data", "expenses.db")  
CATEGORIES_PATH = os.path.join(BASE_DIR, "categories.json")  

mcp = MCPServer("BillExpenseTracker", version="2.0.0")  


def init_db():  
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) 
    connection = sqlite3.connect(DB_PATH)  
    connection.execute( 
        """
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
        """
    )  
    connection.commit()  
    connection.close()  


@mcp.tool()  
def add_expense(date: str, amount: float, category: str) -> dict:  
    """Add a new expense entry to the database.""" 
    init_db()  
    connection = sqlite3.connect(DB_PATH) 
    cursor = connection.execute( 
        "INSERT INTO expenses(date, amount, category) VALUES (?, ?, ?)",  
        (date, amount, category),  
    )  
    expense_id = cursor.lastrowid 
    connection.commit()  
    connection.close()  
    return {"status": "ok", "id": expense_id} 


@mcp.tool()  
def list_expenses(start_date: str, end_date: str) -> list[dict]:  
    """List expense entries within an inclusive date range.""" 
    init_db() 
    connection = sqlite3.connect(DB_PATH)  
    cursor = connection.execute(  
        """
        SELECT id, date, amount, category
        FROM expenses
        WHERE date BETWEEN ? AND ?
        ORDER BY id ASC
        """,
        (start_date, end_date), 
    )  
    column_names = [column[0] for column in cursor.description]  
    expenses = [dict(zip(column_names, row)) for row in cursor.fetchall()]  
    connection.close() 
    return expenses  


@mcp.resource("expense://categories", mime_type="application/json")  
def categories() -> str: 
    """Read the available expense categories."""  
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as file:  
        return file.read() 


if __name__ == "__main__": 
    init_db() 
    mcp.run() 
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)  # HTTP option.

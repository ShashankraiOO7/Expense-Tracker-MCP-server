import sqlite3
from fastmcp import FastMCP
import os

mcp= FastMCP(name='ExpenserecordTracker')
db_path=os.path.join(os.path.dirname(__file__),"kharcharecord.db")

validate_path= os.path.join(os.path.dirname(__file__),'validation.json')

def init_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
                    CREATE TABLE if not exists kharcha(
                        id integer primary key autoincrement,
                        date text not null,
                        amount float not null,
                        category text not null,
                        subcategory text default '',
                        description text  
                        )'''
                    )
init_db()
@mcp.tool
def add_kharcha(date: str, amount: float, category: str, subcategory: str = '', description: str = '') -> str:
    """Add a new expense record."""
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
                    INSERT INTO kharcha(date, amount, category, subcategory, description)
                    VALUES (?, ?, ?, ?, ?)''',
                    (date, amount, category, subcategory, description)
                    )
    return "Expense record added successfully."

@mcp.tool
def veiw_kharcha(start_date:str,end_date:str,cateory:str = None,date:str=None,amount:str=None)-> list[tuple]:
    
    """View expense records within a date range, optionally filtered by category, date, or amount."""
    query = "SELECT * FROM kharcha WHERE 1=1 AND date BETWEEN ? AND ?"
    params = [start_date, end_date]

    if cateory:
        query += " AND category = ?"
        params.append(cateory)
    if date:
        query += " AND date = ?"
        params.append(date)
    if amount:
        query += " AND amount = ?"
        params.append(amount)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(query, params)
        records = cursor.fetchall()

    return records

@mcp.tool
def delete_kharcha(record_id: int=None,date:str=None,amount=None,category:str=None) -> str:
    """Delete expense records by ID, date, amount, or category."""
    query = "DELETE FROM kharcha WHERE 1=1"
    params = []

    if record_id is not None:
        query += " AND id = ?"
        params.append(record_id)
    if date is not None:
        query += " AND date = ?"
        params.append(date)
    if amount is not None:
        query += " AND amount = ?"
        params.append(amount)
    if category is not None:
        query += " AND category = ?"
        params.append(category)

    with sqlite3.connect(db_path) as conn:
        conn.execute(query, params)

    return "Expense record(s) deleted successfully."

@mcp.tool
def update_kharcha(record_id: int, date: str = None, amount: float = None, category: str = None, subcategory: str = None, description: str = None) -> str:
    """Update an existing expense record."""
    query = "UPDATE kharcha SET "
    params = []
    updates = []

    if date is not None:
        updates.append("date = ?")
        params.append(date)
    if amount is not None:
        updates.append("amount = ?")
        params.append(amount)
    if category is not None:
        updates.append("category = ?")
        params.append(category)
    if subcategory is not None:
        updates.append("subcategory = ?")
        params.append(subcategory)
    if description is not None:
        updates.append("description = ?")
        params.append(description)

    query += ", ".join(updates) + " WHERE id = ?"
    params.append(record_id)

    with sqlite3.connect(db_path) as conn:
        conn.execute(query, params)

    return "Expense record updated successfully."

@mcp.tool
def generate_report(start_date: str, end_date: str) -> list[tuple]:
    """Generate a summary report of expenses within a date range."""
    query = '''
            SELECT category, SUM(amount) as total_amount
            FROM kharcha
            WHERE date BETWEEN ? AND ?
            GROUP BY category
            '''
    params = [start_date, end_date]

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(query, params)
        report = cursor.fetchall()

    return report

@mcp.resource("expense://categories", mime_type="application/json")
def expense_resource():
    """Resource for expense record validation."""
    with open(validate_path, 'r') as file:
        return file.read()
if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
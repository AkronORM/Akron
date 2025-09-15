"""Example: SQLite multi-table and foreign key usage."""

from akron import Akron

def run_example():
    db = Akron("sqlite:///:memory:")
    db.create_table("users", {"id": "int", "name": "str"})
    db.create_table("orders", {"id": "int", "user_id": "int->users.id", "amount": "float"})
    alice_id = db.insert("users", {"name": "Alice"})
    bob_id = db.insert("users", {"name": "Bob"})
    db.insert("orders", {"user_id": alice_id, "amount": 100.0})
    db.insert("orders", {"user_id": bob_id, "amount": 50.0})
    print("Users:", db.find("users"))
    print("Orders:", db.find("orders"))
    db.close()

if __name__ == "__main__":
    run_example()

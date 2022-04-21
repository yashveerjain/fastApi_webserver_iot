import os
import sqlite3
from passlib.context import CryptContext
import sys

dir_path = sys.argv[1]


DATABASE_CONN_STR = os.path.join(dir_path,"sql_app.db")


def create_superadmin(db_conn, email: str, pwd: str):
    """Create a superadmin organization user along with their organization."""

    # Create new Organization
    query = """
        INSERT INTO user(
            username,
            email,
            hashed_password,
            isadmin
        )
        VALUES (
            'Admin',
            (?),
            (?),
            true
        )
        
    """
    # Create new Admin user
    hashed_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(pwd)
    cursor = db_conn.cursor()
    cursor.execute(
        query,
        (
            email,
            hashed_pwd,
        ),
    )
    cursor.fetchone()
    cursor.close()

    db_conn.commit()
    print(f"Successfully created superadmin user {email}") #(ID {org_user_id})")
    print(f"with password '{pwd}'")


if __name__ == "__main__":
    db_conn = sqlite3.connect(DATABASE_CONN_STR,check_same_thread=False)
    create_superadmin(db_conn, "admin@homeauto.com", "admin")
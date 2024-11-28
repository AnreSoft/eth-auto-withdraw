import sqlite3 as sq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

DB_FILE = 'seeds.db'

def create_db():
    """Create the database and initialize the seeds table."""
    with sq.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS seeds(
                address TEXT PRIMARY KEY,
                privatekey TEXT
            )
        """)
        con.commit()
    logging.info('Database initialized.')

def is_address_monitored(address):
    """Check if an address is in the database."""
    with sq.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("SELECT address FROM seeds WHERE address = ?", (address,))
        return cur.fetchone() is not None

def add_seed(address, private_key):
    """Add a new seed (address and private key) to the database."""
    with sq.connect(DB_FILE) as con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO seeds (address, privatekey) VALUES (?, ?)", (address, private_key))
            con.commit()
            logging.info(f"Added new seed: {address}")
        except sq.IntegrityError:
            logging.warning(f"Address already exists in database: {address}")

def get_private_key(address):
    """Retrieve the private key for a given address."""
    with sq.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute("SELECT privatekey FROM seeds WHERE address = ?", (address,))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(f"Address not found in database: {address}")

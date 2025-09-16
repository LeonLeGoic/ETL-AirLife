"""
Data Loading Module

This module handles loading cleaned data into PostgreSQL database:
- Load airport data to airports table
- Load flight data to flights table  
- Verify data was loaded correctly
"""

import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2

# Database connection configuration
# ⚠️ Remplace ces valeurs par tes vraies infos
DATABASE_CONFIG = {
    'username': 'postgres',
    'password': 'my_password', 
    'host': 'localhost',
    'port': '5432',
    'database': 'airlife_db'
}

def get_connection_string():
    """Build PostgreSQL connection string"""
    return f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

def load_to_database(airports_df, flights_df):
    """
    Load cleaned data into PostgreSQL database
    
    Args:
        airports_df (pandas.DataFrame): Cleaned airport data
        flights_df (pandas.DataFrame): Cleaned flight data
    """
    print("💾 Loading data to PostgreSQL database...")

    connection_string = get_connection_string()
    
    try:
        # Créer l'engine SQLAlchemy
        engine = create_engine(connection_string)

        # Charger les données des aéroports
        airports_df.to_sql('airports', engine, if_exists='replace', index=False)
        print(f"✅ Loaded {len(airports_df)} airports to database")

        # Charger les données des vols s'il y en a
        if flights_df is not None and not flights_df.empty:
            flights_df.to_sql('flights', engine, if_exists='replace', index=False)
            print(f"✅ Loaded {len(flights_df)} flights to database")
        else:
            print("ℹ️  No flight data to load")

        print("✅ Data loaded successfully!")

    except Exception as e:
        print(f"❌ Error loading data to database: {e}")
        print("💡 Make sure:")
        print("   - PostgreSQL is running")
        print("   - Database 'airlife_db' exists") 
        print("   - Username and password are correct")
        print("   - Tables are created (run database_setup.sql)")

def verify_data():
    """
    Verify that data was loaded correctly by running some basic queries
    """
    print("🔍 Verifying data was loaded correctly...")

    connection_string = get_connection_string()
    
    try:
        engine = create_engine(connection_string)

        # Compter les aéroports
        airports_count = pd.read_sql("SELECT COUNT(*) as count FROM airports", engine)
        print(f"📊 Airports in database: {airports_count.iloc[0]['count']}")

        # Compter les vols
        flights_count = pd.read_sql("SELECT COUNT(*) as count FROM flights", engine)
        print(f"📊 Flights in database: {flights_count.iloc[0]['count']}")

        # Afficher quelques aéroports
        sample_airports = pd.read_sql("SELECT name, city, country FROM airports LIMIT 3", engine)
        print("\n📋 Sample airports:")
        print(sample_airports.to_string(index=False))

        # Afficher quelques vols si disponibles
        sample_flights = pd.read_sql("SELECT * FROM flights LIMIT 3", engine)
        if not sample_flights.empty:
            print("\n✈️  Sample flights:")
            print(sample_flights.to_string(index=False))

    except Exception as e:
        print(f"❌ Error verifying data: {e}")

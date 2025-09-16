"""
Data Transformation Module

This module handles cleaning and transforming the extracted data:
- Clean airport data (remove invalid coordinates, handle missing values)
- Clean flight data (standardize columns, convert units)
- Combine data for loading
"""

import pandas as pd
import numpy as np

def clean_airports(airports_df):
    """
    Clean and validate airport data
    
    Args:
        airports_df (pandas.DataFrame): Raw airport data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned airport data
    """
    if airports_df.empty:
        print("⚠️  No airport data to clean")
        return airports_df
    
    print(f"🧹 Cleaning airport data...")
    print(f"Starting with {len(airports_df)} airports")
    
    # Make a copy to avoid modifying the original
    df = airports_df.copy()
    
    # TODO: Remove rows with missing latitude or longitude
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # TODO: Remove airports with invalid coordinates
    # Latitude should be between -90 and 90
    # Longitude should be between -180 and 180
    df = df[(df['latitude'] >= -90) & (df['latitude'] <= 90)]
    df = df[(df['longitude'] >= -180) & (df['longitude'] <= 180)]
    
    # TODO: Handle missing IATA codes (replace empty strings or 'N' with None)
    df['iata_code'] = df['iata_code'].replace(['', 'N', '\\N'], None)
    
    # TODO: Convert altitude to numeric (handle non-numeric values)
    df['altitude'] = pd.to_numeric(df['altitude'], errors='coerce')
    
    # TODO: Print how many airports remain after cleaning
    print(f"After cleaning: {len(df)} airports remain")
    
    print("⚠️  Airport cleaning not yet implemented")
    return df

def clean_flights(flights_df):
    """
    Clean and standardize flight data from API
    
    Args:
        flights_df (pandas.DataFrame): Raw flight data from API
        
    Returns:
        pandas.DataFrame: Cleaned flight data with proper column names
    """
    if flights_df.empty:
        print("⚠️  No flight data to clean")
        return flights_df
    
    print(f"🧹 Cleaning flight data...")
    print(f"Starting with {len(flights_df)} flights")
    
    # The OpenSky API returns data as a list of lists without column names
    # We need to assign proper column names
    expected_columns = [
        'icao24',           # Unique aircraft identifier
        'callsign',         # Flight callsign
        'origin_country',   # Country of aircraft registration
        'time_position',    # Unix timestamp of position
        'last_contact',     # Unix timestamp of last contact
        'longitude',        # Aircraft longitude
        'latitude',         # Aircraft latitude
        'altitude',         # Aircraft altitude in meters
        'on_ground',        # Boolean: is aircraft on ground
        'velocity',         # Ground speed in m/s
        'true_track',       # Aircraft heading in degrees
        'vertical_rate'     # Vertical speed in m/s
    ]
    
    # Make a copy to avoid modifying the original
    df = flights_df.copy()
    
    # TODO: Assign column names to the DataFrame
    df.columns = expected_columns
    
    # TODO: Remove flights with missing coordinates
    df = df.dropna(subset=['longitude', 'latitude'])
    
    # TODO: Convert altitude from meters to feet (multiply by 3.28084)
    # This makes it easier to understand for aviation
    df['altitude'] = df['altitude'] * 3.28084
    
    # TODO: Remove flights with invalid coordinates
    # Same coordinate bounds as airports
    df = df[(df['latitude'] >= -90) & (df['latitude'] <= 90)]
    df = df[(df['longitude'] >= -180) & (df['longitude'] <= 180)]
    
    # TODO: Clean callsign (remove extra whitespace)
    df['callsign'] = df['callsign'].str.strip()
    
    # TODO: Print how many flights remain after cleaning
    print(f"After cleaning: {len(df)} flights remain")
    
    print("⚠️  Flight cleaning not yet implemented")
    return df

def combine_data(airports_df, flights_df):
    """
    Combine airport and flight data for loading
    
    For this simple exercise, we'll just return both DataFrames separately.
    In a more advanced pipeline, you might:
    - Join flights with nearby airports
    - Calculate distances between aircraft and airports
    - Add airport information to flight records
    
    Args:
        airports_df (pandas.DataFrame): Cleaned airport data
        flights_df (pandas.DataFrame): Cleaned flight data
        
    Returns:
        tuple: (airports_df, flights_df) ready for database loading
    """
    print("🔗 Preparing data for loading...")
    
    # Basic data validation
    print(f"Final airport records: {len(airports_df)}")
    print(f"Final flight records: {len(flights_df)}")
    
    # TODO (Optional): If you want to try something more advanced,
    # you could find the nearest airport for each flight:
    # 
    # def find_nearest_airport(flight_lat, flight_lon, airports_df):
    #     # Calculate distances and return nearest airport
    #     pass
    
    return airports_df, flights_df

def validate_data_quality(df, data_type):
    """
    Helper function to check data quality
    
    Args:
        df (pandas.DataFrame): Data to validate
        data_type (str): Type of data ('airports' or 'flights')
    """
    if df.empty:
        print(f"⚠️  No {data_type} data to validate")
        return
    
    print(f"📊 Data quality report for {data_type}:")
    print(f"   Total records: {len(df)}")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("   Missing values:")
        for col, count in missing_values[missing_values > 0].items():
            print(f"     {col}: {count}")
    else:
        print("   ✅ No missing values")
    
    # Check coordinate bounds if applicable
    if 'latitude' in df.columns and 'longitude' in df.columns:
        invalid_coords = (
            (df['latitude'] < -90) | (df['latitude'] > 90) |
            (df['longitude'] < -180) | (df['longitude'] > 180)
        ).sum()
        
        if invalid_coords > 0:
            print(f"   ⚠️  {invalid_coords} records with invalid coordinates")
        else:
            print("   ✅ All coordinates are valid")

if __name__ == "__main__":
    """Test the transformation functions with sample data"""
    print("Testing transformation functions...\n")
    
    # Create sample airport data for testing
    sample_airports = pd.DataFrame({
        'name': ['Test Airport 1', 'Test Airport 2', 'Invalid Airport'],
        'city': ['Test City 1', 'Test City 2', 'Invalid City'],
        'country': ['Test Country', 'Test Country', 'Invalid Country'],
        'latitude': [48.8566, 51.4700, 999],  # Last one is invalid
        'longitude': [2.3522, -0.4543, -999],  # Last one is invalid
        'iata_code': ['TST', 'TS2', '\\N'],
        'altitude': [100, 200, 'invalid']
    })
    
    # Test airport cleaning
    cleaned_airports = clean_airports(sample_airports)
    validate_data_quality(cleaned_airports, 'airports')
    
    print("\nTransformation testing complete!")

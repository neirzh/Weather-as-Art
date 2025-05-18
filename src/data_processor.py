import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Load weather data from CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the weather data.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded data from {file_path}")
        # **DEBUG: Print column names and types**
        print("DataFrame columns and types:")
        print(df.info())
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{file_path}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Unable to parse '{file_path}'. Please check the file format.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_weather_data(df, month, year):
    """
    Extract average temperature and rainfall for a specific month and year.

    Args:
        df (pandas.DataFrame): DataFrame containing the weather data.
        month (str): Month number (1-12).
        year (str): Year (1901-2023).

    Returns:
        tuple: (average temperature, average rainfall) or (None, None) if data not found.
    """
    if df is None:
        return None, None

    try:
        # Convert inputs to integers
        month_int = int(month)
        year_int = int(year)

        # **DEBUG: Print input values**
        print(f"DEBUG: Input month_int: {month_int}, year_int: {year_int}")

        # Validate inputs
        if not (1 <= month_int <= 12):
            print(f"Error: Month must be between 1 and 12, got {month_int}")
            return None, None

        # **DEBUG: Check unique values in 'Month' column**
        if 'Month' in df.columns:
            print(f"DEBUG: Unique values in 'Month' column: {df['Month'].unique()}")
            print(f"DEBUG: Type of 'Month' column: {df['Month'].dtype}")
        else:
            print("DEBUG: 'Month' column not found in DataFrame.")


        # Extract data for the specified month and year
        # Ensure 'Month' column is integer type for comparison
        if 'Month' in df.columns and df['Month'].dtype != int:
             try:
                 df['Month'] = df['Month'].astype(int)
                 print("DEBUG: Converted 'Month' column to integer type.")
             except ValueError:
                 print("ERROR: Could not convert 'Month' column to integer. Data might be malformed.")
                 return None, None


        filtered_data = df[(df['Month'] == month_int) & (df['Year'] == year_int)]

        # **DEBUG: Print filtered data**
        print("DEBUG: Filtered data:")
        print(filtered_data)


        if filtered_data.empty:
            print(f"No data found for {month_int}/{year_int}")
            return None, None

        # Calculate average temperature and rainfall
        temp = filtered_data['tem'].mean()
        rain = filtered_data['rain'].mean()

        # Handle NaN values
        if np.isnan(temp) or np.isnan(rain):
            print(f"Warning: Missing data for {month_int}/{year_int}")
            return None, None

        return temp, rain

    except ValueError:
        print("Error: Month and year must be valid numbers")
        return None, None
    except KeyError as e:
        print(f"Error: Required column not found in data: {e}")
        return None, None
    except Exception as e:
        print(f"Error processing weather data: {e}")
        return None, None

def get_available_years(df):
    """
    Get the range of available years in the dataset.

    Args:
        df (pandas.DataFrame): DataFrame containing the weather data.

    Returns:
        tuple: (min_year, max_year) or (None, None) if data is invalid.
    """
    if df is None or 'Year' not in df.columns:
        return None, None

    try:
        min_year = df['Year'].min()
        max_year = df['Year'].max()
        return min_year, max_year
    except Exception as e:
        print(f"Error getting available years: {e}")
        return None, None

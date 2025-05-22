import data_processor
import art_generator
import os
import sys
from PIL import Image, ImageTk
# Fallback if PIL is not installed
try:
    from PIL import Image, ImageTk
except ImportError:
    print("PIL not installed. Image display may not work.")
    # Define a fallback function for Image.open
    class DummyImage:
        def __init__(self, path):
            self.path = path
        def show(self):
            print(f"Would display image at {self.path} if PIL was installed")
    Image = type('Image', (), {'open': lambda path: DummyImage(path)})

def display_banner():
    """Display a welcome banner for the application."""
    print("\n" + "=" * 60)
    print("   🌦️  WEATHER ART GENERATOR  🎨")
    print("       Turn weather data into beautiful art")
    print("=" * 60)

def validate_input(prompt, min_val, max_val):
    """
    Validate numeric input within a range.

    Args:
        prompt (str): Input prompt to display.
        min_val (int): Minimum allowed value.
        max_val (int): Maximum allowed value.

    Returns:
        int or None: The validated input value, or None if invalid or 'q' to quit.
    """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'q':
            return 'q'
        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Value must be between {min_val} and {max_val}. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    """Main function to run the Weather Art Generator application."""
    display_banner()

    # Load data file
    csv_path = "../data/Temp_and_rain.csv"
    df = data_processor.load_data(csv_path)
    if df is None:
        print(f"Failed to load data from {csv_path}")
        return

    # Get year range from data
    min_year, max_year = data_processor.get_available_years(df)
    if min_year is None:
        print("Could not determine available years from the dataset.")
        min_year, max_year = 1901, 2023  # Fallback to provided range

    print(f"\nData available from {min_year} to {max_year}")

    # Main application loop
    while True:
        print("\nEnter 'q' at any prompt to quit")

        # Get month input
        month = validate_input(f"Enter month (1-12): ", 1, 12)
        if month == 'q':
            break

        # Get year input
        year = validate_input(f"Enter year ({min_year}-{max_year}): ", min_year, max_year)
        if year == 'q':
            break

        # Get weather data
        print(f"\nFetching weather data for {month}/{year}...")
        temp, rain = data_processor.get_weather_data(df, month, year)

        if temp is not None and rain is not None:
            print(f"📊 Average Temperature: {temp:.2f}°C, Average Rainfall: {rain:.2f}mm")

            # Generate artwork
            print("\n🎨 Generating artwork based on weather data...")
            image_path = art_generator.generate_art(temp, rain)

            if image_path:
                print(f"✅ Artwork generated successfully!")

                # Try to display the image
                try:
                    img = Image.open(image_path)
                    img.show()
                    print(f"\nArtwork saved as {image_path}")
                except Exception as e:
                    print(f"Note: Could not display image automatically ({e})")
                    print(f"You can view the saved image at: {os.path.abspath(image_path)}")
            else:
                print("❌ Failed to generate artwork.")
        else:
            print("❌ No data found for the given month and year.")

        print("\n" + "-" * 40)

    print("\nThank you for using Weather Art Generator! Goodbye. 👋")

if __name__ == "__main__":
    main()

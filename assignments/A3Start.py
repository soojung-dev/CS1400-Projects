# CS1400 – Assignment 3: Part 1
# Author: Soojung Kim & Junghee Kim
# Practice functions with parameters and return values

def convert_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    Formula: F = C * 1.8 + 32
    """
    return celsius * 1.8 + 32


def make_address(city, country):
    """
    Combine city and country into 'City, Country' string.
    """
    return f"{city}, {country}"


# Optional test calls (safe with auto_grader)
if __name__ == "__main__":
    print(convert_to_fahrenheit(0))      # expect 32
    print(convert_to_fahrenheit(100))    # expect 212
    print(make_address("SLC", "USA"))    # expect "SLC, USA"


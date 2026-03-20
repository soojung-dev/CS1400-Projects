# CS1400 – Assignment 3: Part 2 (Driving Cost Calculator)
# Author: Soojung Kim
# This program calculates trip costs for gas and electric vehicles.

def calculate_gas_vehicle_trip_cost(miles, mpg, gas_cost):
    """
    Calculate the cost of a trip for a gas vehicle.
    miles: trip distance in miles
    mpg: vehicle efficiency (miles per gallon)
    gas_cost: dollars per gallon
    """
    return (miles / mpg) * gas_cost


def calculate_electric_vehicle_trip_cost(miles, whpm, kwh_cost):
    """
    Calculate the cost of a trip for an electric vehicle.
    miles: trip distance in miles
    whpm: watt-hours per mile
    kwh_cost: dollars per kilowatt-hour
    """
    return (whpm / 1000) * miles * kwh_cost


def main():
    """
    Ask user for fuel prices, use fixed efficiencies for car/truck/EV,
    then print trip costs for distances from 50 to 500 miles.
    """
    # Get prices from user
    gas_price = float(input("Enter gasoline price ($/gallon): "))
    electric_price = float(input("Enter electricity price ($/kWh): "))

    # Fixed efficiencies
    car_mpg = 24.4          # gas car
    truck_mpg = 14.2        # truck
    electric_whpm = 229     # EV watt-hours per mile

    # Loop through trip distances
    for miles in range(50, 501, 50):
        truck_cost = calculate_gas_vehicle_trip_cost(miles, truck_mpg, gas_price)
        car_cost = calculate_gas_vehicle_trip_cost(miles, car_mpg, gas_price)
        ev_cost = calculate_electric_vehicle_trip_cost(miles, electric_whpm, electric_price)

        # Print results (rounded to whole dollars)
        print(f"For a trip of {miles} miles, the costs are: "
              f"truck ${round(truck_cost)}, car ${round(car_cost)}, electric ${round(ev_cost)}.")


if __name__ == "__main__":
    main()

"""
WI FAM - Crop Yield Monitoring and Farm Record Management System
Module: PROG211 - Object-Oriented Programming 1

A simple system for recording farmers, crops, harvests,
expenses and estimated profits in Sierra Leone.
"""

import json
import math
from pathlib import Path


# File used to store farming records
DATA_FILE = Path(__file__).resolve().parent / "wifam_data.json"

# Sierra Leone's 16 districts
DISTRICTS = (
    "Bo", "Bombali", "Bonthe", "Falaba",
    "Kailahun", "Kambia", "Karene", "Kenema",
    "Koinadugu", "Kono", "Moyamba", "Port Loko",
    "Pujehun", "Tonkolili", "Western Rural",
    "Western Urban"
)


# ==========================================================
# CLASS 1: CROP
# ==========================================================

class Crop:
    """Stores crop information and calculates farm performance."""

    def __init__(self, name, area_acres, harvest_kg,
                 price_per_kg, expenses):

        self.name = name
        self.area_acres = area_acres
        self.harvest_kg = harvest_kg
        self.price_per_kg = price_per_kg
        self.expenses = expenses

    # Calculate estimated revenue and profit
    def revenue(self):
        return self.harvest_kg * self.price_per_kg

    def profit(self):
        return self.revenue() - self.expenses

    def yield_per_acre(self):
        if self.area_acres == 0:
            return 0

        return self.harvest_kg / self.area_acres

    def display_info(self):
        print("\n-----------------------------------")
        print(f"Crop: {self.name}")
        print(f"Farm size: {self.area_acres:.2f} acres")
        print(f"Harvest: {self.harvest_kg:.2f} kg")
        print(f"Yield per acre: {self.yield_per_acre():.2f} kg")
        print(f"Selling price: Le {self.price_per_kg:,.2f}")
        print(f"Estimated revenue: Le {self.revenue():,.2f}")
        print(f"Expenses: Le {self.expenses:,.2f}")
        print(f"Estimated profit: Le {self.profit():,.2f}")
        print("-----------------------------------")

    # Convert crop details into a dictionary for JSON storage
    def to_dict(self):
        return {
            "name": self.name,
            "area_acres": self.area_acres,
            "harvest_kg": self.harvest_kg,
            "price_per_kg": self.price_per_kg,
            "expenses": self.expenses
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["area_acres"],
            data["harvest_kg"],
            data["price_per_kg"],
            data["expenses"]
        )

    @staticmethod
    def valid_number(value):
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            and value >= 0
        )


# ==========================================================
# CLASS 2: FARMER
# ==========================================================

class Farmer:
    """Stores farmer details and their crop records."""

    total_farmers = 0

    def __init__(self, farmer_id, district):
        self.farmer_id = farmer_id
        self.district = district
        self.crops = []

        Farmer.total_farmers += 1

    # Add a crop object to the farmer's list
    def add_crop(self, crop):
        self.crops.append(crop)

    def total_harvest(self):
        return sum(crop.harvest_kg for crop in self.crops)

    def total_expenses(self):
        return sum(crop.expenses for crop in self.crops)

    def total_revenue(self):
        return sum(crop.revenue() for crop in self.crops)

    def total_profit(self):
        return self.total_revenue() - self.total_expenses()

    def most_profitable_crop(self):
        if not self.crops:
            return None

        return max(self.crops, key=lambda crop: crop.profit())

    def display_info(self):
        print("\n===================================")
        print(f"Farmer ID: {self.farmer_id}")
        print(f"District: {self.district}")
        print("===================================")

        if not self.crops:
            print("No crop records available.")
        else:
            for crop in self.crops:
                crop.display_info()

            best_crop = self.most_profitable_crop()
            print(f"\nHighest-profit crop record: {best_crop.name}")

        print(f"\nTotal harvest: {self.total_harvest():,.2f} kg")
        print(f"Total revenue: Le {self.total_revenue():,.2f}")
        print(f"Total expenses: Le {self.total_expenses():,.2f}")
        print(f"Estimated profit: Le {self.total_profit():,.2f}")

    # Prepare farmer records for saving
    def to_dict(self):
        return {
            "farmer_id": self.farmer_id,
            "district": self.district,
            "crops": [crop.to_dict() for crop in self.crops]
        }

    @classmethod
    def from_dict(cls, data):
        farmer = cls(data["farmer_id"], data["district"])

        for crop_data in data["crops"]:
            crop = Crop.from_dict(crop_data)
            farmer.add_crop(crop)

        return farmer

    @classmethod
    def get_total_farmers(cls):
        return cls.total_farmers


# ==========================================================
# SAVE AND LOAD RECORDS
# ==========================================================

def save_data(farmers):
    try:
        records = [farmer.to_dict() for farmer in farmers.values()]

        # Save to a temporary file before replacing the old one
        temporary_file = DATA_FILE.with_suffix(".tmp")

        with open(temporary_file, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

        temporary_file.replace(DATA_FILE)
        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"Unable to save records: {error}")
        return False


def load_data():
    farmers = {}

    if not DATA_FILE.exists():
        return farmers

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError("Saved records must be a list.")

        for record in records:
            farmer = Farmer.from_dict(record)

            if farmer.farmer_id in farmers:
                raise ValueError("Duplicate farmer ID found.")

            farmers[farmer.farmer_id] = farmer

        print("\nPrevious records loaded successfully.")

    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Unable to load saved records: {error}")
        print("Please check the JSON file.")
        raise SystemExit(1)

    return farmers


# ==========================================================
# INPUT VALIDATION
# ==========================================================

def ask_number(message):
    while True:
        try:
            number = float(input(message))

            if Crop.valid_number(number):
                return number

            print("Please enter a number that is zero or greater.")

        except ValueError:
            print("Invalid input. Enter a valid number.")


def ask_positive_number(message):
    while True:
        number = ask_number(message)

        if number > 0:
            return number

        print("Please enter a number greater than zero.")


def ask_district():
    print("\nAVAILABLE DISTRICTS")

    for number, district in enumerate(DISTRICTS, start=1):
        print(f"{number}. {district}")

    while True:
        choice = input("\nSelect district (1-16): ").strip()

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(DISTRICTS):
                return DISTRICTS[number - 1]

        print("Invalid district selection.")


def ask_crop_name():
    while True:
        name = input("Enter crop name: ").strip().title()

        if name:
            return name

        print("Crop name cannot be empty.")


# ==========================================================
# REGISTER FARMER
# ==========================================================

def register_farmer(farmers):
    district = ask_district()
    number = 1

    # Generate a unique farmer ID
    while f"FM-{number:04d}" in farmers:
        number += 1

    farmer_id = f"FM-{number:04d}"
    farmer = Farmer(farmer_id, district)

    farmers[farmer_id] = farmer

    print("\nFarmer registered successfully!")
    print(f"Farmer ID: {farmer_id}")

    if save_data(farmers):
        print("Farmer record saved.")

    return farmer_id


# ==========================================================
# ADD CROP
# ==========================================================

def add_crop_record(farmers):
    farmer_id = input("\nEnter Farmer ID: ").strip().upper()

    farmer = farmers.get(farmer_id)

    if farmer is None:
        print("Farmer ID not found.")
        return

    name = ask_crop_name()
    area = ask_positive_number("Farm size in acres: ")
    harvest = ask_number("Harvest quantity in kg: ")
    price = ask_number("Selling price per kg (Le): ")
    expenses = ask_number("Total expenses (Le): ")

    crop = Crop(name, area, harvest, price, expenses)
    farmer.add_crop(crop)

    print("\nCrop added successfully!")

    if save_data(farmers):
        print("Crop record saved.")


# ==========================================================
# VIEW AND SEARCH FARMERS

def view_farmers(farmers):
    if not farmers:
        print("\nNo registered farmers.")
        return

    for farmer in farmers.values():
        farmer.display_info()


def search_farmer(farmers):
    farmer_id = input("\nEnter Farmer ID: ").strip().upper()
    farmer = farmers.get(farmer_id)

    if farmer:
        farmer.display_info()
    else:
        print("Farmer not found.")


# FARMING REPORT

def farming_report(farmers):
    total_harvest = sum(
        farmer.total_harvest() for farmer in farmers.values()
    )

    total_revenue = sum(
        farmer.total_revenue() for farmer in farmers.values()
    )

    total_expenses = sum(
        farmer.total_expenses() for farmer in farmers.values()
    )

    total_profit = total_revenue - total_expenses

    total_crops = sum(
        len(farmer.crops) for farmer in farmers.values()
    )

    print("\n====================================")
    print("         WI FAM FARMING REPORT")
    print("====================================")
    print(f"Registered farmers: {len(farmers)}")
    print(f"Total crop records: {total_crops}")
    print(f"Total harvest: {total_harvest:,.2f} kg")
    print(f"Total revenue: Le {total_revenue:,.2f}")
    print(f"Total expenses: Le {total_expenses:,.2f}")
    print(f"Estimated profit: Le {total_profit:,.2f}")
    print("====================================")

# MAIN MENU

def main():
    farmers = load_data()

    while True:
        print("\n====================================")
        print("             WI FAM")
        print("    Wi Fam, Wi Fud, Wi Ficha!")
        print("====================================")
        print("1. Register Farmer")
        print("2. Add Crop Record")
        print("3. View All Farmers")
        print("4. Search Farmer")
        print("5. View Farming Report")
        print("6. Save and Exit")
        print("====================================")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            register_farmer(farmers)

        elif choice == "2":
            add_crop_record(farmers)

        elif choice == "3":
            view_farmers(farmers)

        elif choice == "4":
            search_farmer(farmers)

        elif choice == "5":
            farming_report(farmers)

        elif choice == "6":
            if save_data(farmers):
                print("\nAll records saved successfully.")
                print("Thank you for using WI FAM!")
                break

            print("Unable to save. Please try again.")

        else:
            print("Invalid choice. Select 1 to 6.")


# Start the WI FAM program
if __name__ == "__main__":
    main()
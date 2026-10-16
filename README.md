# PROG211-ASSIGNMENT-1-CHERNOR-SULAIMAN-BAH-905006211-DIT01
A Python OOP application for managing farmers, crops, harvests and estimated farming profits in Sierra Leone.


#  WI FAM – Crop Yield Monitoring and Farm Record Management System

**Wi Fam, Wi Fud, Wi Ficha!**

## About the Project

WI FAM means "Our Farm" in Krio. I developed this Python program for my PROG211 – Object-Oriented Programming 1 assignment at Limkokwing University of Creative Technology, Sierra Leone.

The aim of WI FAM is to help farmers keep simple records of their crops, harvests and farming expenses. The system also calculates crop productivity, estimated revenue and profit.

## Main Features

- Register farmers using unique IDs.
- Record crops, farm sizes, harvest quantities, prices and expenses.
- Calculate yield per acre.
- Calculate estimated revenue and profit.
- View and search farmer records.
- Generate farming summary reports.
- Save and load records using JSON.
- Validate numerical inputs.

## Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- JSON
- PyCharm

No additional Python packages are required.

## Object-Oriented Programming

The program uses two main classes:

### Farmer Class

Stores the farmer's ID, district and crop records. It includes methods for adding crops and calculating total harvest, revenue, expenses and profit.

### Crop Class

Stores crop details and calculates estimated revenue, profit and yield per acre.

The project demonstrates classes, objects, attributes, instance methods, class methods, static methods, lists, dictionaries and tuples.

## How to Run the Program

1. Install Python 3.
2. Download or clone this repository.
3. Open the project folder in PyCharm or a terminal.
4. Run:

    python main.py

5. Follow the instructions in the main menu.

## Main Menu

    ====================================
                 WI FAM
        Wi Fam, Wi Fud, Wi Ficha!
    ====================================
    1. Register Farmer
    2. Add Crop Record
    3. View All Farmers
    4. Search Farmer
    5. View Farming Report
    6. Save and Exit
    ====================================

## Sample Input

| Field | Value |
|---|---|
| Farmer ID | FM-0001 |
| District | Bo |
| Crop | Rice |
| Farm size | 2 acres |
| Harvest | 500 kg |
| Selling price | Le 15 per kg |
| Expenses | Le 3,000 |

## Expected Output

    Crop: Rice
    Farm size: 2.00 acres
    Harvest: 500.00 kg
    Yield per acre: 250.00 kg
    Selling price: Le 15.00
    Estimated revenue: Le 7,500.00
    Expenses: Le 3,000.00
    Estimated profit: Le 4,500.00

These results are based on sample values. Revenue assumes the entire harvest is sold.

## Digital Public Goods Principles

While developing WI FAM, I tried to make the system simple, useful and responsible.

**Accessibility:** The program uses a text-based menu and works offline.

**Privacy:** Farmers are identified using unique IDs rather than names or phone numbers. The saved JSON file still needs to be protected.

**Reusability:** The program uses separate classes and methods so that other developers can understand and improve it.

**Local Relevance:** WI FAM includes Sierra Leone's districts and uses the Leone currency.

**Open Source:** The project uses the MIT License, allowing others to use, modify and share the code under its conditions.

WI FAM is a student prototype and has not been officially recognized as a Digital Public Good.

## Data Storage

Farming records are saved in a file named `wifam_data.json`. This file is automatically created when the program saves records.

The saved records can be loaded again when the program restarts.

## Limitations

- No graphical user interface.
- No actual crop sales tracking.
- No seasonal harvest comparisons.
- Records are stored locally.
- Revenue and profit are estimates.

## Future Improvements

I would like to improve WI FAM by adding a graphical interface, sales tracking, seasonal reports and more detailed farming statistics.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Developer

**Chernor Sulaiman Bah**

Diploma in Information Technology

Limkokwing University of Creative Technology, Sierra Leone

**Module:** PROG211 – Object-Oriented Programming 1

**Year:** 2026


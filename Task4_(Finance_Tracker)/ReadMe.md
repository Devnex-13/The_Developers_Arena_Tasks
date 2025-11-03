# Personal Finance Tracker

A small command-line personal finance tracker in Python. Stores transactions in a CSV text file and provides viewing and simple monthly reports. No external libraries required.

## Files
- Task4_(Finance_Tracker).py — main program
- finance_data.txt — data file (created automatically on first run)
- README.md — this file

## Features
- Add Income and Expense transactions (date, type, category, amount, description)
- View all transactions
- Generate monthly report with totals and expense breakdown by category

## Data format
CSV header:
Date,Type,Category,Amount,Description

Example rows (from finance_data.txt):
2025-11-3,Income,Salary,50000,Salary Credited  
2025-11-4,Expense,Food,2500,Mess Monthly Fees

## Quick Start (Windows)
1. Open PowerShell or Command Prompt.
2. Change to the project folder:
   cd "d:\Devanshu_Pote\The_Developers_Arena_Internship\Task4_(Personnel_Finance_Tracker)"
3. Run:
   python Task4_(Finance_Tracker).py
   or
   py -3 Task4_(Finance_Tracker).py

Follow the interactive menu to add transactions, view all, or generate a monthly report.

## Notes
- On first run the program creates finance_data.txt with the header line.
- Keep the CSV format intact if editing the data file manually (commas separate fields; amount should be numeric).
- Dates are stored as entered; monthly reports expect YYYY-MM (e.g., 2025-11).

## License
Add a LICENSE file if you plan to publish this repository.

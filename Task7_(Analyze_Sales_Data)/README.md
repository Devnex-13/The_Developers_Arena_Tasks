# Sales Data Analysis (Task 7)

This mini-project analyzes sales data to find **top products**, **monthly trends**, and generates a short **business insights report** using Python.

## Files

- `sales_data.csv` – Synthetic sales dataset for an electronics retailer (order-level data with date, product, category, region, quantity, price, and revenue).
- `sales_analysis.py` – Python script that:
  - Loads and cleans the data.
  - Calculates top products by revenue and quantity.
  - Builds monthly revenue and quantity trends.
  - Analyzes revenue by region and category.
  - Generates plots and saves them as PNGs in an `outputs/` folder.
  - Writes a text-based business insights summary to `outputs/business_insights_report.txt`.

> Note: There is also a `sales_analysis.ipynb` notebook version, but the main entry point is now the Python script.

## How to Run (Python Script)

1. Create and activate a Python environment (optional but recommended).
2. Install dependencies (from a terminal opened in this folder):
   ```bash
   pip install pandas matplotlib seaborn
   ```
3. Run the analysis script:
   ```bash
   python sales_analysis.py
   ```
4. Check the `outputs/` folder for:
   - CSV summaries (top products, monthly trends, revenue by region/category).
   - Plot images (`monthly_trends.png`, `revenue_by_region_category.png`).
   - `business_insights_report.txt` with the narrative summary.

## Using Your Own Data

If you have your own sales data:

- Replace `sales_data.csv` with your file (or change `file_path` in the first code cell).
- Ensure your file has at least:
  - A date column (update the `parse_dates` argument and column name in `sales_analysis.py` if different).
  - Product, quantity, and revenue (or unit price × quantity so you can compute revenue).
- Adjust column names in `sales_analysis.py` if they differ from the synthetic dataset.

The rest of the script logic (top products, monthly trends, and insights report) will still work with minimal changes as long as those key fields exist.




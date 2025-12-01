import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def load_and_prepare_data(file_path: str = "sales_data.csv") -> pd.DataFrame:
    """Load sales data and add helper columns."""
    df = pd.read_csv(file_path, parse_dates=["order_date"])

    # Basic cleaning
    df = df.dropna(subset=["order_date", "product", "quantity", "revenue"]).copy()

    # Add year-month column for monthly aggregation
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


def analyze_top_products(df: pd.DataFrame):
    """Return top products by revenue and quantity."""
    top_products_revenue = (
        df.groupby("product", as_index=False)["revenue"].sum()
        .sort_values("revenue", ascending=False)
    )

    top_products_qty = (
        df.groupby("product", as_index=False)["quantity"].sum()
        .sort_values("quantity", ascending=False)
    )

    return top_products_revenue, top_products_qty


def analyze_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and quantity by month."""
    monthly = (
        df.groupby("year_month", as_index=False)
        .agg({"revenue": "sum", "quantity": "sum"})
        .sort_values("year_month")
    )
    return monthly


def analyze_region_category(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue by region and category."""
    region_category = (
        df.groupby(["region", "category"], as_index=False)["revenue"].sum()
        .sort_values("revenue", ascending=False)
    )
    return region_category


def plot_monthly_trends(monthly: pd.DataFrame, output_dir: Path):
    """Create and save a monthly trends plot."""
    sns.set(style="whitegrid")
    plt.rcParams["figure.figsize"] = (10, 5)

    fig, ax1 = plt.subplots()

    color = "tab:blue"
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue", color=color)
    ax1.plot(
        monthly["year_month"],
        monthly["revenue"],
        marker="o",
        color=color,
        label="Revenue",
    )
    ax1.tick_params(axis="y", labelcolor=color)
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    color = "tab:orange"
    ax2.set_ylabel("Quantity", color=color)
    ax2.plot(
        monthly["year_month"],
        monthly["quantity"],
        marker="s",
        linestyle="--",
        color=color,
        label="Quantity",
    )
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()
    plt.title("Monthly Sales Trends: Revenue and Quantity")

    output_path = output_dir / "monthly_trends.png"
    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_region_category(region_category: pd.DataFrame, output_dir: Path):
    """Create and save region/category revenue bar chart."""
    sns.set(style="whitegrid")
    plt.rcParams["figure.figsize"] = (10, 5)

    fig, ax = plt.subplots()
    sns.barplot(
        data=region_category,
        x="region",
        y="revenue",
        hue="category",
        ax=ax,
    )
    ax.set_title("Revenue by Region and Category")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = output_dir / "revenue_by_region_category.png"
    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def generate_business_insights(
    df: pd.DataFrame,
    top_products_revenue: pd.DataFrame,
    top_products_qty: pd.DataFrame,
    monthly: pd.DataFrame,
    region_category: pd.DataFrame,
) -> str:
    """Generate a simple business insights narrative."""
    top_rev = top_products_revenue.iloc[0]
    top_qty = top_products_qty.iloc[0]

    monthly_sorted = monthly.sort_values("year_month")
    first_month = monthly_sorted.iloc[0]
    last_month = monthly_sorted.iloc[-1]

    overall_revenue = df["revenue"].sum()
    overall_quantity = df["quantity"].sum()

    best_region = region_category.sort_values("revenue", ascending=False).iloc[0]

    lines = []
    lines.append("BUSINESS INSIGHTS REPORT")
    lines.append("-" * 80)
    lines.append(
        f"Total revenue in the period: ${overall_revenue:,.2f} "
        f"from {overall_quantity} units sold."
    )
    lines.append(
        "Top product by revenue is "
        f"'{top_rev['product']}' with ${top_rev['revenue']:,.2f} in sales, "
        "while the top product by volume is "
        f"'{top_qty['product']}' with {top_qty['quantity']} units sold."
    )
    lines.append(
        "Revenue grew from "
        f"${first_month['revenue']:,.2f} in {first_month['year_month']} "
        f"to ${last_month['revenue']:,.2f} in {last_month['year_month']}."
    )
    lines.append(
        "The strongest region-category combination is "
        f"{best_region['region']} / {best_region['category']} "
        f"with ${best_region['revenue']:,.2f} in revenue over the period."
    )
    lines.append("")
    lines.append("Suggested actions:")
    lines.append(
        "1. Focus marketing and inventory on the top revenue and volume "
        "products to sustain demand."
    )
    lines.append(
        "2. Replicate successful tactics from the best-performing "
        "region/category in underperforming regions."
    )
    lines.append(
        "3. Monitor month-over-month revenue to identify emerging "
        "seasonality or growth trends."
    )

    return "\n".join(lines)


def main():
    data_path = Path("sales_data.csv")
    if not data_path.exists():
        raise FileNotFoundError(
            f"Could not find {data_path}. Make sure the CSV is in this folder."
        )

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # Load and analyze
    df = load_and_prepare_data(str(data_path))

    top_products_revenue, top_products_qty = analyze_top_products(df)
    monthly = analyze_monthly_trends(df)
    region_category = analyze_region_category(df)

    # Save tables to CSV for reference
    top_products_revenue.to_csv(output_dir / "top_products_by_revenue.csv", index=False)
    top_products_qty.to_csv(output_dir / "top_products_by_quantity.csv", index=False)
    monthly.to_csv(output_dir / "monthly_trends.csv", index=False)
    region_category.to_csv(output_dir / "revenue_by_region_category.csv", index=False)

    # Create plots
    monthly_plot_path = plot_monthly_trends(monthly, output_dir)
    region_plot_path = plot_region_category(region_category, output_dir)

    # Generate insights
    report_text = generate_business_insights(
        df,
        top_products_revenue,
        top_products_qty,
        monthly,
        region_category,
    )

    report_path = output_dir / "business_insights_report.txt"
    report_path.write_text(report_text, encoding="utf-8")

    # Also print key outputs to console
    print(report_text)
    print("\nTop products by revenue:")
    print(top_products_revenue.head(10).to_string(index=False))

    print("\nTop products by quantity:")
    print(top_products_qty.head(10).to_string(index=False))

    print("\nMonthly summary:")
    print(monthly.to_string(index=False))

    print("\nRegion/category revenue:")
    print(region_category.to_string(index=False))

    print("\nFiles generated in 'outputs/' folder:")
    print(f"- {monthly_plot_path.name}")
    print(f"- {region_plot_path.name}")
    print("- top_products_by_revenue.csv")
    print("- top_products_by_quantity.csv")
    print("- monthly_trends.csv")
    print("- revenue_by_region_category.csv")
    print("- business_insights_report.txt")


if __name__ == "__main__":
    main()



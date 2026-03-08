import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from xml.sax.saxutils import escape

import pandas as pd


DEFAULT_BACKUP_PATH = Path(
    r"D:/Google 雲端硬碟/Memo/Accounting/Ahorro_Backup_20190522144210.json"
)
DEFAULT_REFERENCE_CSV = Path(
    r"D:/Google 雲端硬碟/Memo/Accounting/2019-05-01-2019-06-01.csv"
)
DEFAULT_OUT_DIR = Path("analysis_output")


def load_ahorro_tables(backup_path: Path) -> Dict[str, pd.DataFrame]:
    data = json.loads(backup_path.read_text(encoding="utf-8"))
    tables = {}
    for item in data["tables"]:
        tables[item["tableName"]] = pd.DataFrame(item["items"])
    return tables


def normalize_ahorro_records(tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    category_df = tables["category"]
    account_df = tables["account"]

    category_name_map = category_df.set_index("_id")["name"].to_dict()
    category_behavior_map = category_df.set_index("_id")["behavior"].to_dict()
    account_map = account_df.set_index("_id")["name"].to_dict()

    rows = []
    for source, income_expense, sign in [
        ("expense", "支出", -1),
        ("income", "收入", 1),
    ]:
        source_df = tables[source].copy()
        source_df["日期"] = pd.to_datetime(source_df["date"], errors="coerce")
        source_df["金額"] = pd.to_numeric(source_df["amount"], errors="coerce")
        source_df["備註"] = source_df["descr"].fillna("").astype(str).str.strip()
        source_df["收入/支出"] = income_expense
        source_df["合計"] = source_df["金額"] * sign
        source_df["舊類別"] = source_df["category_id"].map(category_name_map)
        source_df["舊類別行為"] = source_df["category_id"].map(category_behavior_map)
        source_df["帳戶"] = source_df["account_id"].map(account_map)
        source_df["來源表"] = source
        rows.append(source_df)

    records = pd.concat(rows, ignore_index=True)
    records["日期"] = records["日期"].dt.normalize()
    records["日期字串"] = records["日期"].dt.strftime("%Y-%m-%d")
    records["備註"] = records["備註"].replace({"nan": ""})
    records["類別"] = records["舊類別"]
    return records


def infer_category_mapping(
    records: pd.DataFrame, reference_csv_path: Path
) -> Tuple[Dict[str, str], pd.DataFrame]:
    if not reference_csv_path.exists():
        return {}, pd.DataFrame(
            columns=["舊類別", "推定類別", "票數", "總票數", "信心值", "是否採用"]
        )

    reference_df = pd.read_csv(reference_csv_path)
    reference_df["日期"] = pd.to_datetime(reference_df["日期"], errors="coerce")
    reference_df["日期字串"] = reference_df["日期"].dt.strftime("%Y-%m-%d")
    reference_df["備註"] = reference_df["備註"].fillna("").astype(str).str.strip()
    reference_df["合計"] = pd.to_numeric(reference_df["合計"], errors="coerce")

    date_min = reference_df["日期"].min()
    date_max = reference_df["日期"].max()
    old_slice = records[
        (records["日期"] >= date_min) & (records["日期"] <= date_max)
    ].copy()

    strict = old_slice.merge(
        reference_df[["日期字串", "收入/支出", "備註", "合計", "類別"]].rename(columns={"類別": "新類別"}),
        on=["日期字串", "收入/支出", "備註", "合計"],
        how="inner",
        suffixes=("_old", "_new"),
    )

    if strict.empty:
        return {}, pd.DataFrame(
            columns=["舊類別", "推定類別", "票數", "總票數", "信心值", "是否採用"]
        )

    votes = (
        strict.groupby(["舊類別", "新類別"])
        .size()
        .reset_index(name="票數")
        .sort_values(["舊類別", "票數"], ascending=[True, False])
    )
    votes["總票數"] = votes.groupby("舊類別")["票數"].transform("sum")
    votes["信心值"] = votes["票數"] / votes["總票數"]

    best = votes.drop_duplicates(subset=["舊類別"], keep="first").copy()
    best.rename(columns={"新類別": "推定類別"}, inplace=True)
    best["是否採用"] = (best["信心值"] >= 0.8) & (best["票數"] >= 3)

    mapping = {
        row["舊類別"]: row["推定類別"]
        for _, row in best.iterrows()
        if row["是否採用"]
    }
    return mapping, best[
        ["舊類別", "推定類別", "票數", "總票數", "信心值", "是否採用"]
    ].sort_values(["是否採用", "信心值", "票數"], ascending=[False, False, False])


def apply_mapping(records: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    result = records.copy()
    result["推定類別"] = result["舊類別"].map(mapping).fillna(result["舊類別"])
    result["類別"] = result["推定類別"]
    return result


def build_summary(records: pd.DataFrame) -> str:
    expense_df = records[records["收入/支出"] == "支出"].copy()
    income_df = records[records["收入/支出"] == "收入"].copy()
    expense_total = float(-expense_df["合計"].sum())
    income_total = float(income_df["合計"].sum())
    net_total = float(records["合計"].sum())

    lines = [
        f"總筆數: {len(records):,}",
        f"日期範圍: {records['日期'].min().date()} ~ {records['日期'].max().date()}",
        f"支出筆數: {len(expense_df):,}",
        f"收入筆數: {len(income_df):,}",
        f"支出總額: {expense_total:,.0f}",
        f"收入總額: {income_total:,.0f}",
        f"淨額(收入-支出): {net_total:,.0f}",
        "",
        "支出前 15 類別 (金額):",
    ]
    top_expense = (
        expense_df.assign(支出金額=-expense_df["合計"])
        .groupby("類別")["支出金額"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )
    for cat, value in top_expense.items():
        lines.append(f"- {cat}: {value:,.0f}")
    return "\n".join(lines)


def to_svg_text(x: float, y: float, value: str, size: int = 12, anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'text-anchor="{anchor}" fill="#222">{escape(value)}</text>'
    )


def format_number(value: float) -> str:
    return f"{value:,.0f}"


def write_line_chart_svg(
    labels: List[str],
    series: List[Tuple[str, List[float], str]],
    title: str,
    out_path: Path,
) -> None:
    width = 1280
    height = 680
    left = 90
    right = 40
    top = 60
    bottom = 90
    plot_w = width - left - right
    plot_h = height - top - bottom

    all_values = [v for _, values, _ in series for v in values]
    y_min = min(all_values + [0])
    y_max = max(all_values + [0])
    if y_min == y_max:
        y_min -= 1
        y_max += 1

    def x_pos(i: int) -> float:
        if len(labels) <= 1:
            return left + plot_w / 2
        return left + (plot_w * i / (len(labels) - 1))

    def y_pos(v: float) -> float:
        ratio = (v - y_min) / (y_max - y_min)
        return top + plot_h * (1 - ratio)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect x="0" y="0" width="100%" height="100%" fill="white"/>',
        to_svg_text(width / 2, 30, title, size=22),
    ]

    grid_count = 6
    for i in range(grid_count + 1):
        value = y_min + (y_max - y_min) * i / grid_count
        y = y_pos(value)
        parts.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#e6e6e6" stroke-width="1"/>'
        )
        parts.append(to_svg_text(left - 10, y + 4, format_number(value), size=11, anchor="end"))

    parts.append(
        f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#444" stroke-width="1"/>'
    )

    step = max(1, len(labels) // 10)
    for i, label in enumerate(labels):
        if i % step != 0 and i != len(labels) - 1:
            continue
        x = x_pos(i)
        parts.append(
            f'<line x1="{x:.1f}" y1="{top + plot_h}" x2="{x:.1f}" y2="{top + plot_h + 6}" stroke="#666"/>'
        )
        parts.append(to_svg_text(x, top + plot_h + 22, label, size=11))

    legend_x = left
    legend_y = top - 25
    for name, values, color in series:
        points = " ".join(f"{x_pos(i):.1f},{y_pos(v):.1f}" for i, v in enumerate(values))
        parts.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2.5" points="{points}"/>'
        )
        parts.append(
            f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x + 20}" y2="{legend_y}" stroke="{color}" stroke-width="3"/>'
        )
        parts.append(to_svg_text(legend_x + 26, legend_y + 4, name, size=13, anchor="start"))
        legend_x += 120

    parts.append("</svg>")
    out_path.write_text("\n".join(parts), encoding="utf-8")


def write_horizontal_bar_chart_svg(
    labels: List[str],
    values: List[float],
    title: str,
    out_path: Path,
) -> None:
    width = 1180
    bar_h = 28
    gap = 10
    top_margin = 70
    left = 280
    right = 70
    bottom = 40
    plot_h = len(labels) * (bar_h + gap)
    height = top_margin + plot_h + bottom
    plot_w = width - left - right

    max_value = max(values) if values else 1
    if max_value == 0:
        max_value = 1

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect x="0" y="0" width="100%" height="100%" fill="white"/>',
        to_svg_text(width / 2, 35, title, size=22),
    ]

    for i, (label, value) in enumerate(zip(labels, values)):
        y = top_margin + i * (bar_h + gap)
        bar_w = (value / max_value) * plot_w
        parts.append(
            f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" fill="#4c78a8"/>'
        )
        parts.append(to_svg_text(left - 12, y + bar_h * 0.72, label, size=13, anchor="end"))
        parts.append(to_svg_text(left + bar_w + 8, y + bar_h * 0.72, format_number(value), size=12, anchor="start"))

    parts.append(
        f'<line x1="{left}" y1="{top_margin - 4}" x2="{left}" y2="{top_margin + plot_h}" stroke="#333"/>'
    )
    parts.append("</svg>")
    out_path.write_text("\n".join(parts), encoding="utf-8")


def plot_monthly_income_expense(records: pd.DataFrame, out_path: Path) -> None:
    plot_df = records.copy()
    plot_df["月份"] = plot_df["日期"].dt.to_period("M").dt.to_timestamp()

    month_index = pd.period_range(
        plot_df["月份"].min().to_period("M"),
        plot_df["月份"].max().to_period("M"),
        freq="M",
    ).to_timestamp()

    monthly_income = (
        plot_df[plot_df["收入/支出"] == "收入"].groupby("月份")["合計"].sum().reindex(month_index, fill_value=0)
    )
    monthly_expense = (
        -plot_df[plot_df["收入/支出"] == "支出"].groupby("月份")["合計"].sum().reindex(month_index, fill_value=0)
    )
    monthly_net = plot_df.groupby("月份")["合計"].sum().reindex(month_index, fill_value=0)

    labels = [x.strftime("%Y-%m") for x in month_index]
    series = [
        ("收入", monthly_income.tolist(), "#2a9d8f"),
        ("支出", monthly_expense.tolist(), "#e76f51"),
        ("淨額", monthly_net.tolist(), "#264653"),
    ]
    write_line_chart_svg(labels, series, "Ahorro 舊資料每月收支趨勢", out_path)


def plot_top_expense_categories(records: pd.DataFrame, out_path: Path) -> None:
    expense_df = records[records["收入/支出"] == "支出"].copy()
    top = (
        expense_df.assign(支出金額=-expense_df["合計"])
        .groupby("類別")["支出金額"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .sort_values(ascending=True)
    )
    write_horizontal_bar_chart_svg(
        labels=[str(x) for x in top.index.tolist()],
        values=[float(x) for x in top.values.tolist()],
        title="Ahorro 舊資料支出前 15 類別",
        out_path=out_path,
    )


def plot_monthly_record_counts(records: pd.DataFrame, out_path: Path) -> None:
    plot_df = records.copy()
    plot_df["月份"] = plot_df["日期"].dt.to_period("M").dt.to_timestamp()

    month_index = pd.period_range(
        plot_df["月份"].min().to_period("M"),
        plot_df["月份"].max().to_period("M"),
        freq="M",
    ).to_timestamp()

    monthly_count = (
        plot_df.groupby(["月份", "收入/支出"])
        .size()
        .reset_index(name="筆數")
        .pivot(index="月份", columns="收入/支出", values="筆數")
        .reindex(month_index, fill_value=0)
        .fillna(0)
    )
    labels = [x.strftime("%Y-%m") for x in month_index]
    series = []
    for name, color in [("支出", "#e76f51"), ("收入", "#2a9d8f")]:
        values = (
            monthly_count[name].tolist()
            if name in monthly_count.columns
            else [0.0] * len(labels)
        )
        series.append((name, [float(v) for v in values], color))

    write_line_chart_svg(labels, series, "Ahorro 舊資料每月交易筆數", out_path)



def export_yearly_csvs(converted: pd.DataFrame, out_dir: Path) -> None:
    yearly_dir = out_dir / "yearly_csv"
    yearly_dir.mkdir(parents=True, exist_ok=True)

    date_df = converted.copy()
    date_df["日期"] = pd.to_datetime(date_df["日期"], errors="coerce")
    min_year = int(date_df["日期"].dt.year.min())
    max_year = int(date_df["日期"].dt.year.max())

    for year in range(min_year, max_year + 1):
        start = pd.Timestamp(year=year, month=1, day=1)
        end = pd.Timestamp(year=year + 1, month=1, day=1)
        chunk = date_df[(date_df["日期"] >= start) & (date_df["日期"] < end)].copy()
        if chunk.empty:
            continue

        chunk["日期"] = chunk["日期"].dt.strftime("%Y-%m-%d")
        file_name = f"{year:04d}-01-01-{year + 1:04d}-01-01.csv"
        chunk.to_csv(yearly_dir / file_name, index=False, encoding="utf-8-sig")
def export_outputs(
    records: pd.DataFrame,
    mapping_table: pd.DataFrame,
    out_dir: Path,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    converted = records[["日期字串", "收入/支出", "類別", "備註", "合計"]].copy()
    converted.rename(columns={"日期字串": "日期"}, inplace=True)
    converted = converted.sort_values(["日期", "收入/支出", "合計"], ascending=[True, True, True])
    converted.to_csv(out_dir / "ahorro_preliminary_converted.csv", index=False, encoding="utf-8-sig")
    export_yearly_csvs(converted, out_dir)

    debug_df = records[
        [
            "日期字串",
            "收入/支出",
            "舊類別",
            "推定類別",
            "備註",
            "合計",
            "帳戶",
            "來源表",
        ]
    ].copy()
    debug_df.rename(columns={"日期字串": "日期"}, inplace=True)
    debug_df = debug_df.sort_values(["日期", "來源表", "合計"], ascending=[True, True, True])
    debug_df.to_csv(
        out_dir / "ahorro_preliminary_converted_debug.csv",
        index=False,
        encoding="utf-8-sig",
    )

    mapping_table.to_csv(
        out_dir / "category_mapping_candidates.csv",
        index=False,
        encoding="utf-8-sig",
    )

    (out_dir / "summary.txt").write_text(build_summary(records), encoding="utf-8")

    plot_monthly_income_expense(records, out_dir / "chart_monthly_income_expense.svg")
    plot_top_expense_categories(records, out_dir / "chart_top_expense_categories.svg")
    plot_monthly_record_counts(records, out_dir / "chart_monthly_record_counts.svg")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze Ahorro backup JSON and export preliminary converted CSV."
    )
    parser.add_argument(
        "--backup",
        type=Path,
        default=DEFAULT_BACKUP_PATH,
        help="Path to Ahorro_Backup_*.json",
    )
    parser.add_argument(
        "--reference-csv",
        type=Path,
        default=DEFAULT_REFERENCE_CSV,
        help="Reference CSV used to infer category mapping from overlap period.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory for charts and intermediate files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    tables = load_ahorro_tables(args.backup)
    records = normalize_ahorro_records(tables)

    mapping, mapping_table = infer_category_mapping(records, args.reference_csv)
    mapped_records = apply_mapping(records, mapping)

    export_outputs(mapped_records, mapping_table, args.out_dir)

    print(f"Analysis completed: {args.out_dir.resolve()}")
    print(f"Loaded records: {len(records):,}")
    print(f"Adopted category mappings: {len(mapping):,}")


if __name__ == "__main__":
    main()





import io
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for servers
import matplotlib.pyplot as plt


def generate_pie_chart(stats: list, period_text: str) -> io.BytesIO:
    """
    stats: list of sqlite3.Row with 'category' and 'total'
    Returns a PNG image as BytesIO
    """
    labels = [row["category"] for row in stats]
    sizes = [row["total"] for row in stats]
    total = sum(sizes)

    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
        "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"
    ]

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors[:len(labels)],
        startangle=140,
        pctdistance=0.82,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )

    for text in texts:
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    ax.set_title(f"{period_text} Expenses — ${total:,.2f} total", fontsize=13, fontweight="bold", pad=15)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_bar_chart(stats: list, period_text: str) -> io.BytesIO:
    """Bar chart alternative"""
    labels = [row["category"] for row in stats]
    sizes = [row["total"] for row in stats]
    total = sum(sizes)

    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
        "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(labels, sizes, color=colors[:len(labels)], edgecolor="white", linewidth=1.5)

    for bar, val in zip(bars, sizes):
        ax.text(bar.get_width() + total * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:,.2f}", va="center", fontsize=10, fontweight="bold")

    ax.set_xlabel("Amount (USD)", fontsize=11)
    ax.set_title(f"{period_text} Expenses — ${total:,.2f} total", fontsize=13, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf

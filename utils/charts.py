import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
          "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
          "#FDA7DF", "#9AECDB"]


def generate_pie_chart(stats: list, period_text: str) -> io.BytesIO:
    labels = [row["category"] for row in stats]
    sizes = [row["total"] for row in stats]
    total = sum(sizes)
    colors = COLORS[:len(labels)]

    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 2.5},
        textprops={"fontsize": 11}
    )

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")
        autotext.set_color("white")

    # Custom legend with amounts
    legend_labels = [f"{label}  ${amount:,.2f}" for label, amount in zip(labels, sizes)]
    patches = [mpatches.Patch(color=colors[i], label=legend_labels[i]) for i in range(len(labels))]
    ax.legend(handles=patches, loc="lower center", bbox_to_anchor=(0.5, -0.18),
              ncol=2, fontsize=10, frameon=False)

    ax.set_title(
        f"{period_text}\nTotal: ${total:,.2f}",
        fontsize=14, fontweight="bold", pad=20, color="#2d2d2d"
    )

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=160, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return buf

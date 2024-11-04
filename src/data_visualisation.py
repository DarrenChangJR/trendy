import matplotlib.pyplot as plt
import matplotlib.axes
import pandas as pd

def _plot_closing(ax_close: matplotlib.axes.Axes, df: pd.DataFrame) -> None:
    ax_close.plot(df["close"], label="closing of symbol", color="blue")
    ax_close.set_xlabel("Date")
    ax_close.set_ylabel("Price of Symbol")
    ax_close.set_title("Closing Price of Symbol and Index")
    ax_close_benchmark = ax_close.twinx()
    ax_close_benchmark.plot(df["close_benchmark"], label="closing of index", color="orange")
    ax_close_benchmark.set_ylabel("Price of Index")
    lines, labels = ax_close.get_legend_handles_labels()
    lines2, labels2 = ax_close_benchmark.get_legend_handles_labels()
    ax_close_benchmark.legend(lines + lines2, labels + labels2, loc=0)

def _plot_delta(ax_delta: matplotlib.axes.Axes, df: pd.DataFrame) -> None:
    ax_delta.plot(df["delta"], label="delta of symbol", color="blue")
    ax_delta.set_xlabel("Date")
    ax_delta.set_ylabel("Delta")
    ax_delta.set_title("Delta of Symbol and Index")
    ax_delta.plot(df["delta_benchmark"], label="delta of index", color="orange")

# def

def main_plot(df: pd.DataFrame) -> None:
    fig, (ax_close, ax_delta, _) = plt.subplots(3, 1)
    _plot_closing(ax_close, df)
    _plot_delta(ax_delta, df)
    plt.show()

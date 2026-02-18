from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from joypy import joyplot


def parallel_categories_plot(title, dimensions, color, color_continuous_scale, labels, dataframe):
    fig = px.parallel_categories(
        dataframe,
        dimensions=dimensions,
        color=color,
        labels=labels,
        color_continuous_scale=px.colors.sequential.Inferno if color_continuous_scale else None,
    )
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)


def density_plot(title, x_col, color, category, df: pd.DataFrame):
    if category is None:
        if isinstance(x_col, list):
            for x in x_col:
                fig, ax = plt.subplots()
                sns.kdeplot(data=df, x=x, ax=ax, fill=True, common_norm=False, alpha=0.5, linewidth=0, color=color)
                ax.set_xlabel(x)
                ax.set_title(title)
                st.pyplot(fig)
                plt.close(fig)
            return

        fig, ax = plt.subplots()
        sns.kdeplot(data=df, x=x_col, ax=ax, fill=True, common_norm=False, alpha=0.5, linewidth=0, color=color)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
        return

    if isinstance(x_col, list):
        for x in x_col:
            fig, _axes = joyplot(df, by=category, column=x, figsize=(10, 6), fade=True, overlap=0.5)
            plt.xlabel(x)
            plt.title(title)
            st.pyplot(fig)
            plt.close(fig)
        return

    fig, _axes = joyplot(df, by=category, column=x_col, figsize=(10, 6), fade=True, overlap=0.5)
    plt.xlabel(x_col)
    plt.title(title)
    st.pyplot(fig)
    plt.close(fig)


def bar_chart_plot_na(title, color, df: pd.DataFrame):
    na_counts = df.isna().sum()
    fig, ax = plt.subplots()
    sns.barplot(x=na_counts.index, y=na_counts.values, color=color, ax=ax)
    ax.tick_params(axis="x", rotation=45)
    ax.set_title(title)
    st.pyplot(fig)
    plt.close(fig)


def histogram_plot(title: str, x_col: str, color: str, bins: Optional[int], category: Optional[str], df: pd.DataFrame):
    fig = px.histogram(df, x=x_col, color=category, nbins=bins, title=title)
    fig.update_traces(marker_color=color if category is None else None)
    st.plotly_chart(fig, use_container_width=True)


def pie_plot(title: str, names_col: str, values_col: Optional[str], hole: float, df: pd.DataFrame):
    if values_col:
        fig = px.pie(df, names=names_col, values=values_col, title=title, hole=hole)
    else:
        vc = df[names_col].value_counts(dropna=False).rename_axis(names_col).reset_index(name="count")
        fig = px.pie(vc, names=names_col, values="count", title=title, hole=hole)
    st.plotly_chart(fig, use_container_width=True)


def scatter_plot(title: str, x_col: str, y_col: str, color: Optional[str], size: Optional[str], trendline: Optional[bool], df: pd.DataFrame):
    fig = px.scatter(df, x=x_col, y=y_col, color=color, size=size, title=title, trendline=("ols" if trendline else None))
    st.plotly_chart(fig, use_container_width=True)


def value_counts_plot(title: str, column: str, top_n: int, color: str, df: pd.DataFrame):
    vc = df[column].value_counts(dropna=False).head(top_n).rename_axis(column).reset_index(name="count")
    fig = px.bar(vc, x=column, y="count", title=title)
    fig.update_traces(marker_color=color)
    st.plotly_chart(fig, use_container_width=True)


def bar_count_plot(title: str, x_col: str, color: str, top_n: Optional[int], df: pd.DataFrame):
    vc = df[x_col].value_counts(dropna=False)
    if top_n:
        vc = vc.head(top_n)
    vc = vc.rename_axis(x_col).reset_index(name="count")
    fig = px.bar(vc, x=x_col, y="count", title=title)
    fig.update_traces(marker_color=color)
    st.plotly_chart(fig, use_container_width=True)


def heatmap_count_plot(title: str, x_col: str, y_col: str, cmap: str, annot: bool, df: pd.DataFrame):
    ct = pd.crosstab(df[y_col], df[x_col], dropna=False)
    fig, ax = plt.subplots()
    sns.heatmap(ct, annot=annot, fmt="d", cmap=cmap, ax=ax)
    ax.set_title(title)
    st.pyplot(fig)
    plt.close(fig)


def stacked_bar_count_plot(title: str, x_col: str, stack_col: str, normalize: bool, df: pd.DataFrame):
    ct = pd.crosstab(df[x_col], df[stack_col], normalize="index" if normalize else False, dropna=False)
    plot_df = ct.reset_index().melt(id_vars=x_col, var_name=stack_col, value_name="value")
    fig = px.bar(plot_df, x=x_col, y="value", color=stack_col, title=title, barmode="stack")
    st.plotly_chart(fig, use_container_width=True)


def boxplot_plot(title: str, x_col: Optional[str], y_col: str, color: Optional[str], df: pd.DataFrame):
    fig = px.box(df, x=x_col, y=y_col, color=color, title=title)
    st.plotly_chart(fig, use_container_width=True)

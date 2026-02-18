# DataFrame Agent

## Overview
This project provides a Streamlit app and an LLM-powered agent that analyzes a CSV dataset.  
The agent can transform the dataset and generate plots using built-in tools.  
A shared `DataFrameState` keeps **original** and **current** data in sync for plotting.

## Main Functionality
- Upload a CSV and query it in natural language.
- Apply transformations with `dataset_modify_tool` (filters, groupby, aggregations, etc.).
- Create plots from the current (or original) dataset.
- Return plain text responses when no plot is needed.

## Tools
All plot tools accept `use_original` (default `False`) to choose the source dataset.

### Transformation
- **dataset_modify_tool**: Modify the current dataset in-place.  
  Supports `filter_query`, `select_columns`, `drop_columns`, `rename_columns`, `sort_by`, `fill_na`, `add_column`, `add_column_expr`, `groupby`, `aggregations`, `as_index`.

### Text
- **text_response_tool**: Returns a plain text response.

### Plots
- **bar_chart_plot_na**: Missing values per column.
- **density_plot_tool**: KDE/joyplot density distribution.
- **histogram_plot_tool**: Histogram for a numeric column.
- **scatter_plot_tool**: Scatter plot for two numeric columns.
- **pie_plot_tool**: Category proportions.
- **value_counts_bar_tool**: Value counts (top N).
- **parallel_categorical_plot**: Parallel categories for multiple categorical dimensions.
- **bar_count_plot_tool**: Counts for a single categorical column.
- **heatmap_count_plot_tool**: Counts across two categorical columns (matrix).
- **stacked_bar_plot_tool**: Stacked counts by a second category.
- **box_plot_tool**: Boxplot of numeric distributions (optionally grouped).

## How to Run
1. Install dependencies (example):
   ```bash
   pip install -r requirements.txt
   ```
2. Set your API key:
   ```bash
   set API_KEY=YOUR_KEY
   ```
3. Run the app:
   ```bash
   streamlit run src/app.py
   ```
4. Upload a CSV and enter queries in the UI.

## Notes
- Always transform data with `dataset_modify_tool` before plotting when needed.
- Use `use_original: true` only when a plot should reflect the raw dataset.


import json
from typing import Union, Optional, Type

import pandas as pd
from langchain.tools import BaseTool
from pydantic import BaseModel, PrivateAttr, ValidationError

from tools.schemas import (
    PlotParamsNA,
    PlotParamsDensity,
    PlotParamsParallelCategories,
    PlotParamsHistogram,
    PlotParamsPie,
    PlotParamsScatter,
    PlotParamsValueCounts,
    ModifyDatasetParams,
    TextResponseParams,
    PlotParamsBarCount,
    PlotParamsHeatmapCount,
    PlotParamsStackedBar,
    PlotParamsBoxPlot,
)
from tools.plots import (
    bar_chart_plot_na,
    density_plot,
    parallel_categories_plot,
    histogram_plot,
    pie_plot,
    scatter_plot,
    value_counts_plot,
    bar_count_plot,
    heatmap_count_plot,
    stacked_bar_count_plot,
    boxplot_plot,
)
from tools.state import DataFrameState


def _parse_tool_input(tool_input: Union[str, dict]) -> Union[str, dict]:
    if isinstance(tool_input, str):
        return json.loads(tool_input)
    return tool_input


class CountingNA(BaseTool):
    name: str = "bar_chart_plot_na"
    description: str = "Plot the number of NA per column (bar chart). Params: title, color, use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsNA
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        try:
            parsed = self.args_schema.model_validate(kwargs)
            df = self._state.original if parsed.use_original else self._state.current
            bar_chart_plot_na(parsed.title, parsed.color, df)
            return "NA bar chart created successfully."
        except ValidationError as e:
            return f"Validation error: {e}"
        except Exception as e:
            return f"Failed: {e}"

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class DensityPlotTool(BaseTool):
    name: str = "density_plot_tool"
    description: str = "Density distribution plot. Params: title, x_col, color, category (optional), use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsDensity
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        try:
            parsed = self.args_schema.model_validate(kwargs)
            df = self._state.original if parsed.use_original else self._state.current
            density_plot(parsed.title, parsed.x_col, parsed.color, parsed.category, df)
            return "Density plot generated successfully."
        except ValidationError as e:
            return f"Validation error: {e}"
        except Exception as e:
            return f"Failed: {e}"

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class ParallelCategoriesTool(BaseTool):
    name: str = "parallel_categorical_plot"
    description: str = (
        "Parallel categories diagram for categorical relationships. "
        "Params: dimensions, color, color_continuous_scal, labels, title, use_original (default False)."
    )
    args_schema: Type[BaseModel] = PlotParamsParallelCategories
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        try:
            parsed = self.args_schema.model_validate(kwargs)
            df = self._state.original if parsed.use_original else self._state.current
            parallel_categories_plot(
                parsed.title,
                parsed.dimensions,
                parsed.color,
                parsed.color_continuous_scal,
                parsed.labels,
                df,
            )
            return "Parallel categories plot created successfully."
        except ValidationError as e:
            return f"Validation error: {e}"
        except Exception as e:
            return f"Failed: {e}"

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class HistogramTool(BaseTool):
    name: str = "histogram_plot_tool"
    description: str = "Histogram (distribution). Params: title, x_col, color, bins, category, use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsHistogram
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        histogram_plot(parsed.title, parsed.x_col, parsed.color, parsed.bins, parsed.category, df)
        return "Histogram created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class PieTool(BaseTool):
    name: str = "pie_plot_tool"
    description: str = "Pie chart (proportions). Params: title, names_col, values_col (optional), hole, use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsPie
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        pie_plot(parsed.title, parsed.names_col, parsed.values_col, parsed.hole, df)
        return "Pie chart created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class ScatterTool(BaseTool):
    name: str = "scatter_plot_tool"
    description: str = "Scatter plot (x-y). Params: title, x_col, y_col, color (optional), size (optional), trendline, use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsScatter
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        scatter_plot(parsed.title, parsed.x_col, parsed.y_col, parsed.color, parsed.size, parsed.trendline, df)
        return "Scatter plot created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class ValueCountsTool(BaseTool):
    name: str = "value_counts_bar_tool"
    description: str = "Value counts bar chart (counting amount). Params: title, column, top_n, color, use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsValueCounts
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        value_counts_plot(parsed.title, parsed.column, parsed.top_n, parsed.color, df)
        return "Value-counts bar chart created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class DatasetModifyTool(BaseTool):
    name: str = "dataset_modify_tool"
    description: str = (
        "Modify the current dataframe in-place for downstream plotting. "
        "Params: filter_query, select_columns, drop_columns, rename_columns, "
        "sort_by, ascending, fill_na, add_column, add_column_expr, "
        "groupby, aggregations, as_index."
    )
    args_schema: Type[BaseModel] = ModifyDatasetParams
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        try:
            parsed = self.args_schema.model_validate(kwargs)
            df = self._state.current

            if parsed.filter_query:
                idx = df.query(parsed.filter_query, engine="python").index
                df.drop(df.index.difference(idx), inplace=True)

            if parsed.select_columns:
                drop_cols = [c for c in df.columns if c not in parsed.select_columns]
                df.drop(columns=drop_cols, inplace=True)

            if parsed.drop_columns:
                df.drop(columns=parsed.drop_columns, inplace=True, errors="ignore")

            if parsed.rename_columns:
                df.rename(columns=parsed.rename_columns, inplace=True)

            if parsed.sort_by:
                df.sort_values(by=parsed.sort_by, ascending=parsed.ascending, inplace=True)

            if parsed.fill_na is not None:
                df.fillna(parsed.fill_na, inplace=True)

            if parsed.add_column or parsed.add_column_expr:
                if not (parsed.add_column and parsed.add_column_expr):
                    return "Validation error: add_column and add_column_expr must be provided together."
                df.eval(f"{parsed.add_column} = {parsed.add_column_expr}", inplace=True, engine="python")

            if parsed.groupby:
                if not parsed.aggregations:
                    return "Validation error: aggregations must be provided when using groupby."
                grouped = df.groupby(parsed.groupby, as_index=parsed.as_index).agg(parsed.aggregations)
                self._state.current = grouped.reset_index() if parsed.as_index else grouped

            return "Dataset modified successfully."
        except ValidationError as e:
            return f"Validation error: {e}"
        except Exception as e:
            return f"Failed: {e}"

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class TextResponseTool(BaseTool):
    name: str = "text_response_tool"
    description: str = "Return a plain text response. Params: text."
    args_schema: Type[BaseModel] = TextResponseParams

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        return parsed.text

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class BarCountTool(BaseTool):
    name: str = "bar_count_plot_tool"
    description: str = "Bar plot of category counts. Params: title, x_col, color, top_n (optional), use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsBarCount
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        bar_count_plot(parsed.title, parsed.x_col, parsed.color, parsed.top_n, df)
        return "Bar count plot created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class HeatmapCountTool(BaseTool):
    name: str = "heatmap_count_plot_tool"
    description: str = "Heatmap of counts between two categories. Params: title, x_col, y_col, cmap, annot, use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsHeatmapCount
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        heatmap_count_plot(parsed.title, parsed.x_col, parsed.y_col, parsed.cmap, parsed.annot, df)
        return "Heatmap count plot created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class StackedBarTool(BaseTool):
    name: str = "stacked_bar_plot_tool"
    description: str = "Stacked bar chart of counts. Params: title, x_col, stack_col, normalize, use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsStackedBar
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        stacked_bar_count_plot(parsed.title, parsed.x_col, parsed.stack_col, parsed.normalize, df)
        return "Stacked bar plot created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


class BoxPlotTool(BaseTool):
    name: str = "box_plot_tool"
    description: str = "Boxplot for numeric distributions. Params: title, y_col, x_col (optional), color (optional), use_original (default False)."
    args_schema: Type[BaseModel] = PlotParamsBoxPlot
    _state: DataFrameState = PrivateAttr()

    def __init__(self, state: DataFrameState, **kwargs):
        super().__init__(**kwargs)
        self._state = state

    def _parse_input(self, tool_input: Union[str, dict], tool_call_id: Optional[str] = None):
        return _parse_tool_input(tool_input)

    def _run(self, **kwargs) -> str:
        parsed = self.args_schema.model_validate(kwargs)
        df = self._state.original if parsed.use_original else self._state.current
        boxplot_plot(parsed.title, parsed.x_col, parsed.y_col, parsed.color, df)
        return "Box plot created successfully."

    async def _arun(self, **kwargs) -> str:
        return self._run(**kwargs)


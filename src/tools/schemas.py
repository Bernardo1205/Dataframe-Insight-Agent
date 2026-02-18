from pydantic import BaseModel, Field
from typing import Union, Optional, List, Dict, Any


class PlotParamsNA(BaseModel):
    title: str
    color: str
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsDensity(BaseModel):
    title: str
    x_col: Union[str, List[str]]
    color: str
    category: Optional[str] = None
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsHistogram(BaseModel):
    title: str
    x_col: str
    color: str = "#4C78A8"
    bins: Optional[int] = None
    category: Optional[str] = None
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsPie(BaseModel):
    title: str
    names_col: str
    values_col: Optional[str] = None  # if None -> counts
    hole: float = 0.0  # 0..1
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsScatter(BaseModel):
    title: str
    x_col: str
    y_col: str
    color: Optional[str] = None
    size: Optional[str] = None
    trendline: Optional[bool] = False
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsValueCounts(BaseModel):
    title: str
    column: str
    top_n: int = 20
    color: str = "#72B7B2"
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsParallelCategories(BaseModel):
    dimensions: Union[str, List[str]]
    color: str
    color_continuous_scal: bool
    labels: Dict[str, str]
    title: str
    use_original: bool = Field(False, description="Use original dataset (default False).")


class ModifyDatasetParams(BaseModel):
    filter_query: Optional[str] = None
    select_columns: Optional[List[str]] = None
    drop_columns: Optional[List[str]] = None
    rename_columns: Optional[Dict[str, str]] = None
    sort_by: Optional[Union[str, List[str]]] = None
    ascending: Union[bool, List[bool]] = True
    fill_na: Optional[Union[Dict[str, Any], Any]] = None
    add_column: Optional[str] = None
    add_column_expr: Optional[str] = None
    groupby: Optional[Union[str, List[str]]] = None
    aggregations: Optional[Dict[str, Union[str, List[str]]]] = None
    as_index: bool = False


class TextResponseParams(BaseModel):
    text: str


class PlotParamsBarCount(BaseModel):
    title: str
    x_col: str
    color: str = "#4C78A8"
    top_n: Optional[int] = None
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsHeatmapCount(BaseModel):
    title: str
    x_col: str
    y_col: str
    cmap: str = "Blues"
    annot: bool = True
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsStackedBar(BaseModel):
    title: str
    x_col: str
    stack_col: str
    normalize: bool = False
    use_original: bool = Field(False, description="Use original dataset (default False).")


class PlotParamsBoxPlot(BaseModel):
    title: str
    x_col: Optional[str] = None
    y_col: str
    color: Optional[str] = None
    use_original: bool = Field(False, description="Use original dataset (default False).")

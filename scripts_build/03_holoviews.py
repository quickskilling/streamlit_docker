# %%
import polars as pl
import holoviews as hv
import panel as pn
from holoviews import opts
hv.extension('bokeh')
dat = pl.read_parquet("../data/dat_munged.parquet")
info = pl.read_csv("../data/Metadata_Indicator_API_Download_DS2_en_csv_v2_5657328.csv").rename({"INDICATOR_CODE":"Indicator Code", "INDICATOR_NAME":"Indicator Name"})

dat_vars = dat\
    .group_by("Indicator Name", "Indicator Code", "Country Code").len()\
    .pivot(values="len", index=["Indicator Name", "Indicator Code"], columns="Country Code", aggregate_function="first")\
    .with_columns((pl.col("COD").fill_null(0) + pl.col("GHA").fill_null(0) +
                   pl.col("KEN").fill_null(0) + pl.col("NGA").fill_null(0) +
                   pl.col("ZAF").fill_null(0) + pl.col("ZWE").fill_null(0)).alias("total"))\
    .sort(pl.col("total"), descending=True)\
    .filter(pl.col("total") > 25)

# %%
hv.Scatter(dat.filter(pl.col("Indicator Code").is_in(["NY.GDP.PCAP.PP.KD"])).to_pandas(), "year", "value")\
  .opts(width=500)

# %%
def select_row(row=0):
  return dat.slice(row, 1)

app = pn.interact(select_row, row=(0, dat.select(pl.len()).item()))
print(app)
# %%
pn.Column("## Choose a row", pn.Row(app[0], app[1]))
# %%
color_picker = pn.widgets.ColorPicker()
color_picker
# %%
html = pn.pane.HTML('', width=200, height=200, styles={'background-color': color_picker.value})
color_picker.link(html, value="background-color")# %%
html

# %%
x = pn.widgets.IntSlider(name='x', start=0, end=100)
background = pn.widgets.ColorPicker(name='Background', value='lightgray')

def square(x):
    return f'{x} squared is {x**2}'

def styles(background):
    return {'background-color': background, 'padding': '0 10px'}

pn.Column(
    x,
    background,
    pn.pane.Markdown(pn.bind(square, x), styles=pn.bind(styles, background))
)
# %%

# %%
import polars as pl
import plotly.express as px
import plotly.io as pio
pio.templates.default = "simple_white"

from lets_plot import *
LetsPlot.setup_html()
# ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]

dat = pl.read_csv("../dat_munged.csv")
info = pl.read_csv("../Metadata_Indicator_API_Download_DS2_en_csv_v2_5657328.csv").rename({"INDICATOR_CODE":"Indicator Code", "INDICATOR_NAME":"Indicator Name"})

# %%
dat_vars = dat\
    .group_by("Indicator Name", "Indicator Code", "Country Code").len()\
    .pivot(values="len", index=["Indicator Name", "Indicator Code"], columns="Country Code", aggregate_function="first")\
    .with_columns((pl.col("COD").fill_null(0) + pl.col("GHA").fill_null(0) +
                   pl.col("KEN").fill_null(0) + pl.col("NGA").fill_null(0) +
                   pl.col("ZAF").fill_null(0) + pl.col("ZWE").fill_null(0)).alias("total"))\
    .sort(pl.col("total"), descending=True)\
    .filter(pl.col("total") > 25)

dat_vars.write_csv("../dat_vars.csv")

# %%
ggplot(
    dat.filter(pl.col("Indicator Code").is_in(["NY.GDP.PCAP.PP.KD"])),
    aes(x="year", y="value", color="Country Code")) +\
  geom_line() +\
  geom_point(size=1.2)

# %%
# Access to fuels
# Access to internet
# GDP

drop_country =  ["ZAF"]
indicator_code = "NY.GDP.PCAP.PP.KD"
title_text = dat_vars\
  .filter(pl.col("Indicator Code") == indicator_code)\
  .select("Indicator Name")\
  .to_series()[0]
subtitle_text = info\
  .filter(pl.col("Indicator Code") == indicator_code)\
  .select("SOURCE_NOTE")\
  .to_series()[0]
subtitle_text = subtitle_text[1:100] + "..."
chart_title = title_text + "<br><sup>" + subtitle_text + "</sup>"
y_axis_title = chart_title[chart_title.find("(")+1:chart_title.find(")")]
chart_dat = dat\
  .filter(
    (pl.col("Indicator Code").is_in([indicator_code])) &
    (~pl.col("Country Code").is_in(drop_country)))

chart_plotly = px.line(chart_dat,
    x="year", y="value", color="Country Code", markers=True,
    labels = {"year":"Year", "value":y_axis_title},
    title = chart_title)

chart_lp = ggplot(chart_dat, aes(x="year", y="value", color="Country Code")) +\
  geom_point(shape=21, size=1.25, tooltips="none") +\
  geom_line(tooltips=layer_tooltips()\
            .format('value', '{.0f}')) +\
  labs(
    x="Year", y=y_axis_title,
    title=title_text,
    subtitle=subtitle_text) +\
  scale_x_continuous(format='.0f') +\
  theme(legend_position="bottom")
chart_lp

# %%
# https://2001-2009.state.gov/r/pa/ho/time/pcw/98678.htm#:~:text=Apartheid%2C%20the%20Afrikaans%20name%20given,a%20democratic%20government%20in%201994.
# What happened in South Africa in the 1990s?
# What happened in Nigeria in early 2000?
# What happened in Ghana in 2010s?
# sp.add_annotation(
#         x=1994, y=4100,
#         text="Democratic Government",
#         showarrow=True,
#         yshift=10)

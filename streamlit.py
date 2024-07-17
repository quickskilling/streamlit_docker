# %%
# packages
import streamlit as st
import polars as pl
import plotly.express as px
import plotly.io as pio
pio.templates.default = "simple_white"

st.set_page_config(layout="wide")
# %%
# Data

dat = pl.read_csv("dat_munged.csv")
info = pl.read_csv("Metadata_Indicator_API_Download_DS2_en_csv_v2_5657328.csv").rename({"INDICATOR_CODE":"Indicator Code", "INDICATOR_NAME":"Indicator Name"})
dat_vars = pl.read_csv("dat_vars.csv")

# %%
# Example Chart
# drop_country =  ["ZAF"]
# indicator_code = "NY.GDP.PCAP.PP.KD"
list_name = dat_vars.select("Indicator Name").to_series().to_list()
list_code = dat_vars.select("Indicator Code").to_series().to_list()
list_country_code = ["ZAF", "ZWE", "KEN", "NGA", "GHA", "COD"]
list_country_name = ["South Africa", "Zimbabwe", "Kenya", "Nigeria", "Ghana", "Congo, Dem. Rep."]


drop_country = st.sidebar.multiselect("Remove Country (Country Code)", list_country_code)

checked_var = st.sidebar.checkbox("Use Variable Name")


if checked_var:
    indicator_name = st.sidebar.selectbox("Select your variable", list_name)
    indicator_code = dat_vars.filter(pl.col("Indicator Name") == indicator_name).select("Indicator Code").to_series()[0]
else:
    indicator_code = st.sidebar.selectbox("Select your variable", list_code)
    indicator_name = dat_vars.filter(pl.col("Indicator Code") == indicator_code).select("Indicator Name").to_series()[0]

title_text = indicator_name
subtitle_text = info.filter(pl.col("Indicator Code") == indicator_code).select("SOURCE_NOTE").to_series()[0]

y_axis_title = indicator_name[indicator_name.find("(")+1:indicator_name.find(")")]

use_dat = dat.filter((pl.col("Indicator Code").is_in([str(indicator_code)])) & (~pl.col("Country Code").is_in(drop_country)) & (pl.col("value").is_not_null()))

sp = px.line(use_dat.to_pandas(),
    x="year", y="value", color="Country Name", markers=True,
    labels = {"year":"Year", "value":y_axis_title},
    title = title_text)

st.markdown("## Country performance over time")

st.markdown("_You can read about streamlit [here](slides.html)_")

st.markdown("__" + title_text + "__")

st.markdown(subtitle_text)

st.markdown("### Chart")
st.markdown("_Use the expand arrows visible when you hover over the upper right corner of the chart to see it in full screen._")

sp

st.markdown("### Table: " + title_text)

display_dat = use_dat.select("Country Code", "Indicator Name", "year", "value")

st.dataframe(
  display_dat\
    .pivot(index="year", on="Country Code", values="value", aggregate_function="first")\
    .sort(pl.col("year"),descending=True), hide_index=True,
    use_container_width=True,
    column_config={
        "value": y_axis_title,
        "year": st.column_config.NumberColumn(
            "Year",
            help="Year of data",
            format="%.0f"
        )})


def convert_df(df):
    return df.write_csv().encode('utf-8')

csv = convert_df(display_dat)

st.download_button("Download Data", data = csv, file_name = "data.csv", mime="text/csv")

st.markdown("## My presentation")

# Read file and keep in variable
with open('slides.html','r') as f: 
    html_data = f.read()

## Show in webpage
st.components.v1.html(html_data,height=1500)
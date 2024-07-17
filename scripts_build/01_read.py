# %%
import polars as pl
# Notice that the world health leaves missing as blanks in the csv. We need to explain that blanks aren't strings but missing values.

dat = pl.read_csv("../API_Download_DS2_en_csv_v2_5657328.csv", skip_rows=4, null_values = "")
# We don't like the World Banks wide format.  Let's clean it upt to long format.
dat_long = dat.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"])
# no we need to fix the year column and give it a better name.
# we could have fixed the name as an argument in `.melt()` as well.
# https://docs.pola.rs/user-guide/expressions/casting/#overflow
dat_long = dat_long\
  .with_columns(
    pl.col("variable").cast(pl.Int64, strict=False).alias("variable"),
    pl.col("value").cast(pl.Float32, strict=False).alias("value"))\
  .rename({"variable":"year"})\
  .filter(pl.col("value").is_not_null())


# %%
# Can we split out the information in the indicator Code
indicator_columns = dat_long\
  .select(
    pl.col("Indicator Code"),
    pl.col("Indicator Code")\
    # split string: example VC.IDP.TOCV into list object ["VC", "IDP", "TOCV"]
        .str.split_exact(".", 6).alias("split")).unnest("split")\
  .unique()
      

# What should we call these columns?
# https://datahelpdesk.worldbank.org/knowledgebase/articles/201175-how-does-the-world-bank-code-its-indicators
new_names = {"field_0":"topic", "field_1":"general_subj", "field_2":"specific_subj",
        "field_3":"ext_1", "field_4":"ext_2", "field_5":"ext_3", "field_6":"ext_4"}
indicator_columns = indicator_columns.rename(new_names)

# %%
# now we need to finalize our munge and write our data
dat_final = dat_long.join(indicator_columns, how="left", on="Indicator Code")
# Now I want to reorder the columns
names = dat_final.columns
new_order = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 0]
name_order = [names[i] for i in new_order]
dat_final = dat_final.select(name_order)

# %%
# write data
dat_final.write_csv("../dat_munged.csv")



# %%

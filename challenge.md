# Learning Challenge

- Add the ability to filter the chart to a specified year range with [st.date_input()](https://docs.streamlit.io/develop/api-reference/widgets/st.date_input)
- Add [Dataframes - st.data_editor()](https://docs.streamlit.io/develop/concepts/design/dataframes) to allow the user to pick which variables are displayed in the drop down.
- Add a few metrics to your dashboard using [st.metric()](https://docs.streamlit.io/develop/api-reference/data/st.metric)
  - Report the year range of data available for the variable selected over all countries
  - Add the percent growth from 2000 to the latest available year
  - Add the country with the highest value in the latest year.
- Give the user of your app the ability to take a picture using [st.camera_input()](https://docs.streamlit.io/develop/api-reference/widgets/st.camera_input).
- Try to use a third party extension to allow the user to draw on the camera picture taken using [streamlit-drawable-canvas](https://github.com/andfanilo/streamlit-drawable-canvas?tab=readme-ov-file).
- Now organize your application using
  - [st.set_page_config()](https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config)
  - [st.columns()](https://docs.streamlit.io/develop/api-reference/layout/st.columns)
  
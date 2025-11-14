# US Air Pollution Analysis

**US Air Pollution Analysis** is a comprehensive data analysis tool designed to streamline data exploration, analysis, and visualisation. The tool supports multiple data formats and provides an intuitive interface for both novice and expert data scientists.

## Dataset Content
* This project uses the [US Pollution Dataset](https://www.kaggle.com/datasets/sogun3/uspollution) from Kaggle
* The dataset contains the following columns:

| Category | Column Name | Description |
| --- | --- | --- |
| Location | State Code, County Code, State, County, City | Geographic information for where samples were taken |
| Monitoring Site | Site Num, Address | Specific monitoring location information |
| Date | Date Local | Date on which sample was collected |
| Nitrogen Oxides | NO2 Mean, NO2 1st Max Value, NO2 1st Max Hour, NO2 AQI | NO2 measures in parts per billion |
| Ozone | O3 Mean, O3 1st Max Value, O3 1st Max Hour, O3 AQI | O3 measures in parts per million |
| Sulphur Dioxide | SO2 Mean, SO2 1st Max Value, SO2 1st Max Hour, SO2 AQI | SO2 measures in parts per billion |
| Carbon Monoxide | CO Mean, CO 1st Max Value, CO 1st Max Hour, CO AQI | CO measures in parts per million |

## Project Pages
* Data ETL: [cleaning.ipynb](jupyter_notebooks\cleaning.ipynb)
* Hypotheses Validation: [H1](jupyter_notebooks\hypothesis_population_correlation.ipynb), [H2](jupyter_notebooks/hypothesis_measurement_coverage.ipynb), [H3](jupyter_notebooks/hypothesis_regional_differences.ipynb), [H4](jupyter_notebooks/hypothesis_urban_vs_rural.ipynb), [H5](jupyter_notebooks\hypothesis_event_impact.ipynb)
* Preparing mapping data: [etl_extract_cood.ipynb](jupyter_notebooks/etl_extract_cood.ipynb) and [build_enriched_dataset.ipynb](jupyter_notebooks\build_enriched_dataset.ipynb)
* The dashboard was created in Streamlit and is available at this link: [US Pollution Dashboard](https://jxywwgotg8wauagztuhaiw.streamlit.app/)

## Business Requirements
* Visualise pollution levels across the United States to identify high-risk regions allowing for geographical analysis and<br>
helping businesses assess environmental risks in regions where they operate or plan to expand. This also helps to highlight<br>
regions where there is the greatest need for sustainability policies or business solutions that would reduce pollutants.
* Show pollution levels over time to monitor improvements or deteriorations in air quality and explain pollution trends and<br>
the impact of major events on pollutant levels.
* Break down pollution levels by regions within states to highlight which areas contribute most to overall pollution, this will also allow <br>
local communities to see how their region compares to others, encouraging grassroots environmental action.


## Hypothesis and how to validate?
* **H1**: There is a correlation between population size and pollution levels; more populous areas tend to have higher pollutant concentrations.
* **H2**: Measurement coverage varies by region and population density, potentially leading to gaps or biases in pollution data.
* **H3**: Pollution levels differ significantly between US regions (e.g., Northeast, Midwest, South, West) due to geographic, industrial, and policy factors.
* **H4**: Urban areas have higher pollution levels than rural areas, reflecting differences in population density, traffic, and industrial activity.
* **H5**: Major events within the dataset range (e.g., Hurricane Sandy in 2012, Clean Power Plan in 2015) cause observable changes in pollutant levels over time.

## The rationale to map the business requirements to the Data Visualisations
* Pollution levels by region visualised through interactive heat map and pollution x population scatterplot
* Pollution levels over time visualised through time series line plot
* Pollution levels break down enabled through an interactive tree map and coverage bias highlighted with map visualisation

## Ethical considerations
* The dataset contains no personally identifiable data and is available for use under the Open Database Contents License.

## Dashboard Design
The dashboard was created in Streamlit and is available at this link: [US Pollution Dashboard](https://jxywwgotg8wauagztuhaiw.streamlit.app/)

**Dashboard Pages**<br>
* Introduction: This is the landing page of the site and provides a quick overview of the dashboard contents and navigation
* Heat Map: Shows pollution across a map of the US, users can select pollutants and time frame as well as having a range of options for the granularity of the data displayed
* Population and Polution Correlation: Shows relationsip between pollution level and city population sizes
* Measurement Coverage: Shows monitoring locations and population distributions to highlight coverage bias
* Pollution Over Time: Line plot showing pollution over time, users can select a specific state and/or change time displays to show historical or seasonal trends
* Tree Map: Provides an overview of pollution levels across States, Counties and Cities, users can select which pollutant to visualise
* Event Impact Dashboard: Shows event markers for pollution over time
* Regional Differences: Uses boxplots to show pollutant distributions across regions in the US

**Communication of data insights**
* Data insights are displayed through complex interactive graphs which allow technical users to focus on areas of specific interest and fully explore the data. <br>
Text summaries and simpler charts are provided to give novice users easy access to the most important pollution information.

## Conclusion
The analysis confirms that major events can lead to observable shifts in pollutant levels, although the timing and magnitude of these impacts vary across contexts. <br>Importantly, the data challenges the assumption that urban areas consistently experience higher pollution than rural regions; in fact, rural areas sometimes show comparable or greater pollutant concentrations. <br>Additionally, the monitoring network’s bias toward urban centers highlights a limitation in coverage, potentially underrepresenting rural pollution levels and influencing overall interpretations.

## Next Steps
To build on these findings, future work should expand the scope of pollutants studied, incorporate longer-term datasets, and explore more granular regional differences. <br>Enhancing monitoring coverage in rural areas would provide a more balanced view of national pollution trends. <br>Further, integrating event markers with broader socio-economic or environmental data could deepen understanding of how specific events shape pollution dynamics and inform targeted policy interventions.


## Development Roadmap
The large dataset caused us some issues with uploading to github and managing time taken to perform cleaning and analysis steps.<br>
File size was worked around by using file compression when uploading to github. <br>
Issues with visualisations where overcome by grouping data into manageable sets before charting.

## Main Data Analysis Libraries
* Pandas and Numpy: Used for database manipulation
* Matplotlib, seaborn and plotly: Used to create visualisations within jupyter notebooks and streamlit app
* Scikit Learn: Used for machine learning modelling
* Streamlit for dashboard creation and interactive visualisations


## Credits 

* Generative AI was used to help with ideation, document drafting, code suggestions and bug fixing 
* Web resources were used in creation of dashboard pages and links can be found within the code comments
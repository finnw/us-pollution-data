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

## Project Plan
* Outline the high-level steps taken for the analysis.
* How was the data managed throughout the collection, processing, analysis and interpretation steps?
* Why did you choose the research methodologies you used?

## The rationale to map the business requirements to the Data Visualisations
* Pollution levels by region visualised through interactive heat map
* Pollution levels over time visualised through time series line plot
* Pollution levels break down enabled through an interactive tree map

## Analysis techniques used
* List the data analysis methods used and explain limitations or alternative approaches.
* How did you structure the data analysis techniques. Justify your response.
* Did the data limit you, and did you use an alternative approach to meet these challenges?
* How did you use generative AI tools to help with ideation, design thinking and code optimisation?

## Ethical considerations
* The dataset contains no personally identifiable data and is available for use under the Open Database Contents License.

## Dashboard Design
**Dashboard Pages**<br>
* Introduction: This is the landing page of the site and provides a quick overview of the dashboard contents and navigation.
* Heat Map: Shows pollution across a map of the US, users can select pollutants and time frame as well as having a range of options for the granularity of the data displayed.
* Pollution Over Time: Line plot showing pollution over time, users can select a specific state and/or change time displays to show historical or seasonal trends.
* Tree Map: Provides an overview of pollution levels across States, Counties and Cities, users can select which pollutant to visualise.

**Communication of data insights**
* How were data insights communicated to technical and non-technical audiences?
* Explain how the dashboard was designed to communicate complex data insights to different audiences.

## Conclusions and Next Steps

## Unfixed Bugs
* Please mention unfixed bugs and why they were not fixed. This section should include shortcomings of the frameworks or technologies used. Although time can be a significant variable to consider, paucity of time and difficulty understanding implementation are not valid reasons to leave bugs unfixed.
* Did you recognise gaps in your knowledge, and how did you address them?

## Development Roadmap
* What challenges did you face, and what strategies were used to overcome these challenges?
* What new skills or tools do you plan to learn next based on your project experience? 

## Deployment
### Heroku

* The App live link is: https://YOUR_APP_NAME.herokuapp.com/ 
* Set the runtime.txt Python version to a [Heroku-20](https://devcenter.heroku.com/articles/python-support#supported-runtimes) stack currently supported version.
* The project was deployed to Heroku using the following steps.

1. Log in to Heroku and create an App
2. From the Deploy tab, select GitHub as the deployment method.
3. Select your repository name and click Search. Once it is found, click Connect.
4. Select the branch you want to deploy, then click Deploy Branch.
5. The deployment process should happen smoothly if all deployment files are fully functional. Click now the button Open App on the top of the page to access your App.
6. If the slug size is too large then add large files not required for the app to the .slugignore file.


## Main Data Analysis Libraries
* Here you should list the libraries you used in the project and provide an example(s) of how you used these libraries.


## Credits 

* In this section, you need to reference where you got your content, media and extra help from. It is common practice to use code from other repositories and tutorials, however, it is important to be very specific about these sources to avoid plagiarism. 
* You can break the credits section up into Content and Media, depending on what you have included in your project. 

### Content 

- The text for the Home page was taken from Wikipedia Article A
- Instructions on how to implement form validation on the Sign-Up page was taken from [Specific YouTube Tutorial](https://www.youtube.com/)
- The icons in the footer were taken from [Font Awesome](https://fontawesome.com/)

### Media

- The photos used on the home and sign-up page are from This Open-Source site
- The images used for the gallery page were taken from this other open-source site



## Acknowledgements (optional)
* Thank the people who provided support through this project.

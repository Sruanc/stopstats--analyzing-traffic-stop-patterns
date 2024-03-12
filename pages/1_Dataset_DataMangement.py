import streamlit as st

def main():
    # Set page title and subtitle
    st.title("Dataset and Data Management Plan")
 
    st.subheader("Dataset")
    # Add introduction text
    st.write("Two data sources are used for this project. The Stanford Open Policing Project compiled traffic stop information from police departments across the country. The attributes reported vary from one police department to another; for this project we have focused on data from the Washington State Patrol. Due to the high number of traffic stops included in the dataset, we have restricted our analysis to traffic stops made in 2018, the most recent year provided in the dataset. The second data source used is the U.S. Census Bureau’s American Community Survey (ACS). Data was queried using the ACS API. Key demographic variables were collected for Washington state using 2018 5-year estimates at the census tract level.")
    
    # Add section for Stanford Open Policing Project
    st.subheader("1 Stanford Open Policing Project")
    st.write("The Stanford Open Policing Project compiled traffic stop information from police departments across the country. For this project, we focused on data from the Washington State Patrol in 2018. The dataset includes various attributes such as stop date and time, location coordinates, subject age, race, sex, search conducted, and outcomes such as citations or warnings issued.")
    
    # Add section for U.S. Census Bureau's ACS
    st.subheader("2 U.S. Census Bureau's American Community Survey (ACS)")
    st.write("Data from the ACS was queried using the ACS API, specifically 2018 5-year estimates at the census tract level. Key demographic variables such as population demographics, median age, income, and education level were collected for Washington state.")
    
    # Add section for data merging and preprocessing
    st.subheader("Data Merging and Preprocessing")
    st.write("The traffic stops data and the census tract data were merged using a spatial join, based on the latitudes and longitudes of the traffic stops and the shapefiles of the census tracts. Assumptions were made regarding the relationship between traffic stops and census tracts, and a relational schema was designed to manage the data.")
    st.subheader("Assumptions")
    st.write("- There can be many police stops happening in many census tracts.")
    st.write("- A police stop must happen in a census tract.")
    st.write("- A census tract does not need to have a police stop happen in it.")
    st.write("- There can be multiple stops occurring at the same DateTime and the same Latitude and Longitude (e.g. each person at a multi-subject stop is a unique entity in the PoliceStops entity set, with each entity at the same time and place).")
    
    st.write("The relational schema for the E/R diagram (presented in Figure below) is:")
    st.write("- TrafficStops(StopID, DateTime, Latitude, Longitude, SubjectAge, SubjectRace, SubjectSex, SearchConducted, FriskPerformed, ContrabandFound, CitationIssued, WarningIssued, Outcome)")
    st.write("- CensusTracts(TractID, TotalPopulation, %White, %Black, %Hispanic, %AAPI, %Other, %BIPOC, MedianAge, MedianIncome, %Male, %CollegeEducated)")
    st.write("- HappenIn(TrafficStops.StopID, CensusTracts.TractID)")
  
    image_url = 'pages/CET_522_P2_E_R_Diagram.jpg'
    # image_url = 'E_R_Diagram.png'

    st.image(image_url, caption="E/R Diagram for the Database Design", use_column_width=True)
    # st.image(image, caption="E/R Diagram for the Database Design", use_column_width=True)
    st.write("Some pre-processing was done on the data for the scatterplot analysis. The traffic stops data was aggregated by census tract, and a normalized count was performed to obtain the percentage of traffic stop subjects by each race, and by each stop activity (e.g. search, frisk, etc.) within each census tract.")

    # Add section for limitations
    st.subheader("Limitations")
    st.write("One limitation of the dataset is that Washington State Patrol generally performs traffic stops on highways, which may not be as representative of the population of the tract where the stop occurred compared to stops performed by local police departments on non-highway roads and streets. Additionally, a significant portion of our geospatial analysis was performed via Folium. Folium had limited computational efficiency to plot large datasets, so we chose to limit the data scope for the sake of improved dashboard performance. For the mapping portion, data was reduced to only include census tracts and police stops in King County. We randomly sampled n = 10,000 points from the police stops within King County, which was 20.52% of the King County police stops. Subsequent analysis and visualizations will use this reduced sample.")
    
    # Add references
    st.subheader("References")
    st.write("The Stanford Open Policing Project. (2020). The Stanford Open Policing Project. [Link](https://openpolicing.stanford.edu/)")
    st.write("United States Census Bureau. (2023). American Community Survey Data. [Link](https://www.census.gov/programs-surveys/acs/data.html)")
    
if __name__ == "__main__":
    main()

import streamlit as st

def main():
    st.title('Washington State Police Stops Analysis')
    st.write('## Introduction')
    st.write("Welcome to our Streamlit app, where we analyze spatiotemporal relationships within Washington State Patrol stops and explore potential racial disparities. Our study focuses on understanding patterns of police stops and their implications for racial equity in law enforcement.")

    st.write('## Key Findings')
    st.write('- **Spatiotemporal Patterns:** Police stops predominantly occur along major roadways such as I-5 and I-90, with the highest concentration observed in the Sodo neighborhood of Seattle.')
    st.write('- **Demographic Insights:** The Sodo neighborhood, characterized by a disproportionately high male population and a moderate BIPOC presence, experiences a significant number of police stops.')
    st.write('- **Racial Disparities:** Analysis reveals that census tracts with higher Black populations tend to experience more police stops by the Washington State Patrol.')
    st.write('- **Stop Activity:** Interestingly, no significant relationship was found between the type of stop activity and race.')

    st.write('## Implications')
    st.write('Our findings underscore the need for proactive measures to address racial disparities in law enforcement practices. By leveraging this data, policymakers and law enforcement agencies can develop targeted interventions to mitigate bias and promote equitable policing.')

    st.write('## Future Directions')
    st.write('- **Enhanced Functionality:** We aim to enhance the functionality of our app by incorporating additional years of data and expanding our analysis to include more police departments across the state.')
    st.write('- **Monitoring Police Reform:** Continued analysis will allow us to monitor the effectiveness of police reform efforts, particularly in response to the George Floyd tragedy, and assess whether new strategies are reducing racial bias in policing.')

    st.write('## References')
    st.write('- City of Seattle. (2024). Fighting for Statewide Police Reforms. [Link](https://www.seattle.gov/community-police-commission/our-work/state-legislative-advocacy)')

    st.write('## About Us')
    st.write("This app was developed by [Your Name/Team Name] as part of ongoing research efforts to promote data-driven insights into law enforcement practices and racial equity.")

if __name__ == "__main__":
    main()

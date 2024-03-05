import streamlit as st

st.set_page_config(
    page_title="Traffic Stop Analyzer",
    page_icon="🚓",
)

# Header
st.title("Unveiling Insights: Traffic Stop Analyzer")
st.subheader("Exploring the Dynamics of Traffic Policing through Data")

# Introduction section
st.write("""
Every day, law enforcement officers engage in routine traffic stops, encountering a myriad of drivers on the road. 
These interactions, pivotal in upholding traffic laws, unfold in various contexts, from the reason behind the stop to the subsequent actions taken. 
By delving into the Stanford Open Policing Project's dataset, we uncover a wealth of insights. 
We explore the nuanced relationship between traffic stops, officer-driver interactions, and arrest outcomes across different time and location contexts. 
This examination not only sheds light on disparities and biases within law enforcement practices but also serves as a compass for policymakers and agencies seeking to allocate resources wisely, refine training programs, and foster community relations.
""")

# Content sections
st.write("1. **Location and Timing of Police Stops:** Explore whether police stops are more likely to occur at certain locations or times of day.")
st.write("2. **Demographic Analysis:** Investigate whether there are disproportionate numbers or types of people being stopped based on age, race, and sex.")
st.write("3. **Contraband Found Rates:** Examine which police departments have low contraband found rates and analyze contraband found rates vs. race for each census tract.")


# Source of data
st.write("Data Source: [Stanford Open Policing Project](https://openpolicing.stanford.edu/)")

# Call to action
st.write("Join us on a journey through data-driven analysis as we uncover the intricate dynamics shaping traffic policing today.")

# Additional resources or links (optional)
st.markdown("""
### Want to learn more?
- Check out the [Stanford Open Policing Project](https://openpolicing.stanford.edu/)
- Dive into our [analysis results](#) (replace "#" with our analysis link)
""")

# Footer
st.write("---")
st.write("Developed with ❤️ by Group 8 Sruangsaeng Chaikasetsin, Jeremy Chan, Kaitlyn Ng")
st.write("CET 522 Transportation Data Management and Visualization Winter 2024")
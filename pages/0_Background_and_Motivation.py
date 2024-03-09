import streamlit as st

def main():
    # Set page title and subtitle
    st.title("Analyzing Traffic Police Stops: Background and Motivation")
    st.subheader("Introduction")
    
    # Add introduction text
    st.write("Traffic police stops are routine encounters between law enforcement officers and drivers on the road. These interactions often involve various aspects, such as the reason for the stop, driver behavior, officer actions, and outcomes such as warning or arrest (Disassa & Kebu, 2019). Understanding the correlation between traffic police stops and officer-driver interactions, as well as characteristics of the stopped subject, can provide valuable insights into law enforcement practices. Furthermore, correlations between stop locality and timing may also shed light on potential biases in traffic stops. Understanding these correlations can help policymakers and law enforcement agencies make informed decisions regarding resource allocation, training programs, and strategies to improve community relations (Chainey et al., 2022).")
    
    st.subheader("Research Question")
    
    # Add research question
    st.write("The research question this project poses is, to what extent do time of day and location correlate with traffic stops made by Washington State Patrol in 2018? Also, do racial disparities exist in the frequency of traffic stops being made, and the officer activities that occur during a traffic stop? Uncovering and understanding the nature of biases may provide valuable insights into contributing factors to bias, and possibly enlighten strategies for addressing bias.")
    
    st.subheader("References")
    
    # Add references
    st.write("Chainey, S.P., Estévez-Soto, P.R., Pezzuchi, G., and Serrano–Berthet, R. (2023). 'An evaluation of a hot spot policing programme in four Argentinian cities.' The Police Journal: Theory, Practice and Principles, 96, 267–288. [Link](https://doi.org/10.1177/0032258X221079019)")
    st.write("Disassa, A., and Kebu, H. (2019). 'Psychosocial factors as predictors of risky driving behavior and accident involvement among drivers in Oromia Region, Ethiopia.' Heliyon, 5(6). [Link](https://doi.org/10.1016/j.heliyon.2019.e01876)")

if __name__ == "__main__":
    main()

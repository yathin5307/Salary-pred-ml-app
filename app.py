import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def shorten_categories(categories, cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]="other"
    return categorical_map

def clean_exp(x):
    if x=="More than 50 years":
        return 50
    if x=="Less than 1 year":
        return 0.5
    return float(x)

def clean_edu(x):
    if "Bachelor’s degree" in x or "Associate degree" in x:
        return "Under grad"
    if "Master’s degree" in x:
        return "Master's degree"
    if "Professional degree" in x:
        return "Post grad"
    return "Less than a Bachelors"

def show_predict_page():
        st.title("Software developer salary predictor")
    
        st.write(""" ### We need some information to predict the salary""")

        countries = (
            "United States of America",
            "Germany",
            "United Kingdom of Great Britain and Northern Ireland",
            "Canada",
            "India",
            "France",
            "Netherlands",
            "Australia",
            "Brazil",
            "Spain",
            "Sweden",
            "Italy",
            "Poland",
            "Switzerland",
            "Denmark",
            "Norway",
            "Israel"
        )

        education = (
            "Under grad",
            "Less than a Bachelors",
            "Master's degree",
            "Post grad"
        )
    
        country = st.selectbox("Country", countries)
        education = st.selectbox("Education Level", education)
        experience = st.slider("Years of Experience", 0, 50, 3)

        ok=st.button("Calculate Salary")

        if ok:
            X=np.array([[country, education, experience]])
            X[:, 0]=le_country.transform(X[:, 0])
            X[:, 1]=le_education.transform(X[:, 1])
            X=X.astype(float)

            salary=regressor.predict(X)
            st.subheader(f"The estimated salary is ${salary[0]:.2f}")

def show_explore_page():
        st.title("Explore Software Engineer Salaries")
        st.write(""" Developer Survey 2023""")



# Define your load_model function and load the necessary data as you did in your code
data = pickle.load(open('saved_file.pkl','rb'))

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
page=st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))




if page=="Predict":
    show_predict_page()

else:
    show_explore_page()
    
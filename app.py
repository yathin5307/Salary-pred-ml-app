import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

# Currency Conversion Function
def convert_currency(amount, base_currency, target_currency):

    print(target_currency)
    print(amount)
    print(base_currency)
    # Construct the URL with the parameters
    url = f"https://v6.exchangerate-api.com/v6/c0cf612414417e0c16d3433a/pair/{base_currency}/{target_currency}/{amount}"

    # Make a GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
    # Parse the JSON response
        data = response.json()
    
    # Extract the conversion_result
        conversion_result = data.get("conversion_result")
        if conversion_result is not None:
            return conversion_result
        else:
            st.subheader("no conversion result")
            return None
    else:
        st.subheader(f"API request failed with status code: {response.status_code}")
        return None

def get_currency_for_country(country):
    # Define a dictionary to map countries to currencies
    country_to_currency = {
        "United States of America": "USD",
        "Germany": "EUR",
        "United Kingdom of Great Britain and Northern Ireland": "GBP",
        "Canada": "CAD",
        "India": "INR",
        "France": "EUR",
        "Netherlands": "EUR",
        "Australia": "AUD",
        "Brazil": "BRL",
        "Spain": "EUR",
        "Sweden": "SEK",
        "Italy": "EUR",
        "Poland": "PLN",
        "Switzerland": "CHF",
        "Denmark": "DKK",
        "Norway": "NOK",
        "Israel": "ILS"
    }

    # Return the currency for the selected country
    return country_to_currency.get(country, "USD")  # Default to USD if the country is not found in the dictionary


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

            salary1=regressor.predict(X)
            salary = salary1[0]
            # Convert the predicted salary to the user's selected currency
            selected_currency = get_currency_for_country(country)  # Replace with your own function to get the currency for the country
            converted_salary = convert_currency(salary, "USD", selected_currency)

            # Display the converted salary in the user's local currency
            if converted_salary is not None:
                st.subheader(f"Predicted Salary ({selected_currency}): {converted_salary:.2f}")
            else:
                st.subheader(f"The estimated salary is ${salary[0]:.2f}")

def show_explore_page():
        st.title("Explore Software Engineer Salaries")
        st.write(""" Developer Survey 2023""")

        data=df['Country']. value_counts()
        fig1, ax2=plt.subplots()
        data.plot(kind='barh', ax=ax2)
        ax2.set_xlabel('Count')
        ax2.set_ylabel('Country')
        st.write(""" #### Number of data from different countries """)

        st.pyplot(fig1)

        st.write(""" #### Mean salary based on Country """)

        data2=df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
        st.bar_chart(data2)

        st.write(""" #### Mean salary based on Experience """)
        data3=df.groupby(["Experience"])["Salary"].mean().sort_values(ascending=True)
        st.line_chart(data3)


# Define your load_model function and load the necessary data as you did in your code
data = pickle.load(open('saved_file.pkl','rb'))

def load_data():
    df=pd.read_csv("salary.csv")
    df=df[["Country", "EdLevel", "Experience", "Salary"]]
    df=df[df["Salary"].notnull()]
    df=df.dropna()

    country_map=shorten_categories(df.Country.value_counts(), 400)
    df['Country']=df['Country'].map(country_map)
    df=df[df['Salary']<=200000]
    df=df[df['Salary']>=10000]
    df=df[df['Country']!='Other']

    df['Experience']=df['Experience'].apply(clean_exp)
    df['EdLevel']=df['EdLevel'].apply(clean_edu)
    return df

df=load_data()
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
page=st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))




if page=="Predict":
    show_predict_page()

else:
    show_explore_page()
    
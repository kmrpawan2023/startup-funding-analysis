import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Startup Analysis')
df = pd.read_csv('startup_cleaned')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis():
    st.title("Overall Analysis")

    # total amount
    total_amount = round(df['amount in crore'].sum())
    st.metric("Total Amount Funded Till Now", str(total_amount) + 'cr')

    # max amount infused in company
    max_amount = df.groupby("startup")['amount in crore'].max().sort_values(ascending=False).head(1).values[0]
    st.metric("maximum amount in a Company", str(max_amount) + 'cr')

    avg = round(df.groupby("startup")['amount in crore'].sum().mean())
    st.metric("Average funding in India", str(avg) + 'cr')

    # total funded startups
    num_startups = df['startup'].nunique()
    st.metric("Funded Startups", str(num_startups) + 'cr')

    st.header('MoM graph(month on month)')
    selected_option = st.selectbox("Select Type", ['Total', 'Count'])
    if selected_option == 'Total':

        temp_df = df.groupby(['year', 'month'])['amount in crore'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount in crore'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype("str")
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount in crore'])
    st.pyplot(fig5)


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'industry', 'city', 'amount in crore']]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_invest = df[df['investors'].str.contains(investor)].groupby('startup')['amount in crore'].sum().sort_values(
            ascending=False).head()
        st.subheader("Biggest Investments")
        fig, ax = plt.subplots()
        ax.bar(big_invest.index, big_invest.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('startup')[
            'amount in crore'].sum().sort_values(
            ascending=False).head()
        st.subheader("Sectors Invested in")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%0.01f%%')
        st.pyplot(fig1)

    col1, col2 = st.columns(2)
    with col1:
        # type of company
        companies_type = df[df['investors'].str.contains(investor)].groupby('round')[
            'amount in crore'].sum().sort_values(
            ascending=False).head(5)
        st.subheader("Type of Company")
        fig2, ax2 = plt.subplots()
        ax2.pie(companies_type, labels=companies_type.index, autopct='%0.01f%%')
        st.pyplot(fig2)
    with col2:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount in crore'].sum().sort_values(
            ascending=False).head()
        st.subheader("Cities Invested in")
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount in crore'].sum()
    st.subheader("Year on Year Investment")
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)


st.sidebar.title('Startup funding Analysis')
option = st.sidebar.selectbox('Select one', ['Overall Analysis', 'Startups', 'Investor'])

if option == 'Overall Analysis':

    load_overall_analysis()



elif option == 'Startups':
    st.sidebar.selectbox('Select startups', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investors', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor name")
    if btn2:
        load_investor_details(selected_investor)

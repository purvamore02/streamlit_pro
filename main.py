import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

df = pd.read_csv("startup_cleaned.csv")
st.set_page_config(layout='wide', page_title='Startup Analysis')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

st.header('Purva More')
st.header('FS23AI012')

def load_investor_details(investor):
    st.title(investor)
    st.subheader('Most Recent Investments')
    last5_df = df[df['investors'].str.contains(investor, na=False)].head(5)[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5_df)
    st.subheader('Maximum Investment')
    last5_dff = df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(
        ascending=False).head(1)
    st.dataframe(last5_dff)

    col1, col2, col3 = st.columns(3)
    with col1:
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_serial = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Invested sectors')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_serial, labels=vertical_serial.index, autopct="0.01f%%")

        st.pyplot(fig1)

    with col3:
        # Corrected the line below, changed square brackets to parentheses
        city = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
        st.subheader('City')
        fig2, ax2 = plt.subplots()
        ax2.pie(city, labels=city.index)

        st.pyplot(fig2)

    sub1 = df[df['investors'].str.contains(investor, na=False)].groupby('subvertical')['amount'].sum()
    col1.subheader('Subvertical')
    fig3, ax3 = plt.subplots()
    ax3.bar(sub1.index, sub1.values)
    col1.pyplot(fig3)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    sub2 = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
    col2.subheader('Yearly Invested')
    fig2, ax2 = plt.subplots()
    ax2.plot(sub2.index, sub2.values)
    col2.pyplot(fig2)


    round = df[df['investors'].str.contains('3one4 Capital', na=False)].groupby('round')['amount'].sum()
    col3.subheader('Rounded')
    fig3, ax3 = plt.subplots()
    ax3.bar(round.index, round.values)
    col3.pyplot(fig3)


def overall():
    st.title('Overall Analysis')

    total = round(df['amount'].sum())
    #max amount
    maximum_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    average_funding = df.groupby('startup')['amount'].sum().mean()
    number_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + 'Cr')
    with col2:
        st.metric('Max',str(maximum_funding)+'Cr')
    with col3:
        st.metric('Avg',str(round(average_funding))+'Cr')

    with col4:
        st.metric('Founded Startup',number_startups)


    st.header('MoM Chart')
    selected_option = st.selectbox('select type',[' Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3,ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])

    st.pyplot(fig3)

    st.header('Sector Analysis')
    st.subheader("Top 3 Industries")
    top_verticals = df['vertical'].value_counts().head(3)
    fig, ax = plt.subplots()
    top_verticals.plot(kind='pie', ax=ax)
    st.pyplot(fig)



    st.header('City Funding')
    # Group by city and sum the investment amounts, filling missing values with 0
    investment_city = df.groupby('city')['amount'].sum().fillna(0)
    # Sorting the result by total investment amount
    investment_city = investment_city .sort_values(ascending=False)
    # Resetting index to make city a column again
    investment_city = investment_city .reset_index()


    # Streamlit code
    st.subheader('Total Invested by City')
    # Plotting a pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(investment_city ['amount'], labels=investment_city ['city'], autopct='%1.1f%%')
    ax.set_title('Total Invested by City')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Displaying the plot
    st.pyplot(fig)
    # Group by investors and find the maximum investment amount for each investor

    df['date'] = pd.to_datetime(df['date'])

    # Extract year from the date column
    df['year'] = df['date'].dt.year

    # Group by year and startup, summing the investment amounts, and finding the top startup each year
    top_yearly = df.groupby(['year'])['startup'].agg(lambda x: x.value_counts().idxmax()).reset_index()


    # bar graph
    st.title('Top Startup Year Overall')
    # Plotting a bar graph
    fig, ax = plt.subplots()
    ax.bar( top_yearly['year'],  top_yearly['startup'], color='skyblue')
    ax.set_xlabel('Year')
    ax.set_ylabel('Top Startup')
    ax.set_title('Top Startup Each Year Overall')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    # Displaying the plot
    st.pyplot(fig)


    st.title("Top Investors")
    # Aggregate investment amounts for each investor
    total_investor = df.groupby('investors')['amount'].sum().reset_index()
    # Rank investors based on total investment amount
    total_investor = total_investor.sort_values(by='amount', ascending=False)
    # Select top investors (e.g., top 10)
    top_investors = total_investor.head(10)
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(top_investors['amount'], labels=top_investors['investors'], autopct='%1.1f%%')
    ax.set_title('Top Investors')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart using Streamlit
    st.pyplot(fig)

    st.subheader('Funding Heatmap')
    heatmap_data = df.pivot_table(values='amount', index='year', columns='month', aggfunc='sum')
    fig10, ax10 = plt.subplots()
    cax = ax10.matshow(heatmap_data, cmap='viridis')
    fig10.colorbar(cax)
    ax10.set_xticks(range(len(heatmap_data.columns)))
    ax10.set_xticklabels(heatmap_data.columns, rotation=45)
    ax10.set_yticks(range(len(heatmap_data.index)))
    ax10.set_yticklabels(heatmap_data.index)
    st.pyplot(fig10)





import matplotlib.pyplot as plt

def startup_details(startup):
    st.header('Founders:')
    # Filter the DataFrame to select rows where the 'startup' column
    old_dataframe = df[df['startup'] == startup]
    # Print the names of investors in the startup
    int1 = old_dataframe['investors']
    # Create a DataFrame from the 'investors' column
    investors = pd.DataFrame(int1, columns=['investors']).reset_index()
    # Display the DataFrame
    st.write(investors)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Industries invested in:')
        filtered_dataframe = df[df['startup'].str.contains(startup, na=False)].dropna(subset=['vertical']).drop_duplicates(
            subset=['vertical'])

        # Resetting the index and printing only the 'lndustry' values
        a = filtered_dataframe.reset_index(drop=True)['vertical'].tolist()
        for i in a:
            st.write(i)

    with col2:
        st.subheader('Sub-Industries invested in:')
        filtered_dataframe = df[df['startup'].str.contains(startup, na=False)].dropna(subset=['subvertical']).drop_duplicates(
            subset=['subvertical'])

        # Resetting the index and printing only the 'Sublndustry' values
        a = filtered_dataframe.reset_index(drop=True)['subvertical'].tolist()
        for i in a:
            st.write(i)

    with col3:
        st.subheader('Cities invested in:')
        filtered_dataframe = df[df['startup'].str.contains(startup, na=False)].dropna(subset=['city']).drop_duplicates(
            subset=['city'])

        # Resetting the index and printing only the 'city' values
        a = filtered_dataframe.reset_index(drop=True)['city'].tolist()
        for i in a:
            st.write(i)


    col1, col2 = st.columns(2)

    with col1:
        st.title('Industry')
        industry_data = df[df['startup'].str.contains(startup, na=False)]['vertical'].str.lower().value_counts().head()

        # Create a pie chart for 'Industry'
        fig_industry, ax_industry = plt.subplots()
        ax_industry.pie(industry_data, labels=industry_data.index, autopct='%1.1f%%', startangle=90)
        ax_industry.set_title('Industry Distribution')

        # Display the pie chart using Streamlit
        st.pyplot(fig_industry)

    with col2:
        st.title('Sub-Industry')
        sub_industry_data = df[df['startup'].str.contains(startup, na=False)]['subvertical'].str.lower().value_counts().head()

        # Create a pie chart for 'Sub-Industry'
        fig_subindustry, ax_subindustry = plt.subplots()
        ax_subindustry.pie(sub_industry_data, labels=sub_industry_data.index, autopct='%1.1f%%', startangle=90)
        ax_subindustry.set_title('Sub-Industry Distribution')

        # Display the pie chart using Streamlit
        st.pyplot(fig_subindustry)

    # 'City' section as pie chart
    st.title('City')
    city_data = df[df['startup'].str.contains(startup, na=False)].groupby('startup')['city'].value_counts().head()

    # Create a pie chart for 'City'
    fig_city, ax_city = plt.subplots()
    ax_city.pie(city_data, labels=city_data.index, autopct='%1.1f%%', startangle=90)
    ax_city.set_title('City Distribution')

    # Display the pie chart using Streamlit
    st.pyplot(fig_city)

    st.header('Funding Rounds')
    funding_rounds_info = df[['round', 'investors', 'date']].sort_values('date', ascending=False)
    st.dataframe(funding_rounds_info)



# st.dataframe(df)
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    overall()


elif option == 'Startup':
    st.title("Startup Analysis")
    select_start=selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(df['startup'].astype(str).str.split(',').sum())))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        st.title(select_start)
        startup_details(select_start)


else:
    st.title('Investor')
    selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)

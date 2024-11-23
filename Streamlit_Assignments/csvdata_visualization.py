import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("VISUALIZATION OF CSV DATA")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.write(df.head())
    
    limited_df = df.head(100)

    st.sidebar.header("Select Visualization Settings")
    chart_type = st.sidebar.selectbox(
        "Select Chart Type",
        ["Line Chart", "Bar Chart", "Histogram", "Scatter Plot", "Pie Chart"]
    )
    
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()

    if chart_type == "Pie Chart":
        if len(categorical_columns) == 0:
            st.warning("The uploaded file has no categorical columns for a pie chart.")
        else:
            column = st.sidebar.selectbox("Select Column for Pie Chart", categorical_columns)
            if column:
                pie_data = df[column].value_counts()
                fig, ax = plt.subplots()
                ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
    elif len(numeric_columns) == 0:
        st.warning("The uploaded file has no numeric columns for visualization.")
    else:
        if chart_type in ["Line Chart", "Bar Chart", "Histogram"]:
            column = st.sidebar.selectbox("Select Column", numeric_columns)
        elif chart_type == "Scatter Plot":
            x_col = st.sidebar.selectbox("Select X-axis Column", numeric_columns)
            y_col = st.sidebar.selectbox("Select Y-axis Column", numeric_columns)

        st.write(f"### {chart_type} (First 100 Samples)")
        
        if chart_type == "Line Chart":
            st.line_chart(limited_df[column])
        elif chart_type == "Bar Chart":
            st.bar_chart(limited_df[column])
        elif chart_type == "Histogram":
            fig, ax = plt.subplots()
            sns.histplot(limited_df[column], kde=True, ax=ax)
            st.pyplot(fig)
        elif chart_type == "Scatter Plot":
            fig, ax = plt.subplots()
            sns.scatterplot(x=limited_df[x_col], y=limited_df[y_col], ax=ax)
            st.pyplot(fig)

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO

# Sample data generation (for testing)
def generate_sample_data(num_records=1000):
    """Generate sample fraud detection data for visualization."""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=num_records)
    data = {
        'date': np.random.choice(dates, num_records),
        'risk_level': np.random.choice(['Low', 'Medium', 'High'], num_records),
        'amount': np.random.randint(1, 1000, num_records),
        'location': np.random.choice(['Location A', 'Location B', 'Location C'], num_records)
    }
    return pd.DataFrame(data)

# Load data (replace this with actual data loading logic)
df = generate_sample_data()

# Streamlit UI
st.title("Fraud Analytics & Visualization Module")

# Sidebar for filtering
st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start Date", value=datetime(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", value=datetime(2023, 12, 31))
risk_level = st.sidebar.multiselect("Select Risk Levels", options=['Low', 'Medium', 'High'], default=['Low', 'Medium', 'High'])
filtered_data = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date)) & (df['risk_level'].isin(risk_level))]

# Display filtered data
st.subheader("Filtered Fraud Data")
st.write(filtered_data)

# Visualizations
st.subheader("Fraud Detection Analytics")

# Time Series Plot
time_series_fig = px.line(filtered_data.groupby('date').size().reset_index(name='counts'), x='date', y='counts', title='Fraud Incidents Over Time')
st.plotly_chart(time_series_fig)

# Risk Level Distribution
risk_level_counts = filtered_data['risk_level'].value_counts()
st.bar_chart(risk_level_counts)

# Heatmap of Fraud by Location and Risk Level
heatmap_data = filtered_data.groupby(['location', 'risk_level']).size().unstack(fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu')
plt.title("Heatmap of Fraud by Location and Risk Level")
st.pyplot(plt)

# NLP Component for Summarization
def summarize_fraud_trends(data):
    """Summarize trends based on the filtered data (mock example)."""
    trends = {
        'Total Incidents': len(data),
        'Total Amount Lost': data['amount'].sum(),
        'Most Frequent Risk Level': data['risk_level'].mode()[0],
        'Top Location': data['location'].mode()[0]
    }
    return trends

trends_summary = summarize_fraud_trends(filtered_data)

# Display trends summary
st.subheader("Fraud Trends Summary")
st.write(trends_summary)

# Generate a report (optional download)
report_buffer = BytesIO()
with pd.ExcelWriter(report_buffer, engine='xlsxwriter') as writer:
    filtered_data.to_excel(writer, sheet_name='Filtered Data')
    writer.sheets['Filtered Data'].insert_chart('E2', time_series_fig)
    writer.sheets['Filtered Data'].insert_chart('E20', risk_level_counts)
    writer.sheets['Filtered Data'].insert_chart('E40', heatmap_data)

report_buffer.seek(0)

st.download_button(label="Download Fraud Report", data=report_buffer, file_name='fraud_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


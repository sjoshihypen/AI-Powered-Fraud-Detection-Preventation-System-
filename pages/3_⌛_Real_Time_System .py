import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration
st.set_page_config(page_title="Real-Time Transaction Monitoring", layout="wide")

# Header
st.title("Real-Time Transaction Monitoring System")
st.markdown("## Monitoring Transactions in real-time & detecting suspicious activities using anomaly detection models.")

# Sidebar options
st.sidebar.header("Simulation Settings")
n_transactions = st.sidebar.slider("Number of transactions to simulate", 10, 1000, step=10, value=50)
anomaly_ratio = st.sidebar.slider("Anomaly ratio (%)", 0, 20, step=1, value=5)

# Simulate transaction data
def generate_transaction_data(n, anomaly_ratio):
    np.random.seed(42)
    
    # Calculate the number of normal and anomalous transactions
    n_normal = max(1, int(n * (1 - anomaly_ratio / 100)))  # Ensure at least 1 normal transaction
    n_anomalous = max(0, n - n_normal)  # Calculate remaining as anomalous transactions
    
    # Normal transactions (values around 100, low variance)
    normal_data = np.random.normal(loc=100, scale=10, size=(n_normal, 2))
    
    # Anomalous transactions (values significantly higher)
    anomalous_data = np.random.normal(loc=300, scale=50, size=(n_anomalous, 2))
    
    # Combine normal and anomalous data
    data = np.vstack([normal_data, anomalous_data])
    np.random.shuffle(data)
    
    return pd.DataFrame(data, columns=["Transaction_Amount", "Transaction_Frequency"])

# Function to detect anomalies using Isolation Forest
def detect_anomalies(data):
    if len(data) > 1:
        model = IsolationForest(contamination=anomaly_ratio / 100, random_state=42)
        data['anomaly'] = model.fit_predict(data[['Transaction_Amount', 'Transaction_Frequency']])
        data['anomaly'] = data['anomaly'].apply(lambda x: 1 if x == -1 else 0)  # 1: Anomaly, 0: Normal
    else:
        # If there is only one transaction, we can't run IsolationForest, so mark it as normal
        data['anomaly'] = 0
    return data

# Streaming simulation
placeholder = st.empty()

if st.sidebar.button("Start Simulation"):
    st.sidebar.write("Simulation in progress...")
    for i in range(1, n_transactions + 1):
        # Simulate incoming transactions one by one
        data = generate_transaction_data(i, anomaly_ratio)
        
        # Apply anomaly detection
        data = detect_anomalies(data)
        
        # Visualize results
        with placeholder.container():
            st.subheader(f"Transaction {i} / {n_transactions}")
            
            # Display transaction data
            st.write(data.tail(5))  # Show last 5 transactions
            
            # Plot transaction data with anomalies highlighted
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=data, x="Transaction_Amount", y="Transaction_Frequency", hue="anomaly", palette={0: "blue", 1: "red"}, ax=ax)
            ax.set_title("Transaction Data (Red: Anomaly)")
            st.pyplot(fig)
            
            # Provide real-time alert if anomaly detected
            if data['anomaly'].iloc[-1] == 1:
                st.warning("🚨 Anomaly detected in the latest transaction!")
            
        time.sleep(0.5)  # Simulate time delay for real-time monitoring
    st.sidebar.write("Simulation completed.")


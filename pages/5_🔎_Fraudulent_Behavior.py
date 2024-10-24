import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Streamlit app
st.title("Fraudulent Behavior Prediction Module")

# File uploader to load past transaction data
uploaded_file = st.file_uploader("Upload your transaction data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Load data
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())

    # Assuming 'Amount' and 'Fraud' are columns in your dataset
    if 'Amount' in data.columns and 'Fraud' in data.columns:
        # Preprocessing
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data[['Amount']].values)

        # Prepare data for LSTM
        def create_dataset(data, time_step=1):
            X, y = [], []
            for i in range(len(data) - time_step - 1):
                a = data[i:(i + time_step), 0]
                X.append(a)
                y.append(data[i + time_step, 0])
            return np.array(X), np.array(y)

        time_step = 10  # Number of time steps
        X, y = create_dataset(scaled_data, time_step)
        X = X.reshape(X.shape[0], X.shape[1], 1)

        # Split data into training and testing
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # Build LSTM model
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)

        # Predict future fraud probabilities
        predictions = model.predict(X_test)
        predictions = scaler.inverse_transform(predictions)

        # Plotting results
        plt.figure(figsize=(12, 6))
        plt.plot(data.index[len(data) - len(predictions):], predictions, color='red', label='Predicted Fraud Probability')
        plt.plot(data['Amount'], color='blue', label='Actual Amounts')
        plt.title('Fraudulent Behavior Prediction')
        plt.xlabel('Time')
        plt.ylabel('Transaction Amount')
        plt.legend()
        st.pyplot(plt)

        # Risk analysis output
        future_fraud_probability = predictions[-1][0]  # Latest prediction
        st.write(f"Predicted future fraud probability: {future_fraud_probability:.2f}")
    else:
        st.error("The dataset must contain 'Amount' and 'Fraud' columns.")
else:
    st.info("Please upload a CSV file containing transaction data.")

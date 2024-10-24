import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

st.set_page_config(
    layout="wide",
    page_title="Fraud | AI",
    page_icon="images/main.jpg"
    )

# Set up Streamlit app
st.title("Fraud Pattern Detection System")
st.write("""
This application allows users to upload datasets (transactional or otherwise) 
and use Machine Learning models to detect fraudulent patterns.
""")

# File uploader for dataset
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type="csv")

# Function to preprocess data
def preprocess_data(df):
    st.write("Original Dataset")
    st.write(df.head())
    
    # Handling missing values (if any)
    df = df.dropna()
    
    # Encoding categorical variables (if any)
    if 'TransactionLocation' in df.columns:
        label_encoder = LabelEncoder()
        df['TransactionLocation'] = label_encoder.fit_transform(df['TransactionLocation'])
    
    # Separating features and target (assuming 'Class' as the target label for fraud detection)
    if 'Class' in df.columns:
        X = df.drop('Class', axis=1)
        y = df['Class']
    else:
        st.error("Dataset must have a 'Class' column representing fraudulent or non-fraudulent transactions.")
        return None, None

    # Scaling the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y

# K-Means Clustering for Fraud Detection
def kmeans_clustering(X):
    kmeans = KMeans(n_clusters=2, random_state=42)
    clusters = kmeans.fit_predict(X)
    
    # Adding cluster results to the original dataset
    return clusters

# Random Forest Classifier for Fraud Detection
def random_forest_classifier(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    
    st.write("### Random Forest Classifier Results")
    st.write("Confusion Matrix:")
    st.write(confusion_matrix(y_test, y_pred))
    
    # Create a table for classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.write("Classification Report (Table Format):")
    st.dataframe(report_df)
    
    return y_test, y_pred

# SVM Classifier for Fraud Detection
def svm_classifier(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train, y_train)
    
    y_pred = svm_model.predict(X_test)
    
    st.write("### SVM Classifier Results")
    st.write("Confusion Matrix:")
    st.write(confusion_matrix(y_test, y_pred))
    
    # Create a table for classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.write("Classification Report (Table Format):")
    st.dataframe(report_df)
    
    return y_test, y_pred

# Visualization function for confusion matrix
def plot_confusion_matrix(cm, title):
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, annot_kws={"size": 16})
    plt.title(title, fontsize=16)
    plt.xlabel('Predicted', fontsize=14)
    plt.ylabel('True', fontsize=14)
    st.pyplot(plt)

# Main function to control the flow
if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file)
    
    # Preprocess the dataset
    X, y = preprocess_data(df)
    
    if X is not None and y is not None:
        # Select model
        model_choice = st.selectbox("Select Model for Fraud Detection", 
                                    ("K-Means Clustering", "Random Forest", "SVM"))
        
        if model_choice == "K-Means Clustering":
            clusters = kmeans_clustering(X)
            df['Cluster'] = clusters
            st.write("### Clustering Results")
            st.write(df.head())
            
            # Visualize the clusters
            st.write("### Cluster Distribution")
            sns.countplot(x=clusters, palette="coolwarm")
            plt.title('K-Means Clustering Results')
            plt.xlabel('Cluster')
            plt.ylabel('Count')
            st.pyplot(plt)
            
            # Pairplot of Clusters
            st.write("### Pairplot of Clusters")
            sns.pairplot(df, hue='Cluster', palette="coolwarm")
            st.pyplot(plt)
        
        elif model_choice == "Random Forest":
            y_test, rf_pred = random_forest_classifier(X, y)
            
            # Plot confusion matrix
            rf_cm = confusion_matrix(y_test, rf_pred)
            plot_confusion_matrix(rf_cm, "Random Forest Confusion Matrix")
        
        elif model_choice == "SVM":
            y_test, svm_pred = svm_classifier(X, y)
            
            # Plot confusion matrix
            svm_cm = confusion_matrix(y_test, svm_pred)
            plot_confusion_matrix(svm_cm, "SVM Confusion Matrix")

else:
    st.write("Please upload a CSV file for analysis.")

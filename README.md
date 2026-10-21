# Northeast India Landslide Risk Prediction
A machine-learning project that estimates landslide risk using geographic, weather, and seasonal features. It compares Logistic Regression, Random Forest, and Gradient Boosting, with a Streamlit dashboard and saved model artifacts for the prediction workflow.
Important: This is an educational/experimental prediction project, not an official early-warning system. Predictions should not be used as the sole basis for safety or emergency decisions.

Table of Contents
- Overview
- Objectives
- Features
- Technology Stack
- Workflow
- Dataset and Input Features
- Model Performance
- Random Forest Confusion Matrix
- Installation
- Run the Application
- Example Prediction
- Limitations
- Future Improvements

## Overview
Landslides are a significant natural hazard in Northeast India. This project explores the use of machine learning to estimate landslide risk from selected geographic, weather, and seasonal variables.

The workflow combines a trained classification model, saved model artifacts, weather-stream data handling, and a Streamlit interface. PySpark is part of the project's data-processing/streaming technology stack.

## Objectives
- Build a machine-learning prototype for landslide risk prediction.
- Compare multiple classification algorithms using evaluation metrics.
- Explore geographic, weather, and seasonal input features.
- Present predictions through a dashboard.
- Examine model feature importance to understand which inputs influence model splits.

## Features
- Comparison of Logistic Regression, Random Forest, and Gradient Boosting.
- Random Forest model artifact saved for reuse.
- Geographic inputs: latitude and longitude.
- Weather inputs: rainfall, temperature, and humidity.
- Seasonal input: month.
- Streamlit dashboard for prediction exploration.
- JSON file used in the weather-stream workflow.
- Northeast India location context, including Itanagar, Dispur, Agartala, Aizawl, Gangtok, Imphal, Kohima, and Shillong.
Weather-data note: Describe the feed as live only if the current code retrieves fresh observations from a configured external source. If it reads a local JSON file or sample data, describe it as local weather-stream/sample data.

## Technology Stack
Technology	Purpose
Python	Main programming language
scikit-learn	Model training and evaluation
Random Forest	Best-performing model in the reported comparison
Logistic Regression	Baseline classifier
Gradient Boosting	Comparison classifier
PySpark	Data processing / streaming workflow
Streamlit	Interactive dashboard
JSON	Local weather-stream data format

## Weather Data Integration

This project uses the [Open-Meteo API](https://open-meteo.com/) to retrieve weather data for selected locations. Temperature, humidity, and rainfall data can be used as inputs for landslide risk prediction.

## Workflow

Geographic + weather + seasonal features
(latitude, longitude, rainfall, temperature,
humidity, month)
                  |
                  v
          Input preparation
                  |
                  v
       Trained classification model
                  |
                  v
       Predicted class / risk score
                  |
                  v
        Streamlit dashboard
1. Prepare location and environmental inputs.
2. Ensure input columns and order match the model's training features.
3. Load the trained model and its feature metadata.
4. Generate a prediction from the prepared input.
5. Display the result in the dashboard.
The precise meaning of each class, risk threshold, and score should be documented according to the implementation.

## Dataset and Input Features

The model uses these six input features:
Feature	Description
latitude	Latitude of the selected location
longitude	Longitude of the selected location
rainfall_mm	Rainfall amount in millimetres
temperature_c	Temperature in degrees Celsius
humidity_percent	Relative humidity percentage
month	Month number used to represent seasonal patterns


Add the original dataset source, collection period, total row count, and class balance here before publishing. These details were not included in the evaluation output provided.

## Model Performance
Three classification algorithms were evaluated on a reported test set of 101 samples.

Model	Accuracy	Precision	Recall	F1-Score	ROC-AUC
Logistic Regression	69.31%	65.57%	80.00%	72.07%	76.04%
Random Forest	80.20%	77.78%	84.00%	80.77%	87.76%
Gradient Boosting	74.26%	71.43%	80.00%	75.47%	85.29%


## Best-performing model
Random Forest achieved the highest accuracy, F1-score, and ROC-AUC in this comparison. Its reported results were:
- Accuracy: 80.20%
- Precision: 77.78%
- Recall: 84.00%
- F1-score: 80.77%
- ROC-AUC: 87.76%
These are results on the reported test split. They do not guarantee the same performance on new locations, future weather, or real-world events.
Random Forest Confusion Matrix

	Predicted class 0	Predicted class 1
Actual class 0	39	12
Actual class 1	8	42


The model correctly classified 39 class 0 samples and 42 class 1 samples. It misclassified 12 class 0 samples as class 1 and 8 class 1 samples as class 0.

If class 1 represents landslide risk, the 8 false negatives deserve particular attention because they are positive cases the model missed. Confirm the meaning of class 0 and class 1 in your dataset before publishing.
Saved Model Artifacts
The known model files are:
- models/random_forest_landslide.pkl — trained Random Forest classifier.
- models/landslide_features.pkl — feature metadata used by the prediction workflow.
Only load pickle files from trusted sources because deserializing untrusted pickle files can execute code.

## Installation
Prerequisites
- Python installed and available from your terminal.
- Git, if cloning from GitHub.
- Project source files and the required model artifacts.
- Any API key or environment configuration required by your weather-data integration.
1. Clone the repository
Replace the placeholders with your real GitHub repository URL and folder name.
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER>
2. Create a virtual environment
Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Windows Command Prompt:
python -m venv .venv
.venv\Scripts\activate.bat
Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
If your repository includes requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt
If it does not, create a requirements file from the packages actually imported by your project. The known stack includes scikit-learn, streamlit, and pyspark; other dependencies may be needed depending on your code. Confirm versions in your working environment rather than assuming these are the complete list.
Run the Application
If the Streamlit entry-point file is named app.py, run:
streamlit run app.py
Replace app.py with the actual filename if it differs. Streamlit prints a local URL in the terminal that you can open in a browser.

If PySpark processing runs as a separate script, follow the command and arguments defined by that script.
Example Prediction
A previously recorded example for Shillong used the following inputs:
Input	Value
Location	Shillong
Temperature	20.5 °C
Humidity	83%
Rainfall	0 mm
Month	9
Recorded model output	Approximately 56% risk


This is an illustrative output from the project, not a verified real-world probability or an official risk classification. Confirm that this example was produced by the same saved model and preprocessing pipeline used in the evaluation table.
## Limitations
- Results depend on training-data quality, coverage, class balance, and the evaluation method.
- Six features cannot capture every factor related to landslides, such as slope, elevation, geology, soil, drainage, and land-use changes.
- A model score should not be interpreted as a calibrated probability unless calibration and validation support that interpretation.
- Weather observations may be incomplete, delayed, or different from conditions at a specific slope.
- The model should not be used as the sole basis for public warnings or emergency decisions.

## Future Improvements
- Evaluate with geographically and temporally independent test data.
- Add reliable terrain, elevation, soil, and land-cover features.
- Track precision, recall, F1-score, ROC-AUC, and false negatives.
- Calibrate probability outputs and document the risk thresholds.
- Add reliable weather-source integration, timestamps, and error handling if not already present.
- Add an interactive map and historical risk visualizations.
- Add automated tests, input validation, logging, and model-version tracking.
- Document dataset sources, licenses, and limitations.


License
No license has been specified. Add a LICENSE file and identify the selected license here before permitting reuse or redistribution.
Author
Rugvedi Khandekar
GitHub: Your GitHub Profile
LinkedIn: Your LinkedIn Profile
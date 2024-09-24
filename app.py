from flask import Flask, render_template, request
import joblib
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd

app = Flask(__name__, static_folder='website', template_folder='website')

# Load the model
model = joblib.load('model/model.pkl')

# Load real data from CSV
data = pd.read_csv('data/modnim.csv')

# Crop information based on groundwater levels
crop_info = {
    'High': 'You can grow a variety of crops such as rice, wheat, and sugarcane. These crops require ample water supply.',
    'Medium': 'Consider growing crops like maize, barley, and pulses. These crops are moderately tolerant to varying water levels.',
    'Low': 'Opt for drought-resistant crops such as millet, sorghum, and legumes. These crops require minimal water.',
}

# Function to generate Year-wise GWL graph based on data
def generate_yearwise_plot():
    years = data['Year'].dropna().astype(int).tolist()
    gwl_values = data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').mean(axis=1).tolist()  # Average across months
    
    fig = go.Figure([go.Bar(x=years, y=gwl_values, marker=dict(color='blue'))])
    fig.update_layout(
        title=dict(
            text='Prev Year-wise Groundwater Levels',
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Year',
        yaxis_title='Groundwater Level (mbgl)',
        height=250,
        width=400,
        margin=dict(l=20, r=20, t=40, b=30)
    )
    return pio.to_html(fig, full_html=False)

# Function to generate Month-wise GWL graph based on selected year
def generate_monthwise_plot(year):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    gwl_values = []

    # Filter data for the selected year
    year_data = data[data['Year'] == year]
    
    if year_data.empty:
        gwl_values = [predict_gwl(year, month) for month in months]
    else:
        for month in months:
            month_num = pd.to_datetime(month, format='%b').month
            if month_num in year_data.columns[1:]:
                value = year_data.iloc[0, month_num].astype(float)
                if pd.isna(value):
                    value = predict_gwl(year, month)
            else:
                value = predict_gwl(year, month)
            gwl_values.append(value)

    fig = go.Figure([go.Scatter(x=months, y=gwl_values, mode='lines+markers', marker=dict(color='blue'))])
    fig.update_layout(
        title=dict(
            text=f'Month-wise Groundwater Levels for {year}',
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Month',
        yaxis_title='Groundwater Level (mbgl)',
        height=250,
        width=400,
        margin=dict(l=20, r=20, t=40, b=30)
    )
    return pio.to_html(fig, full_html=False)

# Function to predict groundwater levels based on input year and month
def predict_gwl(year, month):
    month_num = pd.to_datetime(month, format='%b').month
    input_data = pd.DataFrame({'Year': [year], 'Month': [month_num]})
    prediction = model.predict(input_data)[0]
    return prediction

# Function to determine crop advice based on groundwater level
def get_crop_advice(gwl):
    if gwl < 10:
        return crop_info['Low']
    elif gwl < 20:
        return crop_info['Medium']
    else:
        return crop_info['High']

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    yearwise_plot_html = generate_yearwise_plot()
    selected_year = data['Year'].max()  # Default year
    selected_month = 'Jan'
    monthwise_plot_html = generate_monthwise_plot(selected_year)
    crop_advice = None
    
    if request.method == 'POST':
        try:
            selected_year = int(request.form['year'])
            selected_month = request.form['month']
            prediction = predict_gwl(selected_year, selected_month)
            monthwise_plot_html = generate_monthwise_plot(selected_year)
            crop_advice = get_crop_advice(prediction)
        except ValueError:
            monthwise_plot_html = "Invalid year selected."

    return render_template('predict.html',
                           prediction=prediction,
                           yearwise_plot_html=yearwise_plot_html,
                           monthwise_plot_html=monthwise_plot_html,
                           selected_year=selected_year,
                           selected_month=selected_month,
                           crop_advice=crop_advice)

if __name__ == '__main__':
    app.run(debug=True)

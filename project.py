import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
  
tsla=yf.Ticker('TSLA')
tesla_data=tsla.history(period='max')
tesla_data.reset_index(inplace=True)
print(tesla_data.head())

url=' https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm' 
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')
table=soup.find_all('tbody')[1]
tesla_revenue=pd.DataFrame(columns=['Date','Revenue'])
for rows in table.find_all('tr'):
    column=rows.find_all('td')
    date=column[0].text
    revenue=column[1].text
    tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame([[date, revenue]], columns=tesla_revenue.columns)], ignore_index=True)
  
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
print(tesla_revenue.tail())

GameStop=yf.Ticker('GME')
gme_data=GameStop.history(period='max')
gme_data.reset_index(inplace=True)
print(gme_data.head())

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
tbody_elements = soup.find_all('tbody')
if len(tbody_elements) > 0:
    table = tbody_elements[1]
    GME_Revenue = pd.DataFrame(columns=['Date', 'Revenue'])
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 1: 
            date = columns[0].text.strip()
            revenue = columns[1].text.strip()
            GME_Revenue = pd.concat([GME_Revenue, pd.DataFrame([[date, revenue]], columns=GME_Revenue.columns)], ignore_index=True)
    print(GME_Revenue.tail())
else:
    print("No <tbody> found!")

make_graph(tesla_data,tesla_revenue,'Tesla')
make_graph(gme_data,GME_Revenue,'GME')

from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table',attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
row=table.find_all('td',attrs={'class':'text-narrow-screen-hidden'})

row_length = len(row)

temp = [] #initiating a list 

for i in range(0,row_length):
#insert the scrapping process here
    tanggal = table.find_all('tr')[i].findAll('td')[0].text
    harga_harian = table.find_all('tr')[i].findAll('td')[2].text
        
    temp.append((tanggal,harga_harian))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp,columns=('tanggal','harga_harian'))

#insert data wrangling here
df['harga_harian'] = df['harga_harian'].str.replace("IDR","")
df['harga_harian'] = df['harga_harian'].str.replace(",","")
df['harga_harian'] = df['harga_harian'].astype('float64')
df['tanggal'] = df['tanggal'].astype('datetime64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["harga_harian"].mean().round(2)}'

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
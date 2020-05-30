from flask import Flask, request, render_template
import Scraper_modules
app = Flask(__name__)

@app.route('/')
def my_form():
	return render_template('text_box.html')

@app.route('/data', methods=['POST'])
def process_form():
	text = request.form['Handle']
	try: #if data on user already exists on server, load that instead
		f = open(text+'.json','r')
		data = f.read()
		f.close()
		print("Loading saved data")
		return render_template('data.html', result = data)
	except:
		pass
	api = Scraper_modules.authenticate()
	data = Scraper_modules.scrape(api, text, False, False)
	f = open(text+'.json','w') #save data on user to save requests upon requests for same user
	f.write(str(data))
	f.close()
	return render_template('data.html', result = data)

# @app.route('/past', methods=['POST'])
# def display_past():
	# text = request.form['Handle']
	# f.open(text+'.json','r')
	# data = f.read()
	# f.close()
	# return render_template('data.html', result = data)
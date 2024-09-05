from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Database model
class IPData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to capture IP and location
@app.route('/capture_ip')
def capture_ip():
    # Fetch IP address
    ip_response = requests.get('https://httpbin.org/ip')
    if ip_response.status_code == 200:
        ip_data = ip_response.json()
        ip_address = ip_data.get('origin', 'N/A')
        
        # Fetch location based on IP address
        location_response = requests.get(f'https://ipinfo.io/{ip_address}/geo')
        if location_response.status_code == 200:
            location_data = location_response.json()
            city = location_data.get('city', 'N/A')
            region = location_data.get('region', 'N/A')
            country = location_data.get('country', 'N/A')
            
            # Store data in the database
            ip_data_entry = IPData(ip_address=ip_address, city=city, region=region, country=country)
            db.session.add(ip_data_entry)
            db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

from flask import Flask, request, render_template, jsonify,url_for
import datetime
from main import TripCrew  # นำเข้า TripCrew จาก main.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('filter_l.html')
@app.route('/process_trip_plan', methods=['POST'])
def process_trip_plan():
    # Get data from the form
    origin = request.form.get('start-location')
    cities = request.form.get('cities')
    start_date = request.form.get('start-date')
    end_date = request.form.get('end-date') or start_date  # Default to start_date if end_date is not provided
    interests = request.form.get('lifestyle')
    pricing_tiers = request.form.get('pricing-tiers')

    # Convert the string dates to datetime objects
    try:
        start_date = datetime.date.fromisoformat(start_date) if start_date else datetime.date.today()
        end_date = datetime.date.fromisoformat(end_date) if end_date else start_date + datetime.timedelta(days=5)
    except ValueError:
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=5)

    date_range = (start_date, end_date)

    # Create an instance of TripCrew with the form data
    trip_crew = TripCrew(origin, cities, date_range, interests, pricing_tiers)
    plan_summary, result = trip_crew.run()

    # Pass the result to the template for display
    return render_template('show_plan_l.html', plan_summary=plan_summary, result=result)

@app.route('/show_plan_l', methods=['GET'])
def show_plan_l():
    # ดึงข้อมูลจาก URL query string
    travel_data = request.args

    # ดึงข้อมูลที่จำเป็น
    startLocation = travel_data.get('startLocation')
    destination = travel_data.get('destination')
    date_start = travel_data.get('startDate')
    days = int(travel_data.get('days')) - 1
    lifestyles = travel_data.getlist('lifestyles')  # Lifestyle ที่เลือก
    vehicles = travel_data.getlist('vehicles')  # รถที่เลือก
    hotelQuality = int(travel_data.get('hotelQuality'))
    foodIncluded = travel_data.get('foodInclusion')

    # คำนวณวันที่สิ้นสุดจากวันที่เริ่มต้นและจำนวนวัน
    date_start_obj = datetime.date.fromisoformat(date_start)
    date_end_obj = date_start_obj + datetime.timedelta(days=days)
    date_range = (date_start_obj, date_end_obj)

    # สร้างอ็อบเจ็กต์ TripCrew และรันมัน
    trip_crew = TripCrew(startLocation, destination, date_range, lifestyles, vehicles, hotelQuality, foodIncluded)
    result = trip_crew.run()  # ผลลัพธ์จากการคำนวณแผนการเดินทาง

    # ส่งผลลัพธ์ที่ได้ไปแสดงใน template
    return render_template('show_plan_l.html', result=result)
# Collecting travel data from the frontend
@app.route('/api/collect-travel-data', methods=['POST'])
def collect_travel_data():
    # Get the JSON data sent from the frontend
    travel_data = request.json
    print("Travel data received:", travel_data)

    # Optionally store the data in a session or database
    # For simplicity, we'll just pass it to the next page

    return jsonify({
        'message': 'Travel data collected successfully!',
        'data': travel_data,
        'redirect_url': url_for('show_plan_l', **travel_data)
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=False)

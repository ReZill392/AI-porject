from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# ข้อมูลตัวอย่างสำหรับแผนการเดินทาง
todos = {}

@app.get('/')
def home():
    return render_template('filter.html', todos=todos)

@app.route('/api/collect-travel-data', methods=['POST'])
def collect_travel_data():
    try:
        # รับข้อมูล JSON ที่ส่งมาจาก JavaScript
        travel_data = request.json
        
        # ตัวอย่าง: บันทึกข้อมูลการเดินทางลงในฐานข้อมูลหรือไฟล์
        print("Received Travel Data:", travel_data)

        # ส่งข้อมูลนี้ไปประมวลผล (เรียก TripCrew หรือการประมวลผลอื่น ๆ)
        date_range = (travel_data['startDate'], travel_data['days'])
        trip_crew = TripCrew(
            origin=travel_data['startLocation'],
            cities=travel_data['destination'],
            date_range=date_range,
            interests=travel_data['lifestyles'],
            pricing_tiers=travel_data['hotelQuality'],
        )
        result = trip_crew.run()

        # ส่งคำตอบกลับไปยัง JavaScript
        return jsonify({"message": "Trip data processed successfully!", "result": result})
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "An error occurred while processing the travel data.", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
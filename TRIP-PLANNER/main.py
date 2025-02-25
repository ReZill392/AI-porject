from flask import Flask, request, render_template, redirect, url_for
import datetime
from crewai import Crew
from agents import TravelAgent
from tasks import TravelTasks
import os
from dotenv import load_dotenv
import json

# โหลด environment variables
load_dotenv()

app = Flask(__name__)

class TripCrew:
    def __init__(self, startLocation, destination, date_range, lifestyle, vehicles, hotelQuality, foodIncluded):
        self.startLocation = startLocation
        self.destination = destination
        self.date_range = date_range
        self.lifestyle = lifestyle
        self.vehicles = vehicles  # ใช้เป็น pricing_tiers
        self.hotelQuality = hotelQuality
        self.foodIncluded = foodIncluded

    def run(self):
        agents = TravelAgent()
        tasks = TravelTasks()

        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent,  # agent
            self.destination,      # city
            self.date_range,       # range
            self.lifestyle,        # interests
            self.vehicles,         # pricing_tiers
            self.hotelQuality,     # hotelQuality
            self.foodIncluded      # foodIncluded
        )

        identify_city = tasks.identify_city(
            city_selection_expert,  # agent
            self.startLocation,      # origin
            self.destination,        # cities (ต้องใช้ destination หรือ list ของ cities)
            self.lifestyle,          # interests
            self.date_range          # range
        )
        
        gather_city_info = tasks.gather_city_info(
            local_tour_guide,
            self.destination,
            self.date_range,
            self.lifestyle,
            self.hotelQuality,
            self.foodIncluded,
        )

        # Define your custom crew here
        crew = Crew(
            agents=[expert_travel_agent, 
                    city_selection_expert, 
                    local_tour_guide],
            tasks=[plan_itinerary, 
                   identify_city, 
                   gather_city_info],
            verbose=True,
        )

        result = crew.kickoff()
        return result

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # ดึงข้อมูลจากฟอร์ม
        startLocation = request.form['start-location']
        destination = request.form['destination']
        date_start = request.form['start-date']
        days = int(request.form['days'])-1
        lifestyle = request.form['lifestyle']
        vehicles = request.form.getlist('vehicles')  # สามารถรับหลายค่าได้
        hotelQuality = request.form['hotel-quality']
        foodIncluded = request.form['food-inclusion']

        # คำนวณวันที่สิ้นสุดจากวันที่เริ่มต้นและจำนวนวัน
        date_start_obj = datetime.date.fromisoformat(date_start)
        date_end_obj = date_start_obj + datetime.timedelta(days=days)
        date_range = (date_start_obj, date_end_obj)

        # สร้างอ็อบเจ็กต์ TripCrew และรันมัน
        trip_crew = TripCrew(startLocation, destination, date_range, lifestyle, vehicles, hotelQuality, foodIncluded)
        result = trip_crew.run()

        # เก็บผลลัพธ์ใน session หรือไฟล์ชั่วคราว
        output_file = "trip_plan.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f)

        # ส่ง destination ไปยังหน้ารายละเอียดแผนการเดินทาง
        return redirect(url_for('show_plan_a', destination=destination))

    return render_template('filter_a.html')

@app.route('/show_plan_a', methods=['GET'])
def show_plan_a():
    # ดึงค่าจาก Query Parameters
    destination = request.args.get('destination', 'Unknown Destination')
    
    # ตรวจสอบ destination และกำหนดข้อมูลให้เหมาะสม
    if destination == 'Lopburi':
        image = url_for('static', filename='images/Show_Plan_ลพบุรี(1).jpeg')
        title = 'Lopburi'
        result = "ข้อมูลแผนการเดินทางสำหรับลพบุรี"
    elif destination == 'Ayutthaya':
        image = '../static/images/Show_Plan_อยุธยา(1).jpeg'
        title = 'Ayutthaya'
        result = "ข้อมูลแผนการเดินทางสำหรับอยุธยา"
    elif destination == 'Nakhon Pathom':
        image = '../static/images/Show_Plan_นครปฐม(1).jpeg'
        title = 'Nakhon Pathom'
        result = "ข้อมูลแผนการเดินทางสำหรับนครปฐม"
    elif destination == 'Suphan Buri':
        image = '../static/images/Show_Plan_สุพรรณบุรี(1).jpeg'
        title = 'Suphan Buri'
        result = "ข้อมูลแผนการเดินทางสำหรับสุพรรณบุรี"
    else :
        image = '../static/images/Show_Plan_สมุทรสงคราม(1).jpeg'
        title = 'Samut SongKhram'
        result = "ข้อมูลแผนการเดินทางสำหรับสมุทรสงคราม"
        

    return render_template(
        'show_plan_a.html', 
        image=image,
        title=title, 
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)

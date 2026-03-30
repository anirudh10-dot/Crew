import random
import time

class SpaceStationAI:

    def __init__(self, astronauts, activity_level):
        self.astronauts = astronauts
        self.activity_level = activity_level.lower()

        # 🌌 Initial realistic values
        self.oxygen = random.uniform(20, 22)        # %
        self.water = random.uniform(80, 120)        # liters
        self.co2 = random.uniform(0.2, 0.6)         # %

        self.pressure = random.uniform(98, 103)     # kPa
        self.temperature = random.uniform(20, 25)   # °C
        self.humidity = random.uniform(35, 60)      # %

        self.radiation = random.uniform(0.05, 0.15) # mSv/hr
        self.hydrogen = random.uniform(0.0, 0.05)   # %
        self.contaminants = random.uniform(0.5, 2)  # ppm

        # 🔥 Dynamic consumption
        if self.activity_level == "low":
            self.oxygen_rate = 0.8
            self.water_rate = 0.5
        elif self.activity_level == "medium":
            self.oxygen_rate = 1.2
            self.water_rate = 0.8
        else:
            self.oxygen_rate = 1.8
            self.water_rate = 1.2

    # 🔄 Sensor simulation
    def update_sensors(self):
        self.oxygen -= random.uniform(0.05, 0.2)
        self.water -= random.uniform(0.2, 0.8)
        self.co2 += random.uniform(0.02, 0.08)

        self.pressure += random.uniform(-0.5, 0.5)
        self.temperature += random.uniform(-0.3, 0.3)
        self.humidity += random.uniform(-2, 2)

        self.radiation += random.uniform(-0.01, 0.02)
        self.hydrogen += random.uniform(0.0, 0.01)
        self.contaminants += random.uniform(0.0, 0.3)

    def calculate_time_left(self):
        total_oxygen_usage = self.oxygen_rate * self.astronauts
        total_water_usage = self.water_rate * self.astronauts

        oxygen_time = self.oxygen / total_oxygen_usage
        water_time = self.water / total_water_usage

        return oxygen_time, water_time

    # ⚠️ Smart AI Risk Detection
    def check_status(self, oxygen_time, water_time):
        status = []

        # Oxygen
        if self.oxygen < 19:
            status.append("🚨 Oxygen dangerously low")
        elif self.oxygen < 20:
            status.append("⚠️ Oxygen dropping")

        # CO2
        if self.co2 > 1:
            status.append("🚨 CO₂ high خطر")
        elif self.co2 > 0.7:
            status.append("⚠️ CO₂ rising")

        # Pressure
        if self.pressure < 95 or self.pressure > 105:
            status.append("🚨 Pressure unstable")

        # Temperature
        if self.temperature < 18 or self.temperature > 27:
            status.append("⚠️ Temperature out of range")

        # Humidity
        if self.humidity < 30 or self.humidity > 70:
            status.append("⚠️ Humidity imbalance")

        # Radiation
        if self.radiation > 0.2:
            status.append("🚨 Radiation spike!")

        # Hydrogen
        if self.hydrogen > 0.1:
            status.append("🚨 Hydrogen leak risk")

        # Contaminants
        if self.contaminants > 5:
            status.append("🚨 Air contaminated")

        # Water
        if water_time < 8:
            status.append("⚠️ Water low")

        if not status:
            status.append("✅ All systems stable")

        return status

    def predict_future_risk(self, oxygen_time):
        if oxygen_time < 5:
            return "🚨 Life support CRITICAL"
        elif oxygen_time < 10:
            return "⚠️ Risk increasing"
        else:
            return "✅ Stable forecast"


# 🌌 MAIN LOOP

print("🌌 AI Space Station Advanced Monitoring 🌌")

astronauts = int(input("Enter number of astronauts: "))
activity = input("Enter activity level (low / medium / high): ")

ai = SpaceStationAI(astronauts, activity)

while True:
    ai.update_sensors()

    oxygen_time, water_time = ai.calculate_time_left()

    print("\n==============================")
    print(f"🫁 Oxygen: {ai.oxygen:.2f}%")
    print(f"💧 Water: {ai.water:.2f} L")
    print(f"🌫️ CO₂: {ai.co2:.2f}%")

    print(f"ضغط Pressure: {ai.pressure:.2f} kPa")
    print(f"🌡️ Temperature: {ai.temperature:.2f} °C")
    print(f"💧 Humidity: {ai.humidity:.2f}%")

    print(f"☢️ Radiation: {ai.radiation:.3f} mSv/hr")
    print(f"🧪 Hydrogen: {ai.hydrogen:.3f}%")
    print(f"🧬 Contaminants: {ai.contaminants:.2f} ppm")

    print(f"\n⏳ Oxygen left: {oxygen_time:.2f} hrs")
    print(f"⏳ Water left: {water_time:.2f} hrs")

    print("\n📊 Status:")
    for s in ai.check_status(oxygen_time, water_time):
        print("-", s)

    print("\n⚠️ AI Prediction:", ai.predict_future_risk(oxygen_time))

    time.sleep(2)

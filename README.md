# EV Charging Station Location Optimization using Hybrid Gray Wolf and Genetic Algorithms

🧩 Project Features
🧠 AI-Based Optimization: Uses Gray Wolf Optimizer and Genetic Algorithm.

🗺️ Interactive Heatmaps: Visualize existing, potential, and optimal station locations.

🧍 Role-Based Access: Separate interfaces for users and administrators.

🔎 Nearest Station Locator: Find the closest charging station from your location.

## 🔧 Setup Instructions

To run the project, follow these steps in order:

1. **Start Combined API**  
   ```bash
   python combined_api.py
   ```

2. **Start Nearest Stations Script**  
   ```bash
   python nearest_stations.py
   ```

3. **Start Flask App**  
   ```bash
   python app.py
   ```

4. **Open pgAdmin**  
   - Launch pgAdmin from your system menu or terminal.

5. **Visit the Web App**  
   - Open your browser and go to:  
     [http://localhost:3000](http://localhost:3000)

---

## 📸 Screenshots

### 1. Register Page
![Register Page](Register_page.png)

### 2. Login Page
![Login Page](Login_page.png)

### 3. Admin Page
![Admin Page](Admin_dashbord.png)

### 4. Service Page
![Service Page](PGAdmin.png)

### 5. Nearest Stations
![Nearest Stations](Nearest_station.png)

### 6. Existing Heatmap
![Existing Heatmap](Exisiting_Charging_Stations.png)

### 7. Potential Heatmap
![Potential Heatmap](Potential_Ev_Loaction.png)

### 8. Optimal Heatmap
![Optimal Heatmap](optimal_Ev_stations_HeatMap.png)

---

## ✅ Notes

- Make sure PostgreSQL and pgAdmin are installed and properly configured.
- Ensure all dependencies in `requirements.txt` are installed:
  ```bash
  pip install -r requirements.txt
  ```

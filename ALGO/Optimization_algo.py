import psycopg2
import numpy as np
import random
from math import radians, sin, cos, sqrt, atan2

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="EV",
        user="postgres",
        password="@Ankur7753",
        host="localhost",
        port="5432"
    )

# Haversine formula to calculate distance (in km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Fetch existing EV stations
def get_existing_ev_stations():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, latitude, longitude, type FROM ev_stations")  # Added ID and name
    stations = cur.fetchall()
    cur.close()
    conn.close()
    return [(row[0], row[1], row[2], row[3], row[4]) for row in stations]  # Include full details

# Fetch potential locations (within 100 km radius)
def get_potential_locations(current_lat, current_lon):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, name, latitude, longitude, type FROM potential_locations")
    locations = cur.fetchall()
    cur.close()
    conn.close()

    valid_locations = [
        (row[0], row[1], row[2], row[3], row[4]) 
        for row in locations if haversine(current_lat, current_lon, row[2], row[3]) <= 100
    ]

    return valid_locations

# Genetic Algorithm for optimization
def genetic_algorithm(potential_locations, existing_stations, population_size=20, generations=50):
    def fitness(chromosome):
        score = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                lat, lon = potential_locations[i][2], potential_locations[i][3]
                if all(haversine(lat, lon, ex_lat, ex_lon) > 5 for _, _, ex_lat, ex_lon, _ in existing_stations):  
                    score += 1  
        return score

    population = [np.random.choice([0, 1], size=len(potential_locations)).tolist() for _ in range(population_size)]
    
    for _ in range(generations):
        scores = [fitness(ind) for ind in population]
        
        sorted_population = [x for _, x in sorted(zip(scores, population), key=lambda pair: pair[0], reverse=True)]

        new_population = sorted_population[:population_size//2]
        
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(sorted_population[:10], 2)
            crossover = random.randint(0, len(parent1)-1)
            child = parent1[:crossover] + parent2[crossover:]
            if random.random() < 0.1:  
                mutate_index = random.randint(0, len(child)-1)
                child[mutate_index] = 1 - child[mutate_index]
            new_population.append(child)
        
        population = new_population

    best_solution = max(population, key=fitness)
    return [potential_locations[i] for i in range(len(best_solution)) if best_solution[i] == 1]

# Grey Wolf Optimizer for refinement
def grey_wolf_optimizer(potential_locations, existing_stations, max_iter=50):
    wolves = [np.random.choice([0, 1], size=len(potential_locations)) for _ in range(10)]
    
    def fitness(wolf):
        return sum(
            1 for i in range(len(wolf)) if wolf[i] == 1 and 
            all(haversine(potential_locations[i][2], potential_locations[i][3], ex_lat, ex_lon) > 5 for _, _, ex_lat, ex_lon, _ in existing_stations)
        )

    alpha, beta, delta = sorted(wolves, key=fitness, reverse=True)[:3]

    for _ in range(max_iter):
        for wolf in wolves:
            for i in range(len(wolf)):
                r1, r2 = random.random(), random.random()
                A1, A2, A3 = 2 * r1 - 1, 2 * r2 - 1, 2 * random.random() - 1
                X1 = alpha[i] - A1 * abs(alpha[i] - wolf[i])
                X2 = beta[i] - A2 * abs(beta[i] - wolf[i])
                X3 = delta[i] - A3 * abs(delta[i] - wolf[i])
                wolf[i] = round((X1 + X2 + X3) / 3)

        alpha, beta, delta = sorted(wolves, key=fitness, reverse=True)[:3]

    best_solution = alpha
    return [potential_locations[i] for i in range(len(best_solution)) if best_solution[i] == 1]

# Store optimal locations (includes existing EV stations)
# Store optimal locations
def store_optimal_locations(optimal_locations, existing_stations):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # ✅ Step 1: Clear the table before inserting new optimal stations
    cur.execute("DELETE FROM optimal_ev_stations")

    # ✅ Step 2: Insert new optimal locations (handling duplicates)
    for loc_id, name, lat, lon, loc_type in optimal_locations:
        cur.execute(
            """
            INSERT INTO optimal_ev_stations (id, name, latitude, longitude, type)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (loc_id, name, lat, lon, loc_type)
        )

    # ✅ Step 3: Insert existing EV stations into optimal_ev_stations
    for station in existing_stations:
        station_id, station_name, lat, lon, station_type = station  # ✅ Unpacking all 5 columns
        cur.execute(
            """
            INSERT INTO optimal_ev_stations (id, name, latitude, longitude, type)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (station_id, station_name, lat, lon, station_type)
        )

    conn.commit()
    cur.close()
    conn.close()


# Main function
def find_and_store_optimal_stations(current_lat, current_lon):
    existing_stations = get_existing_ev_stations()
    potential_locations = get_potential_locations(current_lat, current_lon)

    # Step 1: Use Genetic Algorithm to find a set of good locations
    optimal_ga_stations = genetic_algorithm(potential_locations, existing_stations)

    # Step 2: Use Grey Wolf Optimizer for further refinement
    optimal_gwo_stations = grey_wolf_optimizer(optimal_ga_stations, existing_stations)

    # ✅ Include existing stations in final storage
    store_optimal_locations(optimal_gwo_stations, existing_stations)
    print(f"Stored {len(optimal_gwo_stations) + len(existing_stations)} optimal EV stations successfully!")

# Run the function
current_latitude = 26.080674618890548 
current_longitude = 91.5581063516589 

find_and_store_optimal_stations(current_latitude, current_longitude)

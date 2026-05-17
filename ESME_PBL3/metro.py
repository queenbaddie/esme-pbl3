import json
import heapq
from collections import deque

#--------Normalize to have no accent--------
def normalize(text):
    text = text.strip().lower() #enlève espace début et fin + met en minuscule
    accents = {
        'à': 'a', 'â': 'a', 'á': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i', 'í': 'i',
        'ô': 'o', 'ö': 'o', 'ó': 'o',
        'ù': 'u', 'û': 'u', 'ú': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    return "".join(accents.get(c, c) for c in text) 
#parcours le texte et remplace le remplace par la version sans accent, sans join, on aurait une liste
# ---------- LOAD DATA ----------

def load_data(city_name):

    file_path = f"data/{city_name}.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("File not found")
        return None

    return (
        data["lignes"],
        data["connexions"],
        data["correspondances"],
        data["temps_moyen"]
    )


# ---------- BUILD GRAPH ----------

def build_graph(lignes, connexions, correspondances, temps_moyen):

    graph = {}

    if connexions:

        for conn in connexions:

            s1 = conn["de"]
            s2 = conn["vers"]
            temps = conn["temps"]
            ligne = conn["ligne"]

            if s1 not in graph:
                graph[s1] = []
            if s2 not in graph:
                graph[s2] = []

            graph[s1].append((s2, temps, ligne))
            graph[s2].append((s1, temps, ligne))

    else:

        for ligne_id, ligne_data in lignes.items():

            stations = ligne_data["stations"]

            for i in range(len(stations) - 1):

                s1 = stations[i]
                s2 = stations[i + 1]

                if s1 not in graph:
                    graph[s1] = []
                if s2 not in graph:
                    graph[s2] = []

                graph[s1].append((s2, temps_moyen, ligne_id))
                graph[s2].append((s1, temps_moyen, ligne_id))

    for corr in correspondances:
        station = corr["station"]
        if station not in graph:
            graph[station] = []

    return graph


# ---------- BFS ----------

def bfs_shortest_path(graph, start, end):

    visited = set()
    queue = deque([(start, [(start, None)])])

    while queue:

        current, path = queue.popleft()

        if current == end:
            return path

        if current not in visited:

            visited.add(current)

            for neighbor, weight, line in graph[current]:

                if neighbor not in visited:
                    queue.append((neighbor, path + [(neighbor, line)]))

    return []


# ---------- DFS ----------

def dfs(graph, start, visited=None):

    if visited is None:
        visited = set()

    visited.add(start)

    for neighbor, weight, line in graph[start]:

        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited


# ---------- DIJKSTRA ----------

def dijkstra(graph, start, end):

    queue = [(0, start)]

    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    previous = {node: None for node in graph}
    previous_line = {node: None for node in graph}

    while queue:

        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, weight, line in graph[current_node]:

            transfer_cost = 0

            if previous_line[current_node] is not None and line != previous_line[current_node]:
                transfer_cost = 120

            new_dist = current_distance + weight + transfer_cost

            if new_dist < distances[neighbor]:

                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                previous_line[neighbor] = line

                heapq.heappush(queue, (new_dist, neighbor))

    return distances, previous, previous_line


# ---------- REBUILD PATH ----------

def get_path(previous, previous_line, start, end):

    path = []
    current = end

    while current is not None:
        path.append((current, previous_line[current]))
        current = previous[current]

    path.reverse()

    if len(path) > 1:
        path[0] = (path[0][0], path[1][1])

    return path


# ---------- MAIN ----------

if __name__ == "__main__":

    while True:

        print("\n===== METRO ROUTE PLANNER =====")

        city = input("Choose city (paris, lyon, lille, bordeaux): ").lower()

        data = load_data(city)

        if data is None:
            continue

        lignes, connexions, correspondances, temps_moyen = data

        graph = build_graph(lignes, connexions, correspondances, temps_moyen)

        print("\nTransfer stations:")
        for c in correspondances:
            print("-", c["station"])

        #pour que çafocntionne sans majuscule et sans accent 
        station_map = {normalize(s): s for s in graph}

        start_input = normalize(input("\nDeparture station: "))
        end_input = normalize(input("Arrival station: "))

        start = station_map.get(start_input)
        end = station_map.get(end_input)

        if start is None or end is None:
            print("Invalid station")
            continue


        # ---------- BFS ----------
        bfs_path = bfs_shortest_path(graph, start, end)

        print("\n===== FEWEST STOPS (BFS) =====")
        for station, line in bfs_path:
            print(f"-> {station}" + (f" (line {line})" if line else ""))

        print(f"\nStops: {len(bfs_path) - 1}")

        # ---------- DFS ----------
        visited = dfs(graph, start)

        print("\n===== DFS =====")
        print("Reachable stations:", len(visited))

        # ---------- DIJKSTRA ----------
        distances, previous, previous_line = dijkstra(graph, start, end)
        path = get_path(previous, previous_line, start, end)

        print("\n===== FASTEST PATH =====\n")

        if not path:
            print("No path found")
            continue

        # ---------- BUILD SEGMENTS ----------
        segments = []

        current_line = path[1][1] if len(path) > 1 else path[0][1]
        segment = [path[0][0]]

        for i in range(1, len(path)):

            station, line = path[i]

            if line == current_line or line is None:
                segment.append(station)

            else:
                segments.append((current_line, segment))
                current_line = line
                segment = [path[i - 1][0], station]

        segments.append((current_line, segment))

        # ---------- PRINT CLEAN OUTPUT ----------

        first_line, first_segment = segments[0]

        print(f"Board at {first_segment[0]} station, line {first_line}")

        for i, (line, stations) in enumerate(segments):

            for s in stations[1:-1]:
                print(f"Continue through {s} station")

            if i < len(segments) - 1:

                transfer_station = stations[-1]
                next_line = segments[i + 1][0]

                print(
                    f"Transfer at {transfer_station} station, "
                    f"take line {next_line}"
                )

        last_line, last_segment = segments[-1]

        print(
            f"Alight at {last_segment[-1]} station, "
            f"line {last_line}"
        )

        minutes = distances[end] // 60
        seconds = distances[end] % 60

        print(f"\nEstimated total time: {minutes} minutes {seconds} seconds")

        again = input("\nDo you want to do another reaserch ? (yes/no) : ").strip().lower()
        if again not in ("oui", "yes"):
            print("Good bye!")
            break

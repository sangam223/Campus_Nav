import tkinter as tk
from tkinter import ttk
from queue import PriorityQueue
from collections import deque
from PIL import Image, ImageTk

# ---------------- Distances ----------------
distances = {
    "Admin Block": {
        "Security Entrance": 80, "Library": 16, "Auditorium": 17, "Academic Block": 126,
        "Cafeteria": 35, "Main Gate": 160, "Exit Gate": 220, "Medical": 80,
        "Hostel": 506, "Mini Mart": 434, "Food Court": 355, "Sports": 850
    },
    "Academic Block": {
        "Security Entrance": 240, "Library": 46, "Auditorium": 150, "Cafeteria": 27,
        "Main Gate": 210, "Exit Gate": 250, "Medical": 85, "Hostel": 380,
        "Mini Mart": 410, "Food Court": 192, "Admin Block": 126, "Sports": 561
    },
    "Library": {
        "Security Entrance": 100, "Auditorium": 3, "Academic Block": 46, "Cafeteria": 63,
        "Main Gate": 275, "Exit Gate": 240, "Medical": 75, "Hostel": 450,
        "Mini Mart": 465, "Food Court": 470, "Admin Block": 16, "Sports": 857
    },
    "Cafeteria": {
        "Security Entrance": 130, "Library": 63, "Auditorium": 10, "Academic Block": 27,
        "Main Gate": 276, "Exit Gate": 270, "Medical": 90, "Hostel": 520,
        "Mini Mart": 585, "Food Court": 355, "Admin Block": 35, "Sports": 920
    },
    "Auditorium": {
        "Security Entrance": 120, "Library": 3, "Academic Block": 150, "Cafeteria": 10,
        "Main Gate": 286, "Exit Gate": 260, "Medical": 80, "Hostel": 510,
        "Mini Mart": 574, "Food Court": 344, "Admin Block": 17, "Sports": 930
    },
    "Food Court": {
        "Security Entrance": 471, "Library": 470, "Auditorium": 344, "Academic Block": 192,
        "Cafeteria": 355, "Main Gate": 699, "Exit Gate": 609, "Medical": 405,
        "Hostel": 816, "Mini Mart": 836, "Admin Block": 355, "Sports": 427
    },
    "Security Entrance": {
        "Admin Block": 80, "Academic Block": 240, "Library": 100, "Cafeteria": 130,
        "Auditorium": 120, "Food Court": 471, "Main Gate": 150, "Exit Gate": 180,
        "Medical": 90, "Hostel": 500, "Mini Mart": 520, "Sports": 880
    },
    "Main Gate": {
        "Admin Block": 160, "Academic Block": 210, "Library": 275, "Cafeteria": 276,
        "Auditorium": 286, "Food Court": 699, "Security Entrance": 150,
        "Exit Gate": 100, "Medical": 180, "Hostel": 600, "Mini Mart": 620, "Sports": 900
    },
    "Exit Gate": {
        "Admin Block": 220, "Academic Block": 250, "Library": 240, "Cafeteria": 270,
        "Auditorium": 260, "Food Court": 609, "Security Entrance": 180,
        "Main Gate": 100, "Medical": 160, "Hostel": 580, "Mini Mart": 600, "Sports": 870
    },
    "Medical": {
        "Admin Block": 80, "Academic Block": 85, "Library": 75, "Cafeteria": 90,
        "Auditorium": 80, "Food Court": 405, "Security Entrance": 90,
        "Main Gate": 180, "Exit Gate": 160, "Hostel": 490, "Mini Mart": 510, "Sports": 840
    },
    "Hostel": {
        "Admin Block": 506, "Academic Block": 380, "Library": 450, "Cafeteria": 520,
        "Auditorium": 510, "Food Court": 816, "Security Entrance": 500,
        "Main Gate": 600, "Exit Gate": 580, "Medical": 490, "Mini Mart": 200, "Sports": 300
    },
    "Mini Mart": {
        "Admin Block": 434, "Academic Block": 410, "Library": 465, "Cafeteria": 585,
        "Auditorium": 574, "Food Court": 836, "Security Entrance": 520,
        "Main Gate": 620, "Exit Gate": 600, "Medical": 510, "Hostel": 200, "Sports": 320
    },
    "Sports": {
        "Admin Block": 850, "Academic Block": 561, "Library": 857, "Cafeteria": 920,
        "Auditorium": 930, "Food Court": 427, "Security Entrance": 880,
        "Main Gate": 900, "Exit Gate": 870, "Medical": 840, "Hostel": 300, "Mini Mart": 320
    }
}

# ---------------- Pathfinding ----------------
def bfs(graph, start, goal):
    visited = set()
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path, len(path) - 1
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, {}):
                queue.append(path + [neighbor])
    return None, None

def dfs(graph, start, goal):
    visited = set()
    stack = [[start]]
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path, len(path) - 1
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, {}):
                stack.append(path + [neighbor])
    return None, None

def ucs(graph, start, goal):
    visited = set()
    pq = PriorityQueue()
    pq.put((0, [start]))
    while not pq.empty():
        cost, path = pq.get()
        node = path[-1]
        if node == goal:
            return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph.get(node, {}).items():
                if neighbor not in visited:
                    pq.put((cost + weight, path + [neighbor]))
    return None, None

def a_star(graph, heuristics, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    while not frontier.empty():
        _, current = frontier.get()
        if current == goal:
            break
        for neighbor, dist in graph[current].items():
            new_cost = cost_so_far[current] + dist
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristics.get(neighbor, 0)
                frontier.put((priority, neighbor))
                came_from[neighbor] = current
    if goal not in came_from:
        return None, None
    path = []
    node = goal
    while node:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path, cost_so_far[goal]

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Chanakya Campus Navigation")
root.geometry("900x700")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Tab 1: Pathfinding Assistant
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Pathfinding Assistant")

tk.Label(frame1, text="From:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
start_choice = ttk.Combobox(frame1, values=list(distances.keys()))
start_choice.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame1, text="To:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
end_choice = ttk.Combobox(frame1, values=list(distances.keys()))
end_choice.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame1, text="Algorithm:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
algo_choice = ttk.Combobox(frame1, values=["BFS", "DFS", "UCS", "A*"])
algo_choice.grid(row=2, column=1, padx=10, pady=5)
algo_choice.current(2)

result_text = tk.Text(frame1, height=8, width=70)
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Load map image (ensure this file exists in same folder)
map_img = Image.open("campus_map.jpg").resize((600, 400))
map_photo = ImageTk.PhotoImage(map_img)

canvas = tk.Canvas(frame1, width=600, height=400)
canvas.grid(row=6, column=0, columnspan=2, pady=10)

# Keep a reference so it doesn't get garbage collected
canvas.image = map_photo
canvas.create_image(0, 0, anchor="nw", image=map_photo)

# Location coordinates (adjust manually to fit your map layout)
location_coords = {
    "Admin Block": (100, 80),
    "Library": (200, 100),
    "Academic Block": (300, 150),
    "Cafeteria": (380, 180),
    "Auditorium": (250, 200),
    "Medical": (150, 250),
    "Hostel": (500, 300),
    "Mini Mart": (450, 280),
    "Food Court": (350, 250),
    "Main Gate": (50, 350),
    "Exit Gate": (100, 360),
    "Security Entrance": (60, 300),
    "Sports": (550, 350)
}

def draw_path(path):
    canvas.delete("path_line")
    for i in range(len(path)-1):
        x1, y1 = location_coords[path[i]]
        x2, y2 = location_coords[path[i+1]]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=3, tags="path_line")
        canvas.create_oval(x1-5, y1-5, x1+5, y1+5, fill="blue", tags="path_line")
    x_end, y_end = location_coords[path[-1]]
    canvas.create_oval(x_end-6, y_end-6, x_end+6, y_end+6, fill="green", tags="path_line")

def run_algorithm():
    start = start_choice.get().strip()
    end = end_choice.get().strip()
    algo = algo_choice.get()
    result_text.delete("1.0", tk.END)

    if start not in distances or end not in distances:
        result_text.insert(tk.END, "Invalid start or destination.\n")
        return

    if algo == "BFS":
        path, cost = bfs(distances, start, end)
    elif algo == "DFS":
        path, cost = dfs(distances, start, end)
    elif algo == "UCS":
        path, cost = ucs(distances, start, end)
    elif algo == "A*":
        heuristics = {loc: 0 for loc in distances}
        path, cost = a_star(distances, heuristics, start, end)
    else:
        path, cost = None, None

    if path:
        time_minutes = round(cost * 0.1, 1)
        result_text.insert(tk.END, f"Path: {' → '.join(path)}\n")
        result_text.insert(tk.END, f"Distance: {cost} meters\n")
        result_text.insert(tk.END, f"Estimated Time: {time_minutes} minutes\n")
        draw_path(path)
    else:
        result_text.insert(tk.END, "No path found.\n")

tk.Button(frame1, text="Find Path", command=run_algorithm).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

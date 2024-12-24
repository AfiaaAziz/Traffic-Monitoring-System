import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.integrate import quad
import threading 
from PIL import Image, ImageTk  # For car icons and background image

# Define the traffic density function
def f(t):
    return 10 + 5 * math.sin(t)

# Function to calculate the total traffic flow
def calculate_traffic():
    try:
        a = float(entry_start.get())
        b = float(entry_end.get())
        # Compute definite integral
        total_traffic, _ = quad(f, a, b)
        result_label.config(text=f"Total Traffic Flow: {total_traffic:.2f} vehicles")
        # Plot the graph in the main thread
        plot_graph(a, b)
        # Start animation for traffic flow in a separate thread
        threading.Thread(target=animate_traffic, args=(a, b)).start()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for the time interval.")


# Function to plot the traffic density graph
def plot_graph(a, b):
    t = np.linspace(a, b, 1000)
    y = [f(ti) for ti in t]
    plt.figure(figsize=(8, 5))
    plt.plot(t, y, label="Traffic Density f(t)")
    plt.fill_between(t, y, color="skyblue", alpha=0.4, label="Area under curve")
    plt.title("Traffic Density Graph")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Density (vehicles/minute)")
    plt.legend()
    plt.grid(True)
    plt.show()
    

# Function to animate traffic flow
def animate_traffic(a, b):
    # Create a window for the animation
    animation_window = tk.Toplevel(root)
    animation_window.title("Traffic Animation")
    canvas = tk.Canvas(animation_window, width=800, height=300, bg="white")
    canvas.pack()

    # Draw road
    road = canvas.create_rectangle(50, 100, 750, 200, fill="black")
    lane_line = canvas.create_line(50, 150, 750, 150, dash=(10, 10), fill="white")

    # Load car image
    car_image = Image.open("car.png")
    car_image = car_image.resize((50, 30), Image.Resampling.LANCZOS)
    car_icon = ImageTk.PhotoImage(car_image)

    cars = []
    # Add cars to the canvas
    for i in range(5):
        x = 60 + i * 100
        car = canvas.create_image(x, 135, image=car_icon, anchor=tk.NW)
        cars.append(car)


    t = a
    while t <= b:
        density = f(t)  # Get the current traffic density
        speed = 200 / density  # Adjust speed based on density
        for car in cars:
            canvas.move(car, speed, 0)
            pos = canvas.coords(car)
            if pos[0] > 750:  # Reset car position when it exits the road
                canvas.move(car, -700, 0)
        t += 0.1
        animation_window.update()
        canvas.after(100)

# GUI Setup
root = tk.Tk()
root.title("Traffic Monitoring System")
root.geometry("600x400")
root.configure(bg="#2c3e50")

# Load and set the background image
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Title label
title_label = tk.Label(root, text="Traffic Monitoring System", font=("Arial", 20, "bold"), bg="#34495e", fg="#ecf0f1")
canvas.create_window(300, 50, window=title_label)

# Input fields for time interval
frame = tk.Frame(root, bg="#34495e", padx=20, pady=20, bd=5, relief="ridge")
canvas.create_window(300, 150, window=frame)

tk.Label(frame, text="Start Time (a):", font=("Arial", 12), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, padx=10, pady=10)
entry_start = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", justify="center")
entry_start.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame, text="End Time (b):", font=("Arial", 12), bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, padx=10, pady=10)
entry_end = tk.Entry(frame, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", justify="center")
entry_end.grid(row=1, column=1, padx=10, pady=10)

# Button to calculate traffic and generate visualizations
calculate_button = tk.Button(root, text="Calculate Traffic", font=("Arial", 14, "bold"), bg="#1abc9c", fg="#ecf0f1", relief="raised", command=calculate_traffic, cursor="hand2")
canvas.create_window(300, 250, window=calculate_button)

# Label to display the result
result_label = tk.Label(root, text="Total Traffic Flow: ", font=("Arial", 14, "bold"), bg="#34495e", fg="#ecf0f1")
canvas.create_window(300, 320, window=result_label)

root.mainloop()

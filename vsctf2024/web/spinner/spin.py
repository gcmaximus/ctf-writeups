import mouse
import time
import math


# Get the size of the primary monitor
screen_width, screen_height = 1920,1080

# Calculate the center of the screen
center_x, center_y = screen_width / 2, screen_height / 2

# Number of movements
num_movements = 10000

# Small radius for circular motion
radius = 50

# Move the cursor around the center of the screen 10,000 times
for i in range(num_movements):
    angle = 2 * math.pi * (i / num_movements)  # Calculate the angle for this iteration
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    mouse.move(x, y)
    time.sleep(0.01)  # Optional: Add a small delay to make the movement visible

print("Done moving the cursor!")

import tkinter as tk
from tkinter import filedialog, messagebox
import ast  # To parse input data from files
import math


# ------------------- Closest Pair of Points Algorithm -------------------
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def closest_pair(points):
    def closest_pair_recursive(points_sorted_x, points_sorted_y):
        if len(points_sorted_x) <= 3:
            return brute_force_closest_pair(points_sorted_x)

        mid = len(points_sorted_x) // 2
        mid_point = points_sorted_x[mid]

        left_x = points_sorted_x[:mid]
        right_x = points_sorted_x[mid:]

        midpoint_x = mid_point[0]

        left_y = list(filter(lambda p: p[0] <= midpoint_x, points_sorted_y))
        right_y = list(filter(lambda p: p[0] > midpoint_x, points_sorted_y))

        (p1, q1, dist1) = closest_pair_recursive(left_x, left_y)
        (p2, q2, dist2) = closest_pair_recursive(right_x, right_y)

        if dist1 < dist2:
            d = dist1
            min_pair = (p1, q1)
        else:
            d = dist2
            min_pair = (p2, q2)

        (p3, q3, dist3) = closest_split_pair(points_sorted_x, points_sorted_y, d, min_pair)

        if dist3 < d:
            return (p3, q3, dist3)
        else:
            return (min_pair[0], min_pair[1], d)

    def brute_force_closest_pair(points):
        min_dist = float("inf")
        pair = (None, None)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                d = distance(points[i], points[j])
                if d < min_dist:
                    min_dist = d
                    pair = (points[i], points[j])
        return pair[0], pair[1], min_dist

    def closest_split_pair(px, py, delta, best_pair):
        mid_x = px[len(px) // 2][0]
        sy = [p for p in py if mid_x - delta <= p[0] <= mid_x + delta]
        best = delta
        len_sy = len(sy)
        for i in range(len_sy - 1):
            for j in range(i + 1, min(i + 7, len_sy)):
                p, q = sy[i], sy[j]
                dst = distance(p, q)
                if dst < best:
                    best = dst
                    best_pair = (p, q)
        return best_pair[0], best_pair[1], best

    px = sorted(points, key=lambda x: x[0])
    py = sorted(points, key=lambda x: x[1])

    return closest_pair_recursive(px, py)


# ------------------- Integer Multiplication Algorithm -------------------
def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    high1, low1 = divmod(x, 10 ** m)
    high2, low2 = divmod(y, 10 ** m)

    z0 = karatsuba(low1, low2)
    z1 = karatsuba((low1 + high1), (low2 + high2))
    z2 = karatsuba(high1, high2)

    return (z2 * 10 ** (2 * m)) + ((z1 - z2 - z0) * 10 ** m) + z0


# ------------------- GUI Implementation -------------------
def process_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = [ast.literal_eval(line.strip()) for line in file]
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return None


def apply_closest_pair(data):
    result = closest_pair(data)
    return f"Closest Pair: {result[0]}, {result[1]}\nDistance: {result[2]:.4f}"


def apply_karatsuba(data):
    results = [karatsuba(pair[0], pair[1]) for pair in data]
    formatted_results = "\n".join(f"{pair[0]} * {pair[1]} = {result}" for pair, result in zip(data, results))
    return f"Karatsuba Multiplications:\n{formatted_results}"


def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    # Update file preview
    file_preview.delete(1.0, tk.END)
    file_preview.insert(tk.END, f"Selected File: {file_path}\n\n")
    try:
        with open(file_path, "r") as file:
            file_preview.insert(tk.END, file.read(500))  # Preview first 500 characters
    except Exception as e:
        file_preview.insert(tk.END, f"Error reading file: {e}")
        return

    # Process file for algorithms
    data = process_file(file_path)
    if not data:
        return

    # Execute the selected algorithm
    algorithm = algorithm_var.get()
    if algorithm == "Closest Pair of Points":
        result = apply_closest_pair(data)
    elif algorithm == "Karatsuba Multiplication":
        result = apply_karatsuba(data)
    else:
        result = apply_closest_pair(data) + "\n\n" + apply_karatsuba(data)

    # Display the results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)


# GUI Setup
root = tk.Tk()
root.title("Algorithm Application")

# Top white space for file preview
file_preview = tk.Text(root, height=10, width=50, wrap=tk.WORD)
file_preview.pack(pady=5)

# Bottom white space for results
result_text = tk.Text(root, height=15, width=50, wrap=tk.WORD)
result_text.pack(pady=5)

# Add radio buttons for algorithm selection
tk.Label(root, text="Select Algorithm:").pack(pady=5)
algorithm_var = tk.StringVar(value="Both")
tk.Radiobutton(root, text="Closest Pair of Points", variable=algorithm_var, value="Closest Pair of Points").pack(anchor="w")
tk.Radiobutton(root, text="Karatsuba Multiplication", variable=algorithm_var, value="Karatsuba Multiplication").pack(anchor="w")
tk.Radiobutton(root, text="Both", variable=algorithm_var, value="Both").pack(anchor="w")

# Add button to choose file
tk.Button(root, text="Choose File", command=choose_file).pack(pady=10)

# Run the GUI loop
root.mainloop()

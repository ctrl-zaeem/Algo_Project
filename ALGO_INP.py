import os
import random

# Generate random points for the closest pair of points algorithm
def generate_points(num_points, x_range, y_range):
    return [(random.randint(*x_range), random.randint(*y_range)) for _ in range(num_points)]

# Generate random integer pairs for the Karatsuba multiplication algorithm
def generate_integers(num_pairs, int_range):
    return [(random.randint(*int_range), random.randint(*int_range)) for _ in range(num_pairs)]

# Save data to a file
def save_to_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

# Main function to generate inputs
def main():
    try:
        # Create 'inputs' directory
        os.makedirs("inputs", exist_ok=True)
        print("Created 'inputs' directory.")

        # Generate and save inputs for closest pair of points
        for i in range(10):
            points = generate_points(100 + i * 10, (0, 1000), (0, 1000))
            filename = f"inputs/closest_points_{i + 1}.txt"
            save_to_file(filename, points)
            print(f"Generated: {filename}")

        # Generate and save inputs for integer multiplication
        for i in range(10):
            integers = generate_integers(100 + i * 10, (10**5, 10**6))
            filename = f"inputs/integer_multiplication_{i + 1}.txt"
            save_to_file(filename, integers)
            print(f"Generated: {filename}")

        print("Input files generated successfully.")
    except Exception as e:
        print(f"Error during file generation: {e}")

if __name__ == "__main__":
    main()

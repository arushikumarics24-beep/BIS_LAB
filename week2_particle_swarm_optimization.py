import random
import math


# ---------------------------------------------------------
# INPUT DATA
# ---------------------------------------------------------

# Solar radiation values (W/m²) for different time periods
solar_radiation = [300, 450, 600, 750, 850, 900, 800, 650, 500, 350]

# Solar altitude angle corresponding to each radiation value
# (in degrees)
solar_altitude = [10, 20, 30, 40, 50, 60, 55, 45, 30, 15]

# Possible tilt angle range of the solar panel
MIN_TILT = 0
MAX_TILT = 90

# Number of particles
NUM_PARTICLES = 30

# Number of iterations
MAX_ITERATIONS = 100

# PSO parameters
W = 0.7       # Inertia weight
C1 = 1.5      # Cognitive coefficient
C2 = 1.5      # Social coefficient


# ---------------------------------------------------------
# FITNESS FUNCTION
# ---------------------------------------------------------

def calculate_energy(tilt_angle):
    """
    Calculates the expected solar energy for a given
    solar panel tilt angle.

    Higher value = better tilt angle.
    """

    total_energy = 0

    for radiation, altitude in zip(solar_radiation, solar_altitude):

        # Difference between panel tilt and solar altitude
        angle_difference = abs(tilt_angle - altitude)

        # Convert angle to radians
        angle_difference = math.radians(angle_difference)

        # Effective radiation received by panel
        effective_radiation = radiation * max(0, math.cos(angle_difference))

        total_energy += effective_radiation

    return total_energy


# ---------------------------------------------------------
# PARTICLE CLASS
# ---------------------------------------------------------

class Particle:

    def __init__(self):
        # Random initial position (tilt angle)
        self.position = random.uniform(MIN_TILT, MAX_TILT)

        # Random initial velocity
        self.velocity = random.uniform(-5, 5)

        # Personal best position
        self.personal_best_position = self.position

        # Personal best fitness
        self.personal_best_fitness = calculate_energy(self.position)


# ---------------------------------------------------------
# INITIALIZE PARTICLES
# ---------------------------------------------------------

particles = [Particle() for _ in range(NUM_PARTICLES)]

# Find initial global best particle
global_best_particle = max(
    particles,
    key=lambda particle: particle.personal_best_fitness
)

global_best_position = global_best_particle.personal_best_position
global_best_fitness = global_best_particle.personal_best_fitness


# ---------------------------------------------------------
# PSO ALGORITHM
# ---------------------------------------------------------

for iteration in range(MAX_ITERATIONS):

    for particle in particles:

        # Generate random numbers
        r1 = random.random()
        r2 = random.random()

        # Update velocity
        particle.velocity = (
            W * particle.velocity
            + C1 * r1 * (
                particle.personal_best_position
                - particle.position
            )
            + C2 * r2 * (
                global_best_position
                - particle.position
            )
        )

        # Update position
        particle.position += particle.velocity

        # Keep position within valid tilt angle range
        particle.position = max(
            MIN_TILT,
            min(MAX_TILT, particle.position)
        )

        # Calculate new fitness
        fitness = calculate_energy(particle.position)

        # Update personal best
        if fitness > particle.personal_best_fitness:

            particle.personal_best_fitness = fitness
            particle.personal_best_position = particle.position

        # Update global best
        if fitness > global_best_fitness:

            global_best_fitness = fitness
            global_best_position = particle.position

    # Display progress
    if (iteration + 1) % 10 == 0:
        print(
            f"Iteration {iteration + 1}: "
            f"Best Tilt Angle = {global_best_position:.2f}° | "
            f"Energy = {global_best_fitness:.2f}"
        )


# ---------------------------------------------------------
# FINAL RESULT
# ---------------------------------------------------------

print("\n---------------------------------------")
print("       PSO OPTIMIZATION RESULT")
print("---------------------------------------")

print(f"Optimal Tilt Angle : {global_best_position:.2f} degrees")
print(f"Maximum Solar Energy: {global_best_fitness:.2f} Wh/m²")

print("---------------------------------------")
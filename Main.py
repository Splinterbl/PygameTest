import pygame
import random
import math

# Initialize pygame
pygame.init()

# Create the screen
screenWidth = 800
screenHeight = 600


# Particle Class
class Particle:
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.color = (255, 255, 255)
        self.thickness = 2
        self.velocity = 0
        self.angle = 0
        self.gravity = (0.001, math.pi)
        self.drag = 0.999
        self.elasticity = .75

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.velocity, self.angle) = addVectors((self.velocity, self.angle), self.gravity)
        self.velocity *= self.drag
        self.x += math.sin(self.angle) * self.velocity
        self.y -= math.cos(self.angle) * self.velocity

    def bounce(self):
        if self.x > screenWidth - self.size:
            self.x = 2 * (screenWidth - self.size) - self.x
            self.angle = - self.angle
            self.velocity *= self.elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.velocity *= self.elasticity

        if self.y > screenHeight - self.size:
            self.y = 2 * (screenHeight - self.size) - self.y
            self.angle = math.pi - self.angle
            self.velocity *= self.elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.velocity *= self.elasticity


# Add Vectors
def addVectors(vector1, vector2):
    length1, angle1 = vector1  # unpack vector 1
    length2, angle2 = vector2  # unpack vector 2
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = math.pi / 2 - math.atan2(y, x)
    return (length, angle)

# Find Particle
def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

# Create screen
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Create particles
number_of_particles = 10
my_particles = []

for n in range(number_of_particles):
    size = random.randint(10, 20)
    x = random.randint(size, screenWidth - size)
    y = random.randint(size, screenHeight - size)

    particle = Particle((x, y), size)
    particle.velocity = random.uniform(0, 2.5)
    particle.angle = random.uniform(0, math.pi * 2)
    #particle.gravity = (0.001, random.uniform(0,2* math.pi))

    my_particles.append(particle)

# Title and Icon
pygame.display.set_caption("Test Game")
icon = pygame.image.load("penis.png")
pygame.display.set_icon(icon)

selected_particle = None

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
            if selected_particle:
                grab_offset_x = mouseX - selected_particle.x
                grab_offset_y = mouseY - selected_particle.y
                dx = 0
                dy = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_particle:
                selected_particle.color = (255, 255, 255)
                selected_particle = None

    if selected_particle:
        selected_particle.color = (255, 0, 0)
        (mouseX, mouseY) = pygame.mouse.get_pos()

        dx = (mouseX - grab_offset_x) - selected_particle.x
        dy = (mouseY - grab_offset_y) - selected_particle.y

        selected_particle.x = mouseX - grab_offset_x
        selected_particle.y = mouseY - grab_offset_y


        selected_particle.angle = math.atan2(dy, dx) + math.pi/2
        selected_particle.velocity = math.hypot(dx, dy)

    # Background
    screen.fill((0, 50, 50))

    # Calculations
    for particle in my_particles:
        if particle != selected_particle:
            particle.move()
            particle.bounce()
        particle.display()

    # Update
    pygame.display.update()

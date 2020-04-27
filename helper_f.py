import numpy as np
from numpy import sqrt, sin, cos
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CONSTANT = 10
PI = np.pi

class Particle:
	def __init__(self, q, x, y):
		self.charge = q
		self.x = x
		self.y = y

#euler's method
def eulers(particles):

	#get the set of initial values which we will plug into euler's method function
	initial_coords = initial_values(particles)
	#create a list to store coordinates which we find using euler's method function
	coordinates = list()
	
	#loop over every initial value
	for t in range(0, len(initial_coords), 2):
		print("=", end="")
		if t == len(initial_coords) - 2:
			print(">")

		#add the particle coordinates to the list for case when y' is very large right at the initial value
		coordinates.append(initial_coords[t])
		#add initial value to coordinates list
		coordinates.append(initial_coords[t + 1])
		
		#make sure the coordinates being calculated are not off the screen or too close to and existing particle
		too_close = False
		too_far = False

		#determine the change in X for each iteration of euler's method
		change = 0.1

		#variable which checks whether we should flip direction of change variable mentioned above
		test = 0
		while not too_close and not too_far:
			
			field_x, field_y = yp_calc(particles, coordinates[-1][0], coordinates[-1][1])
			
			if field_x == 0:
				test = 0
				if coordinates[-1][1] - coordinates[-2][1] > 0:
					coords = (coordinates[-1][0], coordinates[-1][1] + 1)
				elif coordinates[-1][1] - coordinates[-2][1] < 0:
					coords = (coordinates[-1][0], coordinates[-1][1] - 1)
			else:
				#calculate y'(x_n)
				y_prime = field_y / field_x

				#if y' bigger than 10 then switch the direction of change variable
				if y_prime >= 11.5 or y_prime <= -11.5:	
					test += 1
					if coordinates[-1][1] - coordinates[-2][1] < 0:
						coords = (coordinates[-1][0], coordinates[-1][1] - 1)
					elif coordinates[-1][1] - coordinates[-2][1] > 0:
						coords = (coordinates[-1][0], coordinates[-1][1] + 1)

				else:
					if test > 1:
						change = -change
					if y_prime < 11.5 and y_prime > -11.5:
						test=0
						#find y_n+1 and x_n+1
						x_c = coordinates[-1][0] + change
						y_c = coordinates[-1][1] + change * y_prime

						coords = (x_c, y_c)

			coordinates.append(coords)
			
			for i in particles:
				if (coords[0] - i.x) ** 2 + (coords[1] - i.y) ** 2 <= 9:
					too_close = True
				if coords[0] > 1000 or coords[0] < 0 or coords[1] > 1000 or coords[1] < 0:
					too_far = True
		
		too_close = False
		too_far = False
		coordinates.append(initial_coords[t])
		coordinates.append(initial_coords[t + 1])
		change = -0.1
		test = 0
		while not too_close and not too_far:
			field_x, field_y = yp_calc(particles, coordinates[-1][0], coordinates[-1][1])
			
			if field_x == 0:
				test = 0
				if field_y > 0:
					coords = (coordinates[-1][0], coordinates[-1][1] + 1)
				if field_y < 0:
					coords = (coordinates[-1][0], coordinates[-1][1] - 1)
			else:
				#calculate y'(x_n)
				y_prime = field_y / field_x

				#if y' bigger than 10 then switch the direction of change variable
				if y_prime >= 11.5 or y_prime <= -11.5:
					test += 1
					if coordinates[-1][1] - coordinates[-2][1] < 0:
						coords = (coordinates[-1][0], coordinates[-1][1] - 1)
					elif coordinates[-1][1] - coordinates[-2][1] > 0:
						coords = (coordinates[-1][0], coordinates[-1][1] + 1)
				else:
					if test > 1:
						change = -change
					if y_prime < 15 and y_prime > -15:
						test=0
						#find y_n+1 and x_n+1
						x_c = coordinates[-1][0] + change
						y_c = coordinates[-1][1] + change * y_prime

						coords = (x_c, y_c)

			coordinates.append(coords)
			for i in particles:
				if (coords[0] - i.x) ** 2 + (coords[1] - i.y) ** 2 <= 9:
					too_close = True
				if coords[0] > 1000 or coords[0] < 0 or coords[1] > 1000 or coords[1] < 0:
					too_far = True

	return coordinates

#draw everything to the screen
def draw(screen, coordinates, particles):
	screen.fill(BLACK)
	
	#draw the field lines
	for i in coordinates:
		pygame.draw.rect(screen, WHITE, (int(i[0]), int(i[1]), 1, 1), 1)

	#draw the particles
	for k in particles:
		pygame.draw.circle(screen, RED, (k.x, k.y), 5)
	
	pygame.display.flip()

#returns a list of initial values for euler's method
def initial_values(particles):
	
	#initialize an empty list to hold the coords
	initial_values = list()

	#loop through each particle
	for particle in particles:
		
		#get the initial coordinates to create new ones off of
		particle_coords = (particle.x, particle.y)
		
		#how many initial points around the circle 
		split = 16
		for i in range(split):
			
			#multiplier to create even spaced IVs around circle
			const = 2 * PI / split
			
			#calculate the initial coords based off of the particle's coordinates with radius 8
			new_coordsx = particle_coords[0] + 8 * sin(const * i)
			new_coordsy = particle_coords[1] + 8 * cos(const * i)
			new_coordsx = int(new_coordsx)
			new_coordsy = int(new_coordsy)
			
			#append the initial coords to list
			initial_values.append((particle.x, particle.y))
			initial_values.append((new_coordsx, new_coordsy))

	#return calculated coordinates to feed into euler function
	return initial_values

def yp_calc(particles, x, y):
	#set initial field for each point
		field_x = 0
		field_y = 0
		
		for particle in particles:
			#initialize some constants
			q = particle.charge
			k = CONSTANT
			
			#calculate dx, dy
			delta_x = x - particle.x
			delta_y = y - particle.y
			
			#calculate radius and electric field magnitude
			r = sqrt(delta_x ** 2 + delta_y ** 2)
			E_magnitude = q / (k * r**3)
			
			#add EFM for x and y to net EFM vector at x_n
			field_x += E_magnitude * delta_x
			field_y += E_magnitude * delta_y

		#give me the magnitude of the field in x and y directions
		return field_x, field_y

from helper import Particle, eulers, draw, initial_values
import pygame

def main():
	
	#initialize pygame and set up screen and clock
	pygame.init()
	screen = pygame.display.set_mode((1000, 1000))
	clock = pygame.time.Clock()

	#add some charged particles with which to create the field line graph
	particle1 = Particle(8, 400, 400)
	particle2 = Particle(8, 600, 600)
	particle3 = Particle(-8, 400, 600)
	particle4 = Particle(8, 600, 400)
	particles = [particle1, particle2]

	#calculate the coordinates which will be drawn to the screen using euler's method
	coordinates = eulers(particles)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		#draw coordinates and particles to the screen
		draw(screen, coordinates, particles)

		#draw at 30FPS
		clock.tick(30)

if __name__ == "__main__":
	main()

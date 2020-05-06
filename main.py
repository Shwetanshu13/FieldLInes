from helper_f import Particle, eulers, draw, initial_values
import pygame

def main():
	
	#initialize pygame and set up screen and clock
	pygame.init()
	screen = pygame.display.set_mode((1000, 1000))
	clock = pygame.time.Clock()

	#add some charged particles with which to create the field line graph
	p1 = Particle(-12, 400, 400)
	p2 = Particle(8, 600, 600)
	p3 = Particle(-8, 400, 600)
	p4 = Particle(8, 600, 400)
	particles = [p1, p2, p3, p4]

	#calculate the coordinates which will be drawn to the screen using euler's method
	coordinates = eulers(particles)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		#draw coordinates and particles to the screen
		draw(screen, coordinates, particles)

		clock.tick(30)

if __name__ == "__main__":
	main()

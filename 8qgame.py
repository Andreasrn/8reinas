#Juego de las 8 reinas
#Autora: Andrea Serrano (@ThymineDNA)
#Uso: Ejecutar sin argumentos. Se mostrará interfaz gráfica

import pygame,sys
from pygame.locals import *

pygame.init()

#------Algunas constantes útiles

FPS = 15
WINDOWWIDTH = 500 #En pixels
WINDOWHEIGHT = 500  #En pixels
COLUMS = 8
RED = (255,0,0)
ROWS = 8 
TAMCASILLA = 60 #En pixels
FPSCLOCK = pygame.time.Clock()

#------Crear el tablero

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
pygame.display.set_caption('Juego de las 8 reinas')

#------Variables necesarias

tablero = pygame.image.load('board.png')
reina = pygame.image.load('queen.png')
cerveza = pygame.image.load('beer.png')

hayReina = [[False for x in range(8)] for y in range(8)] #Contiene falso si en la casilla [x][y] no hay una reina.

reinasPuestas = 0

#------Funciones útiles
def finDeJuego():
	if reinasPuestas == 8:
		return True
	else:
		return False


def clickEnCasilla(mousex,mousey): #Según Gimp, los bordes son 10 pixels en cada lado.

	if mousex > 10 and mousex < 490 and mousey > 10 and mousey < 490:
		return True
	return False

def dibujarReinas():

	for x in range(8):
		for y in range(8):
			if hayReina[x][y]:
				DISPLAYSURF.blit(reina,(x*60 +10, y*60+10))

def invertirCasilla(x,y): #Si hay una reina, se quita. Si no había, se pone.
	
	global reinasPuestas

	if hayReina[x][y]:
		hayReina[x][y] = False
		reinasPuestas = reinasPuestas-1
	else:
		hayReina[x][y] = True
		reinasPuestas = reinasPuestas+1

def movimientoLegal(x,y):
	if hayReina[x][y]: #Siempre es legal quitar una reina
		return True
	else:
		#Comprobamos la fila
		for col in range(8):
			if hayReina[col][y]:
				return False

		#Comprobamos la columna
		for fila in range(8):
			if hayReina[x][fila]:
				return False
		
		#Comprobamos las diagonales
		col = x
		fil = y
		while col < 8 and fil < 8:
			if hayReina[col][fil]:
				return False
			
			col = col+1
			fil = fil+1

		col = x
		fil = y
		while col >= 0 and fil >= 0:
			if hayReina[col][fil]:
				return False

			col = col-1
			fil = fil-1

		col = x
		fil = y

		while col >= 0 and fil < 8:
			if hayReina[col][fil]:
				return False

			col = col-1
			fil = fil+1

		col = x
		fil = y

		while col < 8 and fil >= 0:
			if hayReina[col][fil]:
				return False

			col = col+1
			fil = fil-1
		#Si hemos llegado hasta aquí, el movimiento es legal
		return True

#------Loop principal

while True:

	DISPLAYSURF.blit(tablero,(0,0)) #Dibujar fondo
	dibujarReinas() #Dibujar reinas

	if finDeJuego():
		DISPLAYSURF.blit(cerveza,(0,0))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	else:

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				mousex,mousey = event.pos
	
				if clickEnCasilla(mousex,mousey):
	
					#Calculamos con el cociente entero la casilla
					x = int((mousex - 10)/TAMCASILLA)
					y = int((mousey - 10)/TAMCASILLA)
	
					#Hay un pequeño margen en la última casilla que no cuadra la división. Parche malo.
					if x == 8:
						x = 7
					if y == 8:
						y = 7
	
	
					if movimientoLegal(x,y):
						invertirCasilla(x,y) 
					else:
						#Colorear en rojo la casilla para mostrar que es un movimiento no permitido
	
						pygame.draw.rect(DISPLAYSURF, RED, (x*60 + 10,y*60 + 10,TAMCASILLA,TAMCASILLA))

	pygame.display.update()
	FPSCLOCK.tick(FPS)


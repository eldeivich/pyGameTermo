import pygame, sys
from pygame.locals import *

class Termometro():
    def __init__(self):
        self.custome = pygame.image.load("images/termometro1.jpg")
        
    def convertir(self, grados, toUnidad):
        resultado = 0
        if toUnidad == 'F':
            resultado = grados * 9/5 + 32
        elif toUnidad == 'C':
            resultado = (grados - 32) * 5/9
        else:
            resultado = grados
            
        return "{:10.2f}".format(resultado)
        
class Selector():
    __tipoUnidad = None
    
    def __init__(self, unidad="C"):
        self.__customes = []
        self.__customes.append(pygame.image.load("images/selectorF.jpg"))
        self.__customes.append(pygame.image.load("images/selectorC.jpg"))
        
        self.__tipoUnidad = unidad
        
    def custome(self):
        if self.__tipoUnidad == 'F':
            return self.__customes[0]
        else:
            return self.__customes[1]
        
    def change(self):
        if self.__tipoUnidad == 'F':
            self.__tipoUnidad = 'C'
        else:
            self.__tipoUnidad = 'F'
            
    def unidad(self):
        return self.__tipoUnidad
        
        
class NumberInput():
    __value = 0
    __strValue = ""
    __position = [0, 0]
    __size = [0, 0]
    __pointsCount = 0
    
    def __init__(self, value=0):
        self.__font = pygame.font.SysFont("Arial", 24)
        self.value(value)
        
        '''
        try:
            self.__strValue = float(value)
            self.__strValue = str(value)
        except:
            pass
        '''
        
    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.unicode.isdigit() and len (self.__strValue) <= 10 or (event.unicode == '.' and self.__pointsCount == 0):
                self.__strValue += event.unicode
                self.value(self.__strValue)
                if event.unicode == '.':
                    self.__pointsCount +=1
            elif event.key == K_BACKSPACE:
                if self.__strValue[-1] == '.':
                    self.__pointsCount -= 1
                self.__strValue = self.__strValue[:-1]
                self.value(self.__strValue)
                
        
    def render(self):
        textBlock = self.__font.render(self.__strValue, True, (74, 74, 74))
        rect = textBlock.get_rect()
        rect.left = self.__position[0]
        rect.top = self.__position[1]
        rect.size = self.__size
        
        '''
        return {
                "fondo": rect,
                "texto": textBlock
            }
        '''
        return (rect, textBlock)
        
    def value(self, val=None):
        if val==None:
            return self.__value
        else:
            val = str(val)
            print(val, "cadena")
            try:
                self.__value = float(val)
                self.__strValue = val
                if '.' in self.__strValue:
                    self.__pointsCount = 1
                else:
                    self.__pointsCount = 0
            except:
                pass
            
    def width(self, val=None):
        if val == None:
            return self.__size[0]
        else:
            try:
                self.__size[0] = float(val)
            except:
                pass
            
    def height(self, val=None):
        if val == None:
            return self.__size[1]
        else:
            try:
                self.__size[1] = float(val)
            except:
                pass
            
    def size(self, val=None):
        if val == None:
            return self.__size
        else:
            try:
                self.__size = [float(val[0]), float(val[1])]
            except:
                pass
            
    def posX(self, val=None):
        if val == None:
            return self.__position[0]
        else:
            try:
                self.__position[0] = float(val)
            except:
                pass
            
    def posY(self, val=None):
        if val == None:
            return self.__position[1]
        else:
            try:
                self.__position[1] = float(val)
            except:
                pass
            
    def pos(self, val=None):
        if val == None:
            return self.__position
        else:
            try:
                self.__position = [float(val[0]), float(val[1])]
            except:
                pass

class mainApp():
    termometro = None
    entrada = None
    selector = None
    
    def __init__(self):
        self.__screen = pygame.display.set_mode((310, 460))
        pygame.display.set_caption("Termómetro")
        
        self.termometro = Termometro()
        self.entrada = NumberInput('Monchu')
        self.entrada.pos((135, 58))
        self.entrada.size((164, 28))
        
        self.selector = Selector()
        
    def __on_close(self):
        pygame.quit()
        sys.exit()
        
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__on_close()
                    
                self.entrada.on_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.selector.change()
                    grados = self.entrada.value()
                    nuevaUnidad = self.selector.unidad()
                    temperatura = self.termometro.convertir(grados, nuevaUnidad)
                    self.entrada.value(temperatura)
                    
            # Pintamos el fondo de pantalla
            self.__screen.fill((239, 227, 175))
            
            # Pintamos el termómetro en su posición
            self.__screen.blit(self.termometro.custome, (10, 14))
            
            # Pintamos el cuadro de texto
            text = self.entrada.render() # Obtenemos rectángulo blanco y foto de texto y lo asignamos a text
            pygame.draw.rect(self.__screen, (255, 255, 255), text[0]) # Creamos el rectángulo blanco con sus datos (posición y tamaño) text[0]
            self.__screen.blit(text[1], self.entrada.pos()) # Pintamos la foto del texto (text[1])
            
            # Pintamos el selector
            self.__screen.blit(self.selector.custome(), (142, 153))
            
            pygame.display.flip()
        
if __name__ == '__main__':
    pygame.font.init()
    app = mainApp()
    app.start()
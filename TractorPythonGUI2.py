import pygame
import asyncio
import uuid
from bleak import BleakClient

#Bluetooth module address and UUID
address = "a0:6c:65:cf:7f:8f"
MODEL_NBR_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"
SERVICE_NBR_UUID = "0000FFE0-0000-1000-8000-00805F9B34FB"

#Set screen width and Height
SCREEN_HEIGHT = 750
SCREEN_WIDTH = 1500

#Initialize the screen and set a screen caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

pygame.font.init()
textfont = pygame.font.SysFont("monospace", 100)

#Load each button image from the PNG file
START_BUTTON = pygame.image.load('START.PNG')
STOP_BUTTON = pygame.image.load('STOP.PNG')
TRIP_REPORT_BUTTON = pygame.image.load('Trip_Report.PNG')
BLACK_TAPE_COUNT_BUTTON = pygame.image.load('Black_Tape_Count.PNG')
ELAPSED_TIME_BUTTON = pygame.image.load('Elapsed_Time.PNG')
DISTANCE_TRAVELED_BUTTON = pygame.image.load('Distance_Traveled.PNG')
SPEED_BUTTON = pygame.image.load('Speed.PNG')
BLANK = pygame.image.load("Blank.PNG")

class Button():
    #This function is similar to a constructor
    def __init__(self, x, y, image, scale):
        width = image.get_width()       #gets the image width and height
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))   #scales the image based on the user input
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)      #sets the top left of the rectangle to the user's x and y inputs
        self.clicked = False

    def draw(self):
        action = False

        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#Creating the buttons neccessary
start_button = Button(547.5, 50, START_BUTTON, 1.0)
stop_button = Button(466.5, 200, STOP_BUTTON, 1.0)
trip_report_button = Button(555, 350, TRIP_REPORT_BUTTON, 1.0)
black_tape_count_button = Button(613.5, 475, BLACK_TAPE_COUNT_BUTTON, 1.0)
elapsed_time_button = Button(1150, 475, ELAPSED_TIME_BUTTON, 1.0)
distance_traveled_button = Button(100, 475, DISTANCE_TRAVELED_BUTTON, 1.0)
speed_button = Button(100, 100, SPEED_BUTTON, 1.0)
blank = Button(665, 550, BLANK, 1.0)

screen.fill((229, 229, 229)) #Used to achieve the soft white background
global_black_tape_count = '999'

async def main(address):
    client = BleakClient(address)

    def callback(sender: client, data: bytearray):
        black_tape_count = data.decode()
        if (black_tape_count != global_black_tape_count):
            blank.draw()
            textTBD = textfont.render(black_tape_count, 1, (0, 0, 0))
            screen.blit(textTBD, (665, 550))
            global_black_tape_count = black_tape_count
        print("hello")
        print(black_tape_count)
    
        
    try:
        await client.connect()
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))
        run = True
        while run:

            await client.start_notify(MODEL_NBR_UUID, callback)

            #draws all the buttons on the screen
            if start_button.draw() == True:
                print("START")
                start = '1'
                bytes_start = bytes(start, 'ascii', errors = 'ignore')
                print('Byte converstion:', bytes_start)
                await client.write_gatt_char(MODEL_NBR_UUID, bytes(start, 'ascii', errors = 'ignore'), response = False)

            if stop_button.draw() == True:
                print("STOP")
                stop = '0'
                bytes_stop = bytes(stop, 'ascii', errors = 'ignore')
                print('Byte converstion:', bytes_stop)
                await client.write_gatt_char(MODEL_NBR_UUID, bytes(stop, 'ascii', errors = 'ignore'), response = False)

            trip_report_button.draw()
            black_tape_count_button.draw()
            elapsed_time_button.draw()
            distance_traveled_button.draw()
            speed_button.draw()
            blank.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update() #Updates the events from the user
        pygame.quit()  
    except Exception as e:
        print(e)

    await client.disconnect()


asyncio.run(main(address))


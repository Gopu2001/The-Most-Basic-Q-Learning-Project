import pygame, sys, time, numpy, random

# COLORS
WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 235)
GREEN = (0, 150, 0)
RED = (255, 75, 75)
YELLOW = (255, 255, 51)
GROUND = 100
WIDTH, HEIGHT = 850, 300
ALPHA = 0.1
GAMMA = 0.8
epsilon = 0.4
EPSILON_RATE = 0.95
STATES = [0, 150, 300, 450, 600, 750]
CONTROL = False
tts = 0

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car on Ground")

#score, counter = 0, 0
counter = 0

def draw_ground():
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - GROUND, WIDTH, GROUND))

class Car:
    def __init__(self):
        self.color = RED
        self.next_x = None
        self.height = 50
        self.length = 100
        self.y = HEIGHT - GROUND - self.height
        self.x = 0
    def step(self, action):
        if action == 0:
            self.x -= 150
        if action == 1:
            self.x += 150
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.length, self.height))
    def collect(self, coin):
        global score, counter
        counter += 1
        #score += 5
        coin.die()

class Coin:
    def __init__(self, x):
        self.color = YELLOW
        self.radius = 20
        self.off_ground = 5
        self.alive = True
        self.x = x
        self.y = HEIGHT - GROUND - self.radius - self.off_ground
    def die(self):
        self.alive = False
    def draw(self):
        if self.alive:
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius, 0)

# initialize the q_table and rewards table

#q_table = numpy.zeros((3, 2), dtype=int)
q_table = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
countxs5 = 0
numWinner = 0
for i in range(1, 101):
    print("Generation: {}".format(i), end="\t")
    car = Car()
    coins = [Coin(STATES[1]), Coin(STATES[2]), Coin(STATES[3]), Coin(STATES[4]), Coin(STATES[5])]
    rewards = [[-100, 5], [-5, 5], [-5, 5], [-5, 5], [-5, 5], [-5, 100]]
    counter = 0
    for j in range(i):
        screen.fill(LIGHT_BLUE)
        draw_ground()
        car.draw()
        if CONTROL:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        car.left()
                    if event.key == pygame.K_RIGHT:
                        car.right()
        
        # Updating the q_table
        '''
        Function: q_table[state][action] = rewards_$[state][action] + GAMMA * max(q_table[next_state][all_actions_for_next_state])
        '''
        
        # find current state
        state = STATES.index(car.x)
        
        # find current action
        epsComp = random.random()
        action = None
        if epsilon > epsComp:
            action = round(random.random())
        else:
            action = q_table[state].index(max(q_table[state]))
        
        for coin in coins:
            if car.x == coin.x and coin.alive:
                car.collect(coin)
                rewards[state-1][1] = 0
            coin.draw()
        
        #print(str(state) + ", " + str(action), end="\t")
        #car.step(action)
        #pygame.display.update()
        if counter == 5 or state == 5:
            pygame.display.update()
            #print("WINNER!", end='')
            numWinner += 1
            time.sleep(tts)
            break
        
        if action == 0:
            car.next_x = car.x - 150
        else:
            car.next_x = car.x + 150
        
        try:
            next_state = STATES.index(car.next_x)
        except ValueError:
            if car.next_x == 0:
                q_table[state][action] = rewards[state][action] + GAMMA * -100
                break
            else:
                q_table[state][action] = rewards[state][action] + GAMMA * 100
                break
        
        q_table[state][action] = rewards[state][action] + GAMMA * max(q_table[next_state])
        
        if (state == 0 and action == 0):
            break
        car.step(action)
        pygame.display.update()
        epsilon *= EPSILON_RATE
        time.sleep(tts)
    print()

print("The number of winners are", numWinner)
#print(q_table)
pygame.quit()
sys.exit()

'''
definitions:
State: 0 = 0px (x), 1 = 300px (x), 2 = 600px (x)
Action: 0 = go left, 1 = go right


            State
        0       1       2
        
    0   0       0       0
A   
    1   0       0       0


            Reward T1
        0       1       2
        
    0   -100    0       0
A   
    1   0       5       -100


            Reward T2
        0       1       2
        
    0   -100    5       0
A   
    1   0       0       -100

'''
'''
while True:
    screen.fill(LIGHT_BLUE)
    draw_ground()
    car.draw()
    coin.draw()
    if (coin.RIGHT and self.x + self.length >= coin.x - coin.radius) or ((not coin.RIGHT) and self.x <= coin.x + coin.radius):
        car.collect(coin)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.left()
            if event.key == pygame.K_RIGHT:
                car.right()
    pygame.display.update()
    if counter == 5:
        pygame.quit()
        print("WINNER!")
        score = 100
        sys.exit()
    elif car.x < 0 or car.x + car.length > WIDTH:
        pygame.quit()
        print("YOU LOST")
        score = -100
        sys.exit()
    else:
        time.sleep(0.005)
'''

import numpy as np
import matplotlib.pyplot as plt
import random
import time

# 시뮬레이션 설정
grid_size = 20
num_ants = 50
food_position = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
nest_position = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
pheromone = np.zeros((grid_size, grid_size))

# 개미 클래스 정의
class Ant:
    def __init__(self):
        self.position = list(nest_position)
        self.has_food = False
    
    def move(self):
        if self.has_food:
            # 둥지 방향으로 이동 (페로몬 무시)
            self.move_towards(nest_position)
            if tuple(self.position) == nest_position:
                self.has_food = False
        else:
            # 음식 방향으로 이동 (페로몬 따라가기)
            if random.random() < 0.8:  # 80% 확률로 페로몬 따라감
                self.follow_pheromone()
            else:
                self.move_random()
            if tuple(self.position) == food_position:
                self.has_food = True
                pheromone[self.position[0], self.position[1]] += 5

    def move_random(self):
        direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self.position[0] = max(0, min(grid_size - 1, self.position[0] + direction[0]))
        self.position[1] = max(0, min(grid_size - 1, self.position[1] + direction[1]))

    def follow_pheromone(self):
        max_phero = -1
        best_move = None
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = self.position[0] + dx, self.position[1] + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                if pheromone[nx, ny] > max_phero:
                    max_phero = pheromone[nx, ny]
                    best_move = (dx, dy)
        
        if best_move:
            self.position[0] += best_move[0]
            self.position[1] += best_move[1]
        else:
            self.move_random()
    
    def move_towards(self, target):
        if self.position[0] < target[0]:
            self.position[0] += 1
        elif self.position[0] > target[0]:
            self.position[0] -= 1
        if self.position[1] < target[1]:
            self.position[1] += 1
        elif self.position[1] > target[1]:
            self.position[1] -= 1

# 개미 생성
ants = [Ant() for _ in range(num_ants)]

def update_pheromone():
    global pheromone
    pheromone *= 0.95  # 페로몬이 서서히 감소

def plot_simulation():
    plt.imshow(pheromone, cmap='inferno', origin='lower')
    plt.scatter(food_position[1], food_position[0], color='green', label='Food', s=100)
    plt.scatter(nest_position[1], nest_position[0], color='blue', label='Nest', s=100)
    for ant in ants:
        plt.scatter(ant.position[1], ant.position[0], color='white', s=10)
    plt.legend()
    plt.show()

# 시뮬레이션 실행
for step in range(100):
    for ant in ants:
        ant.move()
    update_pheromone()
    if step % 10 == 0:
        plot_simulation()
    time.sleep(0.1)

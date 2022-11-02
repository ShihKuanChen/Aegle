import pygame
import random
import time

class App:
    def __init__(
        self, width, height, fullSscreen, fps, memory_size,
        log_path, question_path, start_img_path, mode, title = None):

        self.width = width
        self.height = height
        self.fps = fps
        self.memory_size = memory_size
        self.log_path = log_path
        self.question_path = question_path
        self.start_img_path = start_img_path
        self.mode = mode
        self.memory = []
        self.tessellated_path = './images/tessellated.png'

        self.read_question('./question.txt')

        if title == None:
            title = 'My pygame'

        pygame.init()
        pygame.display.set_caption(title)

        self.divider = [
            '==================',
            '==================',
            '==================']

        self.random_indexs = [i for i in range(len(self.question))]
        random.shuffle(self.random_indexs)
        self.random_indexs.insert(0, self.random_indexs[-1])

        self.clock = pygame.time.Clock()

        if fullSscreen:
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

        else:
            self.window = pygame.display.set_mode((self.width, self.height))

        if self.mode == 1:
            self.waiting_screen = (255, 255, 255)

        elif self.mode == 2:
            self.waiting_screen = (0, 0, 0)

        elif self.mode == 3:
            self.waiting_screen = pygame.transform.scale(pygame.image.load(self.tessellated_path).convert(), self.window.get_size())

        else:
            raise TypeError

        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        self.window.blit(self.background, (0, 0))
        self.update()

    def __call__(self):
        self.game_loop()
    
    def game_loop(self):
        for path in self.start_img_path:
            self.done = False

            image = pygame.transform.scale(pygame.image.load(path).convert(), self.window.get_size())
            self.background = self.background.convert()
            self.background.blit(image, (0, 0))
            self.window.blit(self.background, (0, 0))

            while not self.done:
                self.clock.tick(self.fps)
                self.update()
                self.is_done()
                self.get_user_input()

        if self.mode == 3:
            self.background.blit(self.waiting_screen, (0, 0))

        else:
            self.background.fill(self.waiting_screen)

        self.window.blit(self.background, (0, 0))
        self.update()

        for index in range(len(self.random_indexs)):
            self.done = False
            sleep_time = round(random.random() * 4 + 3) * 1000

            pygame.time.wait(sleep_time)

            time_a = time.time()

            self.background = self.background.convert()
            self.background.fill(self.question[self.random_indexs[index]])
            self.window.blit(self.background, (0, 0))

            self.update()

            while not self.done:
                self.clock.tick(self.fps)
                self.update()
                self.is_done()
                self.get_user_input()

                if self.done:
                    time_b = time.time()
                    print(f'''{self.question[self.random_indexs[index]]} time: {time_b - time_a}''')
                    
                    if index != 0:
                        self.write_log(self.question[self.random_indexs[index]], self.mode, time_b - time_a)

            self.background = self.background.convert()
            if self.mode == 3:
                self.background.blit(self.waiting_screen, (0, 0))

            else:
                self.background.fill(self.waiting_screen)
            self.window.blit(self.background, (0, 0))
            self.update()

        pygame.quit()

        self.write_log(self.divider, self.divider[0], self.divider[0])
        print('測試結束!')
    
    def write_log(self, rgb, mode, time):
        with open(self.log_path, "a") as f:
            f.write(f"{rgb[0]},{rgb[0]},{rgb[0]},{mode},{time}\n")
    
    def add_memory(self, data):
        self.memory.append(data)
        if len(self.memory) >= self.memory_size:
            self.memory.pop(0)
    
    def get_user_input(self):
        all_key = pygame.key.get_pressed()
        if all_key[pygame.K_SPACE] and True not in self.memory:
            self.add_memory(True)
            self.done = True
        
        else:
            self.add_memory(False)

    def read_question(self, path):
        question = []
        with open(path, 'r') as f:
            file = f.read()
            file = file.replace(" ", "")
            file = file.split("\n")
            file = list(map(lambda x: x.split(","), file))
            
            for i in file:
                question.append([int(j) for j in i])

            self.question = question
    
    def is_done(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        pygame.display.update()

if __name__ == '__main__':
    width = 0
    height = 0
    full_screen = True
    fps = 10000
    memory_size = 50
    log_path = './log.txt'
    question_path = './question.txt'
    mode = int(input('請輸入模式, 1 = 白色, 2 = 黑色, 3 = 棋盤格: '))

    app = App(width, height, full_screen, fps, memory_size, log_path, question_path, [
        './images/start1.png',
        './images/start2.png'], mode, 'experiment')

    app()

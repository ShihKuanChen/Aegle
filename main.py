from collections import namedtuple
import pygame
import random
import time

class App:
    def __init__(
        self, width, height, fullSscreen, fps, memory_size,
        log_path, question_path, start_img_path, mode,
        done_img_path, tessellated_path, title = None):

        self.width = width
        self.height = height
        self.fps = fps
        self.memory_size = memory_size
        self.log_path = log_path
        self.question_path = question_path
        self.start_img_path = start_img_path
        self.mode = mode
        self.done_img_path = done_img_path
        self.tessellated_path = tessellated_path
        self.log_data = namedtuple("log_data", ["rgb", "mode", "color", "time"])
        self.memory = []
        self.log = []

        self._read_question("./question.txt")

        if title == None:
            title = "My pygame"

        pygame.init()
        pygame.display.set_caption(title)

        self.divider = [
            "=====",
            "=====",
            "====="]

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
        self._update()

    def __call__(self):
        self._game_loop()

    def _game_loop(self):
        for path in self.start_img_path:
            self.done = False

            image = pygame.image.load(path).convert()
            image = pygame.transform.scale(image, self.window.get_size())

            self._show_image(image)
            self._wait_input()

        if self.mode == 3:
            self.background.blit(self.waiting_screen, (0, 0))

        else:
            self.background.fill(self.waiting_screen)

        self.window.blit(self.background, (0, 0))
        self._update()

        for index, random_index in enumerate(self.random_indexs):
            self.done = False
            sleep_time = round(random.random() * 4 + 3) * 1000

            pygame.time.wait(sleep_time)

            time_a = time.time()

            self.background = self.background.convert()
            self.background.fill(self.question[random_index])
            self.window.blit(self.background, (0, 0))

            self._wait_input()

            time_b = time.time()
            reaction_time = time_b - time_a
            rgb = self.question[random_index]
            print(f"{rgb} time: {reaction_time}")
                    
            if index != 0:
                color = self._rgb_to_chinese(rgb)
                self._write_log(rgb, self.mode, color, reaction_time)

            self.background = self.background.convert()
            if self.mode == 3:
                self.background.blit(self.waiting_screen, (0, 0))

            else:
                self.background.fill(self.waiting_screen)

            self.window.blit(self.background, (0, 0))
            self._update()

        self._done()
        print("測試結束!")
    
    def _rgb_to_chinese(self, color):
        if color == [255, 0, 0]:
            return "紅色"
        
        elif color == [255, 170, 0]:
            return "橘色"
        
        elif color == [255, 255, 0]:
            return "黃色"
        
        elif color == [170, 255, 0]:
            return "檸檬綠色"
        
        elif color == [0, 255, 0]:
            return "綠色"
        
        elif color == [0, 255, 170]:
            return "春綠色"

        elif color == [0, 255, 255]:
            return "青色"
        
        elif color == [0, 170, 255]:
            return "蔚藍色"
        
        elif color == [0, 0, 255]:
            return "藍色"
        
        elif color == [170, 0, 255]:
            return "紫羅蘭色"
        
        elif color == [255, 0, 255]:
            return "洋紅色"
        
        elif color == [255, 0, 170]:
            return "玫瑰紅色"

    def _show_image(self, image):
        self.background = self.background.convert()
        self.background.blit(image, (0, 0))
        self.window.blit(self.background, (0, 0))

    def _wait_input(self):
        while not self.done:
            self.clock.tick(self.fps)
            self._update()
            self._is_done()
            self._get_user_input()

    def _write_log_file(self, rgb, mode, color, time):
        with open(self.log_path, "a", encoding = "utf-8") as f:
            f.write(f"{rgb[0]},{rgb[1]},{rgb[2]},{mode},{color},{time}\n")

    def _write_log(self, rgb, mode, color, time):
        # self.log.append((rgb, mode, color, time))
        self.log.append(self.log_data(rgb, mode, color, time))
    
    def _sort(self, data):
        output = sorted(data, key = lambda x: x.time)
        return output
    
    def _add_memory(self, data):
        self.memory.append(data)

        if len(self.memory) >= self.memory_size:
            self.memory.pop(0)
    
    def _get_user_input(self):
        all_key = pygame.key.get_pressed()

        if all_key[pygame.K_SPACE] and True not in self.memory:
            self._add_memory(True)
            self.done = True
        
        else:
            self._add_memory(False)

    def _read_question(self, path):
        question = []

        with open(path, "r", encoding = "utf-8") as f:
            file = f.read()
            file = file.replace(" ", "")
            file = file.split("\n")
            file = list(map(lambda x: x.split(","), file))
            
            for i in file:
                question.append([int(j) for j in i])

            self.question = question
    
    def _is_done(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done()

    def _done(self):
        self.log = self._sort(self.log)
        
        for data in self.log:
            self._write_log_file(data.rgb, data.mode, data.color, data.time)
        
        self._write_log_file(
            self.divider, self.divider[0], self.divider[0],
            self.divider[0])
        
        self.done = False

        image = pygame.image.load(self.done_img_path).convert()
        image = pygame.transform.scale(image, self.window.get_size())

        self._show_image(image)
        self._wait_input()
        
        pygame.quit()

    def _update(self):
        pygame.display.update()

if __name__ == "__main__":
    width = 0
    height = 0
    full_screen = True
    fps = 10000
    memory_size = 65
    log_path = "./log.txt"
    question_path = "./question.txt"
    mode = int(input("請輸入模式, 1 = 白色, 2 = 黑色, 3 = 棋盤格: "))

    app = App(
        width, height, full_screen, fps, memory_size, log_path, question_path,
        ["./images/start1.png", "./images/start2.png", "./images/start3.png"],
        mode, "./images/done.png", "./images/tessellated.png", "experiment")

    app()

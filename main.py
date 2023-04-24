import pygame
from random import randint
from pandas import read_excel

words = read_excel("./words.xlsx")


class word:
    def __init__(self, infinitiv, presens, preteritum, supinum, trans):
        self.__swedish = [infinitiv, presens, preteritum, supinum]
        self.__shown = ["#"] * 4
        self.__colours = ["black"] * 4
        self.__trans = trans
        self.__index = -1

        i = randint(0, 3)
        self.__shown[i] = self.__swedish[i]
        self.__colours[i] = "blue"

    def __iter__(self):
        return self

    def __next__(self):
        self.__index += 1
        if self.__index >= len(self.__swedish):
            self.__index = -1
            raise StopIteration
        return self.__shown[self.__index], self.__colours[self.__index]

    def check(self, txt):
        for i in range(4):
            if self.__shown[i] != self.__swedish[i]:
                self.__shown[i] = self.__swedish[i]
                if self.__swedish[i] == txt:
                    self.__colours[i] = "green"
                else:
                    self.__colours[i] = "red"
                break

    def is_all(self):
        for i in range(4):
            if self.__shown[i] != self.__swedish[i]:
                return False
        return True

    def get_translation(self):
        return self.__trans


class Display:
    def __init__(self, word_obj):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        w, h = pygame.display.get_surface().get_size()
        self.__x = w // 13
        self.__y = h // 7
        self.__dis_text = ""
        self.__word = ""
        self.__word_obj = word_obj
        self.__all = False
        self.__closed = False

    def flip(self):
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def show(self):
        x = self.__x
        y = self.__y
        text_color = "black"
        size = 0.6
        font = pygame.font.SysFont("Helvetica", int(size * x))
        symb = pygame.font.SysFont("Helvetica", x)
        self.__draw_rect(x, y, 2 * x, y)
        self.__draw_rect(4 * x, y, 2 * x, y)
        self.__draw_rect(7 * x, y, 2 * x, y)
        self.__draw_rect(10 * x, y, 2 * x, y)

        self.__draw_rect(x, 3 * y, 2 * x, y)
        label = symb.render("?", True, text_color)
        text_rect = label.get_rect(center=(2 * x, int(1.5 * y + 2 * y)))
        self.screen.blit(label, text_rect)

        self.__draw_rect(10 * x, 3 * y, 2 * x, y)
        label = symb.render("X", True, text_color)
        text_rect = label.get_rect(center=(11 * x, int(1.5 * y + 2 * y)))
        self.screen.blit(label, text_rect)

        txt = self.__word_obj.get_translation() if self.__all else "#"
        self.__draw_rect(4 * x, 3 * y, 5 * x, y)
        label = font.render(txt, True, text_color)
        text_rect = label.get_rect(center=(int(6.5 * x), int(1.5 * y + 2 * y)))
        self.screen.blit(label, text_rect)

        for i, one_w in enumerate(self.__word_obj):
            label = font.render(one_w[0], True, one_w[1])
            text_rect = label.get_rect(center=(2 * x + 3 * x * i, int(1.5 * y)))
            self.screen.blit(label, text_rect)

        self.__draw_rect(x, 5 * y, 11 * x, y)
        label = font.render(self.__word, True, text_color)
        text_rect = label.get_rect(center=(int(6.5 * x), int(1.5 * y + 4 * y)))
        self.screen.blit(label, text_rect)

    def __draw_rect(self, x, y, x_size, y_size):
        margin = 5
        pygame.draw.rect(self.screen, "white", [x, y, x_size, y_size])
        pygame.draw.rect(self.screen, "lightblue", [x + margin, y + margin, x_size - 2 * margin, y_size - 2 * margin])

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Display.__close()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.__mouse_effect(x, y)
                return x, y

            elif event.type == pygame.KEYDOWN:
                self.__keyboard_effect(event.key)
                return event.key

        return None, None

    def __mouse_effect(self, x, y):
        a = self.__x
        b = self.__y

        if 10 * a <= x <= 12 * a and 3 * b <= y <= 4 * b:
            self.__close()

        if a <= x <= 3 * a and 3 * b <= y <= 4 * b and not self.__all:
            self.__word_obj.check("")
            self.__word = ""
            self.__all = self.__word_obj.is_all()

    def __keyboard_effect(self, key):
        if key == pygame.K_RETURN:
            if self.__all:
                self.__dis_text = ""
                self.__word = ""
                self.__word_obj = random_word()
                self.__all = False
            else:
                self.__word_obj.check(self.__word)
                self.__word = ""
                self.__all = self.__word_obj.is_all()

        elif key == pygame.K_BACKSPACE:
            self.__word = self.__word[:-1]
        else:
            self.__word += pygame.key.name(key)

    def __close(self):
        self.__closed = True
        pygame.display.quit()
        pygame.quit()

    def is_closed(self):
        return self.__closed

def random_word():
    new = words.iloc[randint(0, words.size // 5)].values.tolist()
    return word(new[0], new[1], new[2], new[3], new[4])


if __name__ == '__main__':
    wor = random_word()
    screen = Display(wor)

    while not screen.is_closed():
        screen.flip()
        screen.show()
        screen.get_input()

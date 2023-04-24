import pygame
from random import randint
from pandas import read_excel

words = read_excel("./words.xlsx")


class word:
    def __init__(self, infinitiv, presens, preteritum, supinum, trans):
        self.swedish = [infinitiv, presens, preteritum, supinum]
        self.shown = ["#"] * 4
        self.colours = ["white"] * 4
        self.trans = trans
        self.index = -1

        i = randint(0, 3)
        self.shown[i] = self.swedish[i]
        self.colours[i] = "blue"

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.swedish):
            self.index = -1
            raise StopIteration
        return self.shown[self.index], self.colours[self.index]

    def check(self, txt):
        for i in range(4):
            if self.shown[i] != self.swedish[i]:
                self.shown[i] = self.swedish[i]
                if self.swedish[i] == txt:
                    self.colours[i] = "green"
                else:
                    self.colours[i] = "red"
                break

    def is_all(self):
        for i in range(4):
            if self.shown[i] != self.swedish[i]:
                return False
        return True


class Display:  # Klasa Display czyli frontend to co gracz widzi, spawn statkow wybuchy itp
    def __init__(self, word_obj):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        w, h = pygame.display.get_surface().get_size()
        self.a = w // 13
        self.b = h // 7
        self.dis_text = ""
        self.word = ""
        self.word_obj = word_obj
        self.all = False

    def flip(self):
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def show(self):
        a = self.a
        b = self.b
        color = "lightblue"
        size = 0.6
        font = pygame.font.SysFont("Helvetica", int(size * a))
        symb = pygame.font.SysFont("Helvetica", a)
        pygame.draw.rect(self.screen, color, [a, b, 2 * a, b])
        pygame.draw.rect(self.screen, color, [4 * a, b, 2 * a, b])
        pygame.draw.rect(self.screen, color, [7 * a, b, 2 * a, b])
        pygame.draw.rect(self.screen, color, [10 * a, b, 2 * a, b])

        pygame.draw.rect(self.screen, color, [a, 3 * b, 2 * a, b])
        label = symb.render("?", True, "white")
        text_rect = label.get_rect(center=(2 * a, int(1.5 * b + 2 * b)))
        self.screen.blit(label, text_rect)

        pygame.draw.rect(self.screen, color, [10 * a, 3 * b, 2 * a, b])
        label = symb.render("X", True, "white")
        text_rect = label.get_rect(center=(11 * a, int(1.5 * b + 2 * b)))
        self.screen.blit(label, text_rect)

        txt = self.word_obj.trans if self.all else "#"
        pygame.draw.rect(self.screen, color, [4 * a, 3 * b, 5 * a, b])
        label = font.render(txt, True, "white")
        text_rect = label.get_rect(center=(int(6.5 * a), int(1.5 * b + 2 * b)))
        self.screen.blit(label, text_rect)

        for i, one_w in enumerate(self.word_obj):
            label = font.render(one_w[0], True, one_w[1])
            text_rect = label.get_rect(center=(2 * a + 3 * a * i, int(1.5 * b)))
            self.screen.blit(label, text_rect)

        pygame.draw.rect(self.screen, color, [a, 5 * b, 11 * a, b])
        label = font.render(self.word, True, "white")
        text_rect = label.get_rect(center=(int(6.5 * a), int(1.5 * b + 4 * b)))
        self.screen.blit(label, text_rect)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Display.close()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.mouse_effect(x, y)
                return x, y

            elif event.type == pygame.KEYDOWN:
                self.keybord_effect(event.key)
                return event.key

        return None, None

    def mouse_effect(self, x, y):
        a = self.a
        b = self.b

        if 10 * a <= x <= 12 * a and 3 * b <= y <= 4 * b:
            self.close()

        if a <= x <= 3 * a and 3 * b <= y <= 4 * b:
            self.word_obj.check("")
            self.word = ""
            self.all = self.word_obj.is_all()

    def keybord_effect(self, key):
        if key == pygame.K_RETURN:
            if self.all:
                self.dis_text = ""
                self.word = ""
                self.word_obj = random_word()
                self.all = False
            else:
                self.word_obj.check(self.word)
                self.word = ""
                self.all = self.word_obj.is_all()

        elif key == pygame.K_BACKSPACE:
            self.word = self.word[:-1]
        else:
            self.word += pygame.key.name(key)

    @staticmethod
    def close():
        pygame.display.quit()
        pygame.quit()


def random_word():
    new = words.iloc[randint(0, 158)].values.tolist()
    return word(new[0], new[1], new[2], new[3], new[4])


if __name__ == '__main__':
    wor = random_word()
    screen = Display(wor)

    while True:
        screen.flip()
        screen.show()
        screen.get_input()

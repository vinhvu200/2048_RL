from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from Enum.direction import Direction
from Game import Game

import random

game = Game()
game.update()


def play():
    while(game.game_over() is False):
        r = random.randint(1, 4)

        if r is 1:
            game.move(Direction.RIGHT)
        if r is 2:
            game.move(Direction.LEFT)
        if r is 3:
            game.move(Direction.DOWN)
        if r is 4:
            game.move(Direction.UP)

    game.update()
    print(game.board)
    game.replay()

while True:
    play()
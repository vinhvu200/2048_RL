import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from models.enum.direction import Direction


class Game():

    def __init__(self):

        # IMPORTANT.. Test delay to see if results are being
        # recorded correctly
        self.delay = 0.02

        self.url = 'https://gabrielecirulli.github.io/2048/'
        exec_path = '/Users/vinh/Desktop/chromedriver'
        self.tile_container_xpath = '/html/body/div/div[4]/div[3]/*'
        self.game_over_xpath = '/html/body/div/div[4]/div[1]'
        self.try_again_xpath = '/html/body/div/div[4]/div[1]/div/a[2]'
        self.score_xpath = '/html/body/div/div[1]/div/div[1]'

        self.last_score = 0
        self.rows = 4
        self.cols = 4
        self.board = [0 for _ in range(16)]
        self.on_board = 0
        self.browser = webdriver.Chrome(executable_path=exec_path)
        self.browser.get(self.url)
        self.action_space = 4
        self.state = []

    def calc_reward(self):
        '''
        Calculate reward by getting current score and subtracting
        by last score.

        :return: reward (int)
        '''
        current_score = int(self.browser.find_element(By.XPATH, self.score_xpath).text)
        reward = current_score - self.last_score
        self.last_score = current_score
        return reward

    def game_over(self):
        '''
        Checks if game is over by checking if game-over element exists
        :return: boolean
        '''
        message = self.browser.find_element(By.XPATH, self.game_over_xpath).get_attribute('class')

        if message == 'game-message game-over':
            return True
        return False

    def get_state(self):
        state = list(self.board)
        state.append(self.on_board)
        return state

    def move(self, direction):
        '''
        Move in the direction stated. Small delay at the end before updating
        :param direction: UP, DOWN, LEFT, RIGHT(Direction enum)
        :return:
        '''

        action = ActionChains(self.browser)

        if direction is Direction.UP:
            action.send_keys(Keys.ARROW_UP)
        if direction is Direction.DOWN:
            action.send_keys(Keys.ARROW_DOWN)
        if direction is Direction.LEFT:
            action.send_keys(Keys.ARROW_LEFT)
        if direction is Direction.RIGHT:
            action.send_keys(Keys.ARROW_RIGHT)

        action.perform()
        time.sleep(self.delay)
        self.update()

        return self.state, self.calc_reward(), self.game_over()

    def replay(self):
        '''
        Click replay to reset the game
        :return: None
        '''
        replay = self.browser.find_element(By.XPATH, self.try_again_xpath)
        replay.click()

    def update(self):
        '''
        Update self.on_board and self.board
        :return:
        '''
        total_blocks = 0
        self.board = [0 for _ in range(16)]

        # Get all element of the board
        elements = self.browser.find_elements(By.XPATH, self.tile_container_xpath)

        # Parse each element
        for e in elements:
            by_spaces = e.get_attribute('class').split(' ')

            # total block update
            if len(by_spaces) is 4 and by_spaces[3] == 'tile-merged':
                total_blocks -= 1
            else:
                total_blocks += 1

            # board update
            num = int(by_spaces[1].split('tile-')[1])
            col = int(by_spaces[2][-3]) - 1
            row = int(by_spaces[2][-1]) - 1
            index = (row) * self.rows + (col)
            self.board[index] = num

        self.on_board = total_blocks
        self.state = list(self.board).append(self.on_board)
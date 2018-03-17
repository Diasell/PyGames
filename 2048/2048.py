
import pygame
import random
import math

# globals for user interface
WIDTH    = 500
HEIGHT   = 650
FPS      = 60


# colors:
BG_color    = (250,248,239)
BOARD_color = (187,173,160)

# importing images:
sheet = pygame.image.load("images/assets_2048.png")
BG_IMAGE = pygame.image.load('images/background.jpg')
logo_image = pygame.image.load("images/2048-logo.png")


# Sprite info:
LEN_SPRT_X    = 100
LEN_SPRT_Y    = 100
SPRITE_BORDER = 5


board = pygame.Surface((425,425))   # the size of your rect
board.set_alpha(255)                # alpha level
board.fill(BOARD_color)           # this fills the entire surface


# Initializing PyGame and gamescreen
pygame.init()
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()


# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def sprite_sheet(size,file,pos=(0,0)):

    #Initial Values
    len_sprt_x,len_sprt_y = size #sprite size
    sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

    sheet = pygame.image.load(file).convert_alpha() #Load the sheet
    sheet_rect = sheet.get_rect()
    sprites = []
    print sheet_rect.height, sheet_rect.width
    for i in range(0,sheet_rect.height-len_sprt_y,size[1]):#rows
        print "row"
        for i in range(0,sheet_rect.width-len_sprt_x,size[0]):#columns
            print "column"
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x

        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    print sprites
    return sprites


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    temp_lst = []
    for item in line:
        if item != 0:
            temp_lst.append(item)
    while len(temp_lst)<len(line):
        temp_lst.append(0)
    result = []
    for index in range(len(temp_lst)-1):
        if temp_lst[index] == temp_lst[index+1]:
            result.append(temp_lst[index]*2)
            temp_lst[index+1] = 0
        else:
            if temp_lst[index] != 0:
                result.append(temp_lst[index])
    if temp_lst[-1] != 0:
        result.append(temp_lst[-1])
    while len(result)<len(line):
        result.append(0)
    return result


def start_cell_value(number):
    """
    choosing 2 in 90%  and 4 in 10% of the cases if number = 10
    """
    value = 0
    temp = random.choice(range(number))
    if temp == 0:
        value = 4
    else:
        value = 2
    return value


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial_tiles = {UP : zip([0 for x in range(self._grid_width)],[x for x in range(self._grid_width)]),
                             DOWN : zip([self._grid_height-1 for x in range(self._grid_width)],[x for x in range(self._grid_width)]),
                             RIGHT : zip([x for x in range(self._grid_height)],[self._grid_width-1 for x in range(self._grid_height)]),
                             LEFT : zip([x for x in range(self._grid_height)],[0 for x in range(self._grid_height)])}
        self.reset()


    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[row*0 + col*0 for col in range(self._grid_width)] for row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_to_print =[]
        for item in self._grid:
            dummy_item = str(item)
            grid_to_print.append(dummy_item)

        # replace with your code
        return "\n".join(grid_to_print)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height


    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width


    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changes=[]
        for initial_tile in self._initial_tiles[direction]:
            tile = list(initial_tile)
            temp_list_values = []
            test_list=[]
            if direction in [UP, DOWN]:
                for number in range(self._grid_height):
                    value = self.get_tile(tile[0],tile[1])
                    temp_list_values.append(value)
                    tile[0] += OFFSETS[direction][0]
                    tile[1] += OFFSETS[direction][1]
                test_list = merge(temp_list_values)

                if temp_list_values != test_list:
                    changes.append(1)
                tile = list(initial_tile)

                for number in range(self._grid_height):
                    self.set_tile(tile[0],tile[1],test_list[number])
                    tile[0] += OFFSETS[direction][0]
                    tile[1] += OFFSETS[direction][1]

            if direction in [LEFT, RIGHT]:
                for number in range(self._grid_width):
                    value = self.get_tile(tile[0],tile[1])
                    temp_list_values.append(value)
                    tile[0] += OFFSETS[direction][0]
                    tile[1] += OFFSETS[direction][1]
                test_list = merge(temp_list_values)

                if temp_list_values != test_list:
                    changes.append(1)
                tile = list(initial_tile)

                for number in range(self._grid_width):
                    self.set_tile(tile[0],tile[1],test_list[number])
                    tile[0] += OFFSETS[direction][0]
                    tile[1] += OFFSETS[direction][1]
        if len(changes) == 0:
            pass
        else:
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile = [random.randrange(0,self._grid_height),
                 random.randrange(0,self._grid_width)]
        tile_value = start_cell_value(10)
        empty_cells = []
        for row in self._grid:
            for col in row:
                if col == 0:
                    empty_cells.append(col)
        if self._grid[tile[0]][tile[1]] == 0:
            self._grid[tile[0]][tile[1]] = tile_value
        elif len(empty_cells)>0:
            self.new_tile()
        else:
            print "you lose"



    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value


    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        tile_value = self._grid[row][col]
        return tile_value

    def draw(self, x, y):
        self.x = x
        self.y = y
        z = x # needs to return x to initial value
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                tile = self.get_tile(row,col)
                if tile == 0:
                    val = 0
                else:
                    val = int(math.log(tile, 2))
                # Locate the sprite you want
                sheet.set_clip(pygame.Rect(val*LEN_SPRT_X + SPRITE_BORDER, SPRITE_BORDER, LEN_SPRT_X, LEN_SPRT_Y))
                # Extract the sprite you want
                draw_me = sheet.subsurface(sheet.get_clip())
                # Create the whole screen so you can draw on it
                backdrop = pygame.Rect(self.x, self.y, WIDTH, HEIGHT)
                # moving to next position to draw an element in the grid
                self.x += LEN_SPRT_X + SPRITE_BORDER
                if self.x>=(LEN_SPRT_X + SPRITE_BORDER) * self._grid_width:
                    self.x = z
                    self.y +=LEN_SPRT_Y + SPRITE_BORDER
                game_display.blit(draw_me,backdrop)


def gameloop():
    grid = TwentyFortyEight(4, 4)

    while gameloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grid.move(LEFT)
                if event.key == pygame.K_RIGHT:
                    grid.move(RIGHT)
                if event.key == pygame.K_UP:
                    grid.move(UP)
                if event.key == pygame.K_DOWN:
                    grid.move(DOWN)

        game_display.fill(BG_color)
        game_display.blit(logo_image, (35,10))
        game_display.blit(board,(35,195))
        grid.draw(45,205)
        pygame.display.update()
        clock.tick(FPS)


gameloop()




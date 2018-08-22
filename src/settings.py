# Game options/settings
TITLE = "I am the massive LEGEND~! (pepo sink)"
WIDTH = 1024  # 768
HEIGHT = 576  # 432
FPS = 60
FONT_NAME = 'Arial'

# FILE PATHS
SPRITESHEET_FILE = 'images/sprite-sheet-16.png'
CHARACTER_SPRITESHEET = 'images/character-spritesheet3.png'

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMPS = 2
PLAYER_JUMP_VEL = 10

# Color codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BGCOLOR = (0, 100, 255)
IMG_BGCOLOR = (171, 205, 239)   # Color used to indicate transparency in sprites

# Some temporary testing platforms
PLATFORM_LIST = [
    (0, HEIGHT - 40, WIDTH, 40),
    (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
    (75, HEIGHT - 380, 100, 20),
    (350, 250, 100, 20),
    (175, 100, 50, 20)
]

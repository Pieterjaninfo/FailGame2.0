import pygame as pg
import random
from settings import *
from sprites import *
import utils


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.score = 0
        utils.load_data(self)
        self.spritesheet = SpriteSheet(SPRITESHEET_FILE)
        self.char_spritesheet = SpriteSheet(CHARACTER_SPRITESHEET)
        utils.log('Started up the program and loaded all the data successfully.')

    # Starts a new game
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platorms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.deth = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Build some platforms
        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platorms.add(p)

        self.run()

    # Run the game
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # Check player collision with platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platorms, False)
            if hits and self.player.rect.bottom < hits[0].rect.bottom:
                print(f'self: {self.player.rect.bottom} - hit: {hits[0].rect.bottom}')
                # TODO Check if hitting from top/bottom or left/right
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.rect.midbottom = self.player.pos

        # Player death
        if self.player.rect.bottom < 0:
            self.score += 1
            self.playing = False

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Use arrow keys to move", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to start", 22, WHITE, WIDTH/2, HEIGHT/4*3)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.draw_text("LOL U DIED - PRESS R TO RESPAWN", 49, BLACK, WIDTH/2, HEIGHT/4)
        self.draw_text("LOL U DIED - PRESS R TO RESPAWN", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        self.wait_for_key(pg.K_r)

    def wait_for_key(self, key=None):
        waiting = True
        while waiting:
            self.clock.tick(10)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game()
                if event.type == pg.KEYUP:
                    if key is None:
                        waiting = False
                    else:
                        if event.key == key:
                            waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def quit_game(self):
        utils.store_data(self)
        utils.log('Quit the game.')
        pg.quit()
        exit()


if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()
    g.quit_game()

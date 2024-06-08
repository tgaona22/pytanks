import pygame as pg
import numpy as np
from pathlib import Path

main_dir = Path("./")
data_dir = main_dir / "data"


def load_image(name, colorkey=None, scale=1):
    img_path = data_dir / name
    image = pg.image.load(img_path)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    # copies a Surface and converts its color format
    # and depth to match the display.
    image = image.convert()
    # what is a colorkey?
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((size[0] - 1, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


class Tank(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.orig_image, self.orig_rect = load_image("tank.png", None)
        self.image = self.orig_image
        self.rect = self.orig_rect
        # when part of a Group and draw(surf) is called,
        # the surface will blit(sprite.image, sprite.rect)
        self.angle = 0.0
        self.direction = np.array([1.0, 0.0])
        self.rotating = False
        self.moving = False
        self.pos = (300, 200)
        self.rect.topleft = self.pos

    def update(self):
        if self.rotating:
            rot_img = pg.transform.rotate(self.orig_image, self.angle)
            new_rect = rot_img.get_rect(center=self.orig_rect.center)
            self.rotating = False
            new_rect.topleft = self.pos
            self.image = rot_img
            self.rect = new_rect
            self.rotating = False
        else:
            self.rect.topleft = self.pos

    def rotate(self, right):
        self.angle = (self.angle - 2.0) if right else (self.angle + 2.0)
        self.angle = 0.0 if self.angle > 360.0 else self.angle
        self.angle = 360.0 if self.angle < 0.0 else self.angle
        print(f"angle: {self.angle}")
        self.rotating = True
        self.direction = np.array(
            [
                np.cos(self.angle * np.pi / 180),
                -np.sin(self.angle * np.pi / 180),
            ]
        )
        print(f"direction: {self.direction}")

    def move(self, forward):
        if forward:
            self.pos += 2 * self.direction
        else:
            self.pos += -2 * self.direction


def main():
    pg.init()
    screen = pg.display.set_mode((600, 480), pg.SCALED)
    pg.display.set_caption("Tanks")
    pg.mouse.set_visible(False)

    bgr = pg.Surface(screen.get_size())
    bgr = bgr.convert()
    bgr.fill((170, 238, 187))

    screen.blit(bgr, (0, 0))
    # changes to display surface are not immediately visible.
    pg.display.flip()

    tank = Tank()

    allsprites = pg.sprite.RenderPlain((tank))
    clock = pg.time.Clock()

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            tank.rotate(right=False)
        elif keys[pg.K_d]:
            tank.rotate(right=True)
        elif keys[pg.K_w]:
            tank.move(forward=True)
        elif keys[pg.K_s]:
            tank.move(forward=False)

        allsprites.update()

        screen.blit(bgr, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()
    pg.quit()


if __name__ == "__main__":
    main()

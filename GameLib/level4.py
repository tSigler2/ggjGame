import pygame as pg
import sys
import math

# level design matrix
# P = platform, R = ring, E = enemy, S = spring, _ = empty space
LEVEL_MATRIX = [
    "_______________________RRRRRRRRRRRRR________________________________________________",
    "_______________________PPPPPPPPPPPPP___R____________________________________________",
    "__________________________________________R_________________________________________",
    "____________________________________________R_______________________________________",
    "____________________________________________R______R________________________________",
    "________R___________________________________PPPP______E__________R________R_________",
    "___________________S_________________________R__R_______________PP______R___R_______",
    "__________PPPPPPPPPP______________________P__________________R_________R_____R______",
    "_______R__________________________________R_________________________________________",
    "__PPPPPPPP___R_______PPP_______E__________P________R_____R______E________E__________",
    "_________________________________RRRRR______________________S_________S_____________",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
]

CELL_WIDTH = 40
CELL_HEIGHT = 40


class Level4:
    def __init__(self, dims, fps=60):
        pg.init()
        self.width, self.height = dims
        self.fps = fps
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Level 4: Brazonic Adventure!")
        self.clock = pg.time.Clock()

        # player properties
        self.player_pos = [100, 300]
        self.player_vel = [0, 0]
        self.player_accel = 0.5
        self.player_friction = 0.9
        self.player_gravity = 0.8
        self.player_jump_strength = -15
        self.on_ground = False
        self.max_speed = 12
        self.ring_count = 0

        # camera offset for side-scrolling
        self.camera_offset = 0

        # game objects
        self.platforms = []
        self.rings = []
        self.enemies = []
        self.springs = []

        # load and scale ring image to be smaller (10 times smaller)
        self.ring_image = pg.image.load("GameLib/ring.png").convert_alpha()
        self.ring_image = pg.transform.scale(
            self.ring_image,
            (self.ring_image.get_width() // 10, self.ring_image.get_height() // 10),
        )
        self.ring_angle = 0  # initial rotation angle

        # parse the level matrix
        self.parse_level_matrix()

    def parse_level_matrix(self):
        # convert level matrix into game objects
        for row_index, row in enumerate(LEVEL_MATRIX):
            for col_index, cell in enumerate(row):
                x = col_index * CELL_WIDTH
                y = row_index * CELL_HEIGHT
                if cell == "P":  # platform
                    self.platforms.append([x, y, CELL_WIDTH, CELL_HEIGHT])
                elif cell == "R":  # ring
                    self.rings.append([x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2])
                elif cell == "E":  # enemy
                    self.enemies.append(
                        {"rect": [x, y, CELL_WIDTH, CELL_HEIGHT], "vel": 2}
                    )
                elif cell == "S":  # spring
                    self.springs.append(
                        [x + CELL_WIDTH // 4, y + CELL_HEIGHT // 4, 20, 10]
                    )

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:  # move left
            self.player_vel[0] -= self.player_accel
        if keys[pg.K_RIGHT]:  # move right
            self.player_vel[0] += self.player_accel
        if keys[pg.K_SPACE] and self.on_ground:  # jump
            self.player_vel[1] = self.player_jump_strength

    def apply_physics(self):
        # apply gravity
        self.player_vel[1] += self.player_gravity

        # apply friction
        self.player_vel[0] *= self.player_friction

        # cap horizontal speed
        if abs(self.player_vel[0]) > self.max_speed:
            self.player_vel[0] = self.max_speed * (
                self.player_vel[0] / abs(self.player_vel[0])
            )

        # update player position
        self.player_pos[0] += self.player_vel[0]
        self.player_pos[1] += self.player_vel[1]

        # update camera offset for scrolling
        self.camera_offset = max(0, self.player_pos[0] - self.width // 2)

        # check for collisions with platforms
        self.on_ground = False
        for plat in self.platforms:
            if (
                self.player_pos[1] + 20 >= plat[1]
                and self.player_pos[1] <= plat[1]
                and plat[0] <= self.player_pos[0] <= plat[0] + plat[2]
            ):
                self.player_pos[1] = plat[1] - 20
                self.player_vel[1] = 0
                self.on_ground = True

    def update_enemies(self):
        for enemy in self.enemies:
            # update enemy position
            enemy["rect"][0] += enemy["vel"]

            # reverse direction if the enemy hits a boundary
            if (
                enemy["rect"][0] <= 0
                or enemy["rect"][0] + enemy["rect"][2]
                >= len(LEVEL_MATRIX[0]) * CELL_WIDTH
            ):
                enemy["vel"] *= -1

            # reverse direction if the enemy falls off a platform
            on_platform = False
            for plat in self.platforms:
                if (
                    enemy["rect"][0] + enemy["rect"][2] / 2 >= plat[0]
                    and enemy["rect"][0] + enemy["rect"][2] / 2 <= plat[0] + plat[2]
                    and enemy["rect"][1] + enemy["rect"][3] == plat[1]
                ):
                    on_platform = True
                    break
            if not on_platform:
                enemy["vel"] *= -1

    def handle_rings(self):
        # check for collisions with rings
        for ring in self.rings[:]:
            if math.dist(self.player_pos, ring) < 15:
                self.rings.remove(ring)
                self.ring_count += 1

    def handle_springs(self):
        # check for collisions with springs
        for spring in self.springs:
            if (
                self.player_pos[1] + 20 >= spring[1]
                and self.player_pos[1] <= spring[1] + spring[3]
                and spring[0] <= self.player_pos[0] <= spring[0] + spring[2]
            ):
                self.player_vel[1] = -20

    def handle_enemies(self):
        # check for collisions with enemies
        for enemy in self.enemies:
            if (
                self.player_pos[0] < enemy["rect"][0] + enemy["rect"][2]
                and self.player_pos[0] + 20 > enemy["rect"][0]
                and self.player_pos[1] < enemy["rect"][1] + enemy["rect"][3]
                and self.player_pos[1] + 20 > enemy["rect"][1]
            ):
                print("Hit an enemy! You lost all your rings!")
                self.ring_count = 0

    def draw(self):
        self.screen.fill((135, 206, 235))  # sky blue background

        # draw platforms (green ground)
        for plat in self.platforms:
            pg.draw.rect(
                self.screen,
                (34, 139, 34),
                [plat[0] - self.camera_offset, plat[1], plat[2], plat[3]],
            )

        # draw player
        pg.draw.circle(
            self.screen,
            (0, 0, 255),
            [int(self.player_pos[0] - self.camera_offset), int(self.player_pos[1])],
            20,
        )

        # draw rotating rings
        for ring in self.rings:
            # Rotate the ring image
            rotated_ring = pg.transform.rotate(self.ring_image, self.ring_angle)
            # Draw the rotated ring
            self.screen.blit(
                rotated_ring,
                (
                    ring[0] - self.camera_offset - rotated_ring.get_width() // 2,
                    ring[1] - rotated_ring.get_height() // 2,
                ),
            )
            self.ring_angle += 5  # increment the rotation angle

        # draw enemies
        for enemy in self.enemies:
            pg.draw.rect(
                self.screen,
                (255, 0, 0),
                [
                    enemy["rect"][0] - self.camera_offset,
                    enemy["rect"][1],
                    enemy["rect"][2],
                    enemy["rect"][3],
                ],
            )

        # draw springs
        for spring in self.springs:
            pg.draw.rect(
                self.screen,
                (0, 255, 255),
                [spring[0] - self.camera_offset, spring[1], spring[2], spring[3]],
            )

        # draw ring count
        font = pg.font.Font(None, 36)
        ring_text = font.render(f"Rings: {self.ring_count}", True, (0, 0, 0))
        self.screen.blit(ring_text, (10, 10))

        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.handle_input()
            self.apply_physics()
            self.update_enemies()
            self.handle_rings()
            self.handle_springs()
            self.handle_enemies()
            self.draw()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Level4((800, 600))
    game.run()

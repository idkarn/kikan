from kikan import Loop, InitEvent, Input, CollisionEvent, Entity, Vector, World, WorldMap, WorldObject, Logger, engine
from random import randint

world_map = WorldMap([
    WorldObject(Vector(2, 2), "#"),
    WorldObject(Vector(2, 3), "#"),
    WorldObject(Vector(3, 3), "#")
])
world = World(world_map, {})

engine.init(world)


class Player(Entity):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    @CollisionEvent
    def collide(self):
        global score, gem
        score += 1
        gem.respawn()


class Gem(Entity):
    def __init__(self, position: Vector, texture: str) -> None:
        super().__init__(position, texture)
        self.velocity = Vector(5, 0)

    def respawn(self):
        self.position = Vector(randint(-10, 10), randint(-10, 10))
        self.velocity = Vector(5, 0)

    def update(self):
        self.apply_force(Vector(-1, 0))


player: Player
gem: Gem
score = 0


def print_score():
    size = engine.screen.size
    coords = (-(size["width"] // 2 - 1), size["height"] // 2 - 1)
    # noinspection PyTypeChecker
    engine.screen.display_string(*coords, f"Score: {score}", (0, 255, 0))


@InitEvent
def init():  # start point of the game
    global player, gem
    player = Player(Vector(0, 0), "@")
    gem = Gem(Vector(5, 2), "*")
    print("[INIT] Success")


@Loop(fps=10)
def loop():  # main game loop
    engine.screen.draw(gem)
    engine.screen.draw(player)
    print_score()

# *** keyboard inputs ***


@Input(key="d")
def inputD():
    player.position.x += 1
    Logger.print('D')


@Input(key="a")
def inputA():
    player.position.x -= 1
    Logger.print('A')


@Input(key="w")
def inputW():
    player.position.y += 1
    Logger.print('W')


@Input(key="s")
def inputS():
    player.position.y -= 1
    Logger.print('S')


@Input(key="q")
def quit():
    exit()


engine.start()

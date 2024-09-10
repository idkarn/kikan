from random import randint
from kikan import engine, Entity, Vector
from kikan.entity import EmptyObject, Pixel, Texture, StepSides
from kikan.utils import Logger
from kikan.states import State
from time import time

speed = State(1)


def random_position() -> Vector:
    return Vector(
        randint(
            -engine.screen.screen.width // 2 + 1, engine.screen.screen.width // 2 - 1
        ),
        randint(
            -engine.screen.screen.height // 2 + 1, engine.screen.screen.height // 2 - 1
        ),
    )


def update_parts() -> None:
    for i in range(len(snake.parts) - 1):
        d = (snake if i == 0 else snake.parts[i - 1]).position - snake.parts[
            i + 1
        ].position
        if d.x == 0 and d.y != 0:
            snake.parts[i].texture = SnakeTailPart.VerticalTexture
        elif d.x != 0 and d.y == 0:
            snake.parts[i].texture = SnakeTailPart.HorizonalTexture
        else:
            snake.parts[i].texture = SnakeTailPart.CornerTexture


class Snake(Entity):
    Texture = Texture([[Pixel("@")]])

    def __init__(self) -> None:
        super().__init__(Vector(0, 0), self.Texture)
        self.direction = StepSides.UP
        self.parts = [SnakeTailPart(Vector(0, i)) for i in range(-1, -3, -1)]
        self.dp = Vector(0, 0)
        self.ts = time()

    def on_input(self, key: str) -> None:
        match key:
            case "up":
                self.direction = StepSides.UP
            case "down":
                self.direction = StepSides.DOWN
            case "right":
                self.direction = StepSides.RIGHT
            case "left":
                self.direction = StepSides.LEFT

    def on_pre_update(self, dt: float) -> None:
        if (
            abs(self.position.x) >= engine.screen.screen.width / 2
            or abs(self.position.y) >= engine.screen.screen.height / 2
        ):
            GameManager.stop_game()

    def on_update(self, dt: float) -> None:
        if time() - self.ts > 1 / speed.get():
            Logger.print(f"tick {time() - self.ts:.03f} delay {1 / speed.get():.03f}")

            for i in range(len(self.parts) - 1, 0, -1):
                self.parts[i].position = self.parts[i - 1].position * 1
            self.parts[0].position = self.position * 1

            self.step(self.direction)

            self.ts = time()

            update_parts()

    def on_collision(self, other: Entity) -> None:
        if other is not self.parts[0] and isinstance(other, SnakeTailPart):
            # engine.stop()
            ...
        elif isinstance(other, Apple):
            Logger.print("apple is eaten")
            speed.set(speed.get() + 1)
            self.parts.append(SnakeTailPart(self.position))


class SnakeTailPart(Entity):
    VerticalTexture = Texture([[Pixel("|")]])
    HorizonalTexture = Texture([[Pixel("-")]])
    CornerTexture = Texture([[Pixel("+")]])

    def __init__(self, position: Vector) -> None:
        super().__init__(position, "*")


class Apple(Entity):
    def __init__(self) -> None:
        super().__init__(Vector(-5, 0), Texture([[Pixel("o", (255, 0, 0))]]))

    @speed.affects
    def respawn(self) -> None:
        parts_coords = [i.position for i in snake.parts]
        self.position = random_position()
        while self.position in parts_coords:
            self.position = random_position()
        Logger.print(self.position)


class GameManager(EmptyObject):
    score = 0

    @classmethod
    def on_update(cls, dt: float) -> None:
        engine.screen.display_string(-40, 10, f"Score: {cls.score}")

    @staticmethod
    def stop_game() -> None:
        engine.stop()

    @staticmethod
    def on_input(key: str) -> None:
        if key == "q":
            engine.stop()

    @speed.affects
    @staticmethod
    def inc_score() -> None:
        GameManager.score += 1

        if GameManager.score % 10 == 0:
            engine.config.fps = GameManager.score


snake = Snake()
apple = Apple()

engine.start()

print(len(snake.parts))

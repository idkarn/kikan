# kikan

TUI-based game engine in Python. Use this little thing to make awesome games right into your terminal.

## Installation

All you need to do is install this module as you usual do.

```sh
$ pip install kikan
```

## Usage

Let's cover all essential things you will use for your game.

### Engine

TODO

### Entities

This is main component a game is built from. Any interactable object in your game is `Entity`. Entities use several default methods to use engine's capabilities.

```py
from kikan import engine
from kikan.entity import Entity
from kikan.math import Vector

class Player(Entity):
  def on_pre_update(self, dt: float):
    ...
  def on_update(self, dt: float):
    ...
  def on_collision(self, other: Entity):
    ...
  def on_input(self, key: str):
    ...

p = Player(Vector(0, 0), "P") # position and texture

engine.start() # at the very end of the file
```

Sometimes you want to manage some variables or display something but you don't need a whole entity with the physics and all that stuff. Then use `MetaEntity`. Such classes don't have to be initialized.

### World

TODO

### Screen

TODO

### Logger

TODO

### Entities communication

There are two ways to implement this. Signals let you subscribe a function to some kind of event. When that event happens (signal emits), the subscribers are called. If you want something to contain payload then use states. State is a cell with value that you can update and affect functions that depend on this state.

**States**

```py
hp = State(10) # you have to pass an initial value

class StatManager(MetaEntity):
  @hp.affects # subscribe the method to the state
  def update_hearts():
    render_hearts(hp.get()) # get the current value from the state

hp.set(9) # change the current value
```

**Signals**

```py
on_hit = Signal() # define a signal in scope your entities can reach

class Player(Entity):
  @on_hit # use it as a decorator to mark subscribers
  def dec_hp(self):
    self.hp -= 1

p = Player()

class Enemy(Entity):
  def on_collision(self, other):
    if other is p:
      on_hit.emit() # emit the signal to trigger subscribed functions
```

## Development

So you want to contibute to this package... Let's prepare environment:

1. Make a fork and clone the repo.
2. Install package as editable.
3. Use `tox` to test and run other useful scenarios.
4. (VS Code) Install recommended extensions to follow the code style. Make sure you have installed `mypy` in your system if you want to check static typing on save .

What about tools?

- Use `ruff` to lint your code
- Use `black` to format your code
- Use `mypy` to check static typing in your code

All this you can do with tox.

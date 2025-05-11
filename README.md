# Polterphysics

## General presentation

**Project title**: Polterphysics

**Contributors**:
- **Clément Moussy** (Otherbug) : Core physics and object interactions
- **Maël Prouteau** (Astrion20) : UI/UX design and level management
- **Maxime Noudelberg** (MrThonChan) : Interaction with the player, trajectory equations
- **Mathias Gomes** (mathias-46) : Asset design and level layouts
- **Rafael Véclin** (Meta122) : Project structure, sprite management and documentation

## Description

**Polterphysics** is a Python-based 2D game project centered around chaotic, physics-driven interactions in a paranormal setting. The gameplay involves object manipulation, puzzle-solving, and humorous physics-based outcomes.

## Key features

- Modular architecture divided into core, data, utils and object layers  
- Physics-based object interactions
- Large number of varied levels

## Technologies used

- **Programming language**: Python 3.12+  
- **Libraries**:  
  - Standard Python libraries (`math`, `random`, etc.)
  - External `Pygame` library
- **Tools**:
  - Git for version control  
  - Visual Studio / VSCode / PyCharm for development
  - Discord for communication
  - A bit of ChatGPT for readability/documentation
  - Paint for most of the sprites, Sora and itch.io for some of them

## Installation

### Clone the repository

```
git clone https://github.com/Inkflow-Games/Polterphysics.git
cd Polterphysics
```

### Set up the environment

1. Ensure Python 3.12+ is installed  
2. (If needed) Install external libraries

## How to use

### Running the application

```
python main.py
```

> Be careful to be in the `Polterphysics` folder when running this command.

## Technical documentation

### Project structure

```
Polterphysics/
├── core/           # Core game logic and game loop
├── data/           # Assets and game data (sounds, images, levels, etc.)
├── objects/        # Game object classes and tools for handling physical objects
├── utils/          # Utility scripts
├── main.py         # Main launcher script
```

### Key modules and functionalities

#### core/
- `collision.py` : Provides functions for detecting and resolving collisions between objects using physics-based calculations.
- `input_handler.py` : Library of functions that handle the possible actions of the user.
- `level_manager.py` : Handles the different scenes and transitions between them.
- `physics_engine.py` : Dimple physics engine that manages a collection of objects and handles physics updates.
- `run.py` : Main loop for the Polterphysics game.
- `sound.py` : Main script for handling sound effects and background music in the game.
- `sprite_manager.py` : Defines a SpriteManager class used for updating objects sprites and the Key object.

#### data/
- `buttons.json` : File containing all the necessary data for buttons, linked to each level.
- `levels.json` : File containing all the level data (objects and their properties, static sprites, etc.)

#### objects/
- `bonus.py` : Defines a Bonus class used for giving the player extra launch.
- `key.py` : Defines a Key class used for switching to the next in-game level.
- `mincircle.py` : Module for computing the Minimum Enclosing Circle (MEC) using Welzl's algorithm.  
- `object.py` : Defines a physical object with mass, position, velocity, and interactions such as forces, spin, and collisions.
- `Quadtree.py` : Quadtree structure for efficient spatial partitioning and query of circular objects.

#### utils/
- `math_utils.py` : Provides utility functions for force conversions.
- `sprites_utils.py` : Provides utility sprites rendering.
- `vector_utils.py` : Provides utility functions to obtain information on vectors / make computations with them.

## Known bugs

- Some precision errors with collision, unfortunately hard to fix because they are caused by Pygame's lack of execution speed.
- Sometimes the input detection on objects is a little grumpy.

## Credits

- `Audio` : Yo-kai Watch OST, Stardust Crusaders OST, Bayonetta OST, Hollow Knight OST, New Super Mario Bros OST, Edgy Truck on YouTube, Super Mario sound effects
- `Graphics` : itch.io, Sora, and us !
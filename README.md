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

- **Programming language**: Python 3.10+  
- **Libraries**:  
  - Standard Python libraries (`math`, `random`, etc.)
  - External `Pygame` library
- **Tools**:
  - Git for version control  
  - Visual Studio / VSCode / PyCharm for development  
  - A bit of ChatGPT for readability/documentation
  - Paint for most of the sprites, Sora and itch.io for some of them

## Installation

### Clone the repository

```
git clone https://github.com/Inkflow-Games/Polterphysics.git
cd Polterphysics
```

### Set up the environment

1. Ensure Python 3.10+ is installed  
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
- `placeholder.py` :

#### data/
- `placeholder.py` :

#### objects/
- `placeholder.py` :

#### utils/
- `placeholder.py` :

## Known bugs

- Some precision errors with collision, unfortunately hard to fix because they are caused by Pygame's lack of execution speed.
- Sometimes the input detection is a little grumpy.

## Credits

- Sons : `PLACEHOLDER` 
- Graphismes : `PLACEHOLDER` 
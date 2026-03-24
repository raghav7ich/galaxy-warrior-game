# REPORT CONTENT - GALAXY WARRIOR

## Title Page
**Project Title:** Galaxy Warrior: 2D Space Shooter Game  
**Subject:** Computer Graphics / Programming  
**Prepared By:** Your Name  
**Roll No.:** Your Roll Number  
**Semester:** Your Semester  
**Submitted To:** Your Teacher Name  

---

## 1. Introduction
Galaxy Warrior is a 2D space shooter game developed using Python and the Pygame library. The project demonstrates the use of computer graphics concepts in a practical and interactive way. The game allows the player to control a spaceship, shoot incoming enemies, collect power-ups, and battle a boss across multiple levels. It also uses collision detection, animation, score tracking, and event handling, which are important concepts in game and graphics programming.

This project was developed in Visual Studio Code and is suitable for academic practical submission because it combines programming logic with graphical output.

---

## 2. Objectives
- To develop a complete 2D game using Python and Pygame.
- To understand the game loop and real-time rendering.
- To implement movement, animation, and collision detection.
- To apply object-oriented programming in a practical project.
- To create an attractive and interactive graphical application.
- To understand event handling and keyboard controls in game development.

---

## 3. Problem Statement
The purpose of this project is to create a graphical game application that demonstrates the practical use of computer graphics and interactive programming concepts. The game should provide player movement, enemy generation, shooting mechanics, level progression, and a boss system while maintaining smooth gameplay.

---

## 4. Tools and Technologies Used
- **Programming Language:** Python
- **Library:** Pygame
- **Code Editor:** Visual Studio Code
- **Operating System:** Windows

---

## 5. System Design
The system is divided into the following modules:

### 5.1 Main Module
Starts the project and launches the game object.

### 5.2 Game Management Module
Controls the game loop, menus, states, levels, and drawing of all elements.

### 5.3 Entity Module
Contains all game objects such as player, enemies, boss, bullets, power-ups, and stars.

### 5.4 Settings Module
Contains reusable constants such as width, height, colors, and game speed values.

---

## 6. Features of the Project
- Start menu
- Player spaceship control
- Shooting system
- Enemy wave generation
- Boss fight
- Health and lives system
- Power-ups
- Level progression
- Score display
- Game over and restart option
- Victory screen

---

## 7. Algorithm / Working Procedure
1. Start the game and show the main menu.
2. When the player presses Enter, gameplay starts.
3. The spaceship moves based on keyboard input.
4. Pressing Space fires bullets upward.
5. Enemies are generated automatically and move downward.
6. If bullets hit enemies, enemies lose health or get destroyed.
7. The score increases when enemies are destroyed.
8. Power-ups may appear and give temporary advantages.
9. After a required number of enemies are defeated, the boss appears.
10. Defeating the boss moves the game to the next level.
11. After all levels are completed, the player wins.
12. If player lives are exhausted, the game over screen appears.

---

## 8. Key Graphics Concepts Used
- 2D drawing using polygons, circles, and rectangles
- Real-time screen update using the game loop
- Object movement and animation
- Collision detection using rectangular hitboxes
- Color usage and HUD rendering
- Interactive keyboard control handling

---

## 9. Code Explanation
### `main.py`
This file is the entry point of the project. It imports the Game class and runs the main loop.

### `settings.py`
This file stores configuration constants such as screen size, colors, speed, and FPS.

### `entities.py`
This file contains all game object classes:
- Player
- Enemy
- Boss
- Bullet
- Star
- Explosion
- PowerUp

### `game.py`
This is the main controller file. It manages:
- menu screen
- game states
- enemy spawning
- boss fight
- level progression
- collision detection
- score and health display
- final drawing on screen

---

## 10. Advantages of the Project
- Easy to understand and explain
- Demonstrates multiple graphics concepts
- Uses object-oriented programming
- Can be extended with images and sound later
- Runs completely inside VS Code with Python

---

## 11. Limitations
- The game currently uses shape-based graphics instead of image sprites.
- Multiplayer mode is not included.
- Sound effects are not added in this version.
- Data is not saved permanently.

---

## 12. Future Enhancements
- Add image assets and background music
- Add difficulty selection
- Add leaderboard and score saving
- Add more enemies and more boss stages
- Add sound effects and particle effects

---

## 13. Conclusion
Galaxy Warrior is a successful 2D game project that demonstrates the practical implementation of computer graphics and game programming concepts using Python and Pygame. The project includes player interaction, animation, collision detection, and level-based gameplay. It helped in understanding how graphical applications are built and managed in real time.

---

## 14. References
1. Python Official Documentation
2. Pygame Official Documentation
3. Visual Studio Code Documentation
4. Class notes and laboratory guidelines

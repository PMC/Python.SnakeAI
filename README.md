# SnakeAI

The idea is to build a minimal snake game as phase 1 and then in phase 2, use reinforcement learning to learn an AI to play the game.

Right now the game works atleast. One apple to chase and use WASD to control the snake. Close Window to quit. Game score when you loose is printed in the console and shortly thereafter the game restarts.

## Running the Project with `uv`

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management and running.

### 1. Install Dependencies

```pwsh
uv sync
```

### 2. Activate (pwsh)

```pwsh
.\.venv\Scripts\activate.ps1
```

### 3. Run the Application

```pwsh
uv run .\src\game.py
```

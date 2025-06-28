# Backend

For this project, we use Python 3.10+, Flask, and SQLite.

## Installation

Python 3.10+ is required.
You can run the following script to install the dependencies.
```
./install.sh // OR ./install3.sh for MacOS where python3 is the default python
```

## Running the backend

Run the following script to start the backend.
```
./start.sh
```

## Creating a new game

Run the following command at root to create a new game (word).
```
. backend/.venv/bin/activate && python -m backend.automation.daily_game_creation
```


## Cron job for game creation

Automate game creation using crontable and specific script

```
crontab -e
45 9 * * 1-5 cd <path/to/wordle/file> && . backend/.venv/bin/activate && python -m backend.automation.daily_game_creation > wordle.log
```

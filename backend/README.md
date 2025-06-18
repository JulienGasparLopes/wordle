Run backend

```
flask --app app run -p 5001
```

Automate game creation using crontable and specific script

```
crontab -e

45 9 * * 1-5 cd <path/to/wordle/file> && . backend/.venv/bin/activate && python -m backend.automation.daily_game_creation > wordle.log
```

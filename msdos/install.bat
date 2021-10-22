@echo off

rem pip install -e .

if exist database.db goto DATABASE_EXISTS

python init_db.py

goto END

:DATABASE_EXISTS

echo The database exists already:
dir database.db

:END

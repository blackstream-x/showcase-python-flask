@echo off

rem pip install -e .

if exist database.db goto DATABASE_EXISTS

python init_db.py

goto END

:DATABASE_EXISTS

echo Die Datenbank existiert bereits:
dir /b database.db

:END

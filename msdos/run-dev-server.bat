@echo off

if NOT EXIST "%VIRTUAL_ENV%" goto NOVENV

set FLASK_APP=app
set FLASK_DEBUG=true

python -m flask run


goto END

:NOVENV

echo Please activate the virtual environment before running this project using msdos\activate-virtualenv

:END

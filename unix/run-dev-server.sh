if [ -z "${VIRTUAL_ENV}" ] ; then
    echo "Please run this project in a virtual environment!"
    exit 1
fi

export FLASK_APP=app
export FLASK_ENV=development

python -m flask run

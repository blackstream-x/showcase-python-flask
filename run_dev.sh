if [ -z "${VIRTUAL_ENV}" ] ; then
    echo "Please run this project in a virtual environment!"
    exit 1
fi

. ./set_environment_dev.sh
python -m flask run

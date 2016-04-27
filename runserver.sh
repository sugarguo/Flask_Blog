#! /bin/bash

#source ~/.bashrc 

echo "==========================="
echo "please input mode:"
echo "0 shell"
echo "1 runserver"
echo "2 gunicorn"
echo "3 uwsgi"
echo "8 clean *.sqlite *~ *.pyc"
echo "9 exit"
echo "==========================="
read input

case $input in
	0)
		echo "shell run"
		#sleep 1
		source venv/bin/activate
		python manage.py shell;;
	1)
		echo "runserver 0.0.0.0:2000"
		source venv/bin/activate
		python manage.py runserver -p 3000 -h 0.0.0.0;;
	2)
		echo "gunicorn.conf runserver:app"
		source venv/bin/activate
		gunicorn --config gunicorn.conf runserver:app;;
	3)
		echo "uwsgi"
		source venv/bin/activate
		uwsgi config.ini;;
	8)
		echo "clean *.sqlite *~ *.pyc"
		rm *.sqlite
		find . -name "*~" | xargs rm
		find . -name "*.pyc" | xargs rm;;
	9)
		echo "exit!"
		exit;;
esac

#python manage.py shell

#python runserver.py

#python manage.py runserver -p 2005 -h 0.0.0.1

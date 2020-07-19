chmod +x run.sh 
 
echo "SKIP DROP DATABASE ? y == yes n == no"
read types 
if [ $types == 1 ] 
then
mysql -uroot -p'password1234' -Bse "CREATE DATABASE checkin; exit;"
else
mysql -uroot -p'password1234' -Bse "DROP DATABASE checkin; CREATE DATABASE checkin; exit;"
fi

python manage.py migrate   
mysql -uroot -p'password1234' -Bse "use checkin; source ./backup/fff.sql; exit;"

echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'root@root.com', 'root')" | python manage.py shell

python manage.py runserver

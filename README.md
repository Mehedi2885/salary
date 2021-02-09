# job_salary

#### Run the query in database :
```
delete from django_migrations;
```

#### Existing database migrations :
```
rm -rf wage-estimation/migrations/
python manage.py migrate
python manage.py migrate --fake
python manage.py makemigrations wage-estimation
python manage.py migrate --fake-initial
```
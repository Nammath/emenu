# emenu
Django Rest Framework eMenu API

# Install
1. Create .env file using .env.tmp template file
2. Run 'docker-compose up' command to create and launch containers
3. List containers by command 'docker ps'
4. Enter 'django' container by command 'docker exec -it {container_id} bash'
5. Run migrations by command 'python manage.py migrate'
6. Create superuser by running command 'python manage.py createsuperuser'

# Documentation
To see documentation use /swagger/ endpoint

Menu list query parameters - 'name', 'date_added_start', 'date_added_finish', 'date_modified_start', 'date_modified_finish'
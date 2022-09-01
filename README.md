# Messenger

Stack
1. Django Rest Framework
2. Channels
3. PostgreSql
4. Vue.js
5. Redis

Functionality
1. Registration and Authorisation via tokens
2. Searching people
3. Live chat
4. Notifications

Launch Docker

1. Migrations

   ```bash
    $ python manage.py makemigrations && python manage.py migrate
    ```
 
2. Run Django

   ```bash
    $ python manage.py runserver
    ```
    
3. Launh Redis in a Docker container
   ```bash
    $ docker run -p 6379:6379 redis
    ```

4. Launch Vue
   ```bash
    $ npm run serve
   ```


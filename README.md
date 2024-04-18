1.Create posgres container with password.
docker run --name postgresdb -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=240383 -p 5432:5432 -v /Users/olenamaliarenko/documents/data:/var/lib/postgresql/data -d postgres

2. show all containers

docker ps -a

3. create migrations
 alembic revision --autogenerate -m "init"

4.apply migration

alembic upgrade head

5. docker stop ID container

6. docker start или restart ID container

7. docker attach ID container (під`єднатися до контейнера)

8. docker logs ID container (почему упал контейнер читает логи) 

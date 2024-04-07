# Introduction
In this project, I introduce a sample project on how we can use Docker Compose (YANL) to containerize a python (Flask) based application and PostgreSQL database with mounted volume. The Flask application runs a special thread that accesses 
one of the data sets available on the World Bank webnsite and this thread can be condigured from the yaml file. Then it save JSON file in PostgreSQL that has a spcial inverted index GIN that speeds up the queries about JSON against the database 

# Docker Hub Link 
I'll pubish the image on [Docker hub](https://hub.docker.com/r/maenmulhem/docker_search_engine_api/tags)

# Goals
The target here is not showing a complete user friendly flask application, rather shwoing three main things:
1. Showing how we can compose docker files and apply the concept of multistaging using Docker and Docker Compose
2.   1. It's quiet useful to see how we can run a Python(FLask) web application that runs on Virtual Environment in Docker
     2. It's good to see how we can save the data permenantly using the mounting volume
     3. By using multisatge in docker, we minimize the final image size and it's an important technique to optimize the image
     4. 1. In the Dokcer file of Flask, we build the app, and the we move to other two stages Runner and db_initializer. The db_initializer shows how we can run a special command in Flask to create the requied scheme and
           whereas the runner shows how we can run the Flask application 
3. Showing the benifits of using Inverted Index like Gin in PostgreSQL to access JSON files save in a special column in the database
4. Showing how we can run a thread in Python (Flask)

# How to Run
At the begingin, make sure that you created your own `.env` file and list the following configuration inside it :

```
POSTGRES_HOST: db
POSTGRES_DB: mytest
POSTGRES_USER: postgres
POSTGRESS_PASSWORD: test123
CRAWLER_RUN: no
```
First you should be sure you run PostgreSQL inmage and the database with the specified name is craeted and the required user to access the database is created and granted the privillage to do all opertaions from creating the sche,e
to apply the CRUD operations. 

Then you can run `docker compose up -d` and then you can check how the Flask console shows you the retrived data by the thread and od course you can check these data in PostgreSQL and you can query this data from the simple you 
provided. 

# To DO: Front End
Later, I'll publish a React project that allows the user to access this API on github and list the link here . 

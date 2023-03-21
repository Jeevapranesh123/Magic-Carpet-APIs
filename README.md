### Magic Carpet APIs

Simple implementation of E-Commerce book store APIs using [FastAPI](https://fastapi.tiangolo.com/) and MongoDB

#### Getting Started

1. Install Docker Engine [For Windows](https://docs.docker.com/desktop/windows/install/) , [For MacOSX](https://docs.docker.com/desktop/mac/install/) , [For Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

2. Install Docker Compose [For Ubuntu](https://docs.docker.com/compose/install/)

```
Note: Docker Compose Comes Default with Docker Desktop for Windows and MacOSX
```

3. Clone this Repository and cd /to/the/repository

4. Create Public and Private keys for authentication
```openssl genrsa -out private.pem 2048```
```openssl rsa -in private.pem -outform PEM -pubout -out public.pem```

5. Create Environment file from example.env

6. Run ```docker-compose up```

7. You should be able to see the Container getting build and once Built you should be able to see the container Logs

8. Once the build is done and the containers are up in running head to [Localhost](http://127.0.0.1/docs) in you Computer Browser to see swagger documentation of the APIs

9. That's it You are Good to go!

10. Report Bugs to `jeevadev02@gmail.com`


#### API Documentation

Features:

1. User Registration and Login
2. Add Books to inventory
3. List all books in Inventory
4. Add books to cart
5. Remove books from cart
6. Checkout cart

Note: All APIs are protected by JWT Authentication and Authorization, hence to make API calls acquire a JWT token from the Login API and use it in the Authorization Header of the API call
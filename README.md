### Magic Carpet APIs

Simple implementation of E-Commerce book store APIs using [FastAPI](https://fastapi.tiangolo.com/) and MongoDB

#### Getting Started

1. Install Docker Engine and Docker Compose

2. Clone this Repository and cd /to/the/repository

3. Create Public and Private keys for authentication
```
$ openssl genrsa -out private.pem 2048
$ openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```

4. Create Environment file from example.env

5. Run ```docker-compose up```

6. You should be able to see the Container getting build and once Built you should be able to see the container Logs

7. Once the build is done and the containers are up in running head to [Localhost](http://127.0.0.1/docs) in you Computer Browser to see swagger documentation of the APIs

8. That's it You are Good to go!

9. Report Bugs to `jeevadev02@gmail.com`


#### API Documentation

Features:

1. User Registration and Login
2. Add Books to inventory
3. List all books in Inventory
4. Add books to cart
5. Remove books from cart
6. Checkout cart

Note: All APIs are protected by JWT Authentication and Authorization, hence to make API calls acquire a JWT token from the Login API and use it in the Authorization Header of the API call
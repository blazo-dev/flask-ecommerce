# Flask E-Commerce API

This is a fully functional e-commerce API built using Flask, SQLAlchemy, Marshmallow, JWT, and MySQL. The API allows
managing users, products, and orders, with proper relationships between them. This project is designed to serve as the
backend for an e-commerce platform, providing RESTful endpoints for creating and managing users, products, and orders.

## Table of Contents

- [Installation](#installation)
- [Project Setup](#project-setup)
- [Models](#models)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Technologies Used](#technologies-used)

## Installation

To install the dependencies, use the following command:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries listed in the `requirements.txt` file.

## Project Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
    - On Mac/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:
    - Create a MySQL database named `flask_ecommerce_db`.
    - Update the `SQLALCHEMY_DATABASE_URI` in the `config.py` file with your MySQL connection details.

5. **Run the application**:
   ```bash
   flask run
   ```

## Models

The project includes the following database models, implemented using SQLAlchemy:

- **User Table**:
    - `id`: Integer, primary key, auto-increment
    - `name`: String
    - `address`: String
    - `email`: String (unique)

- **Order Table**:
    - `id`: Integer, primary key, auto-increment
    - `order_date`: DateTime
    - `user_id`: Integer, foreign key referencing User

- **Product Table**:
    - `id`: Integer, primary key, auto-increment
    - `product_name`: String
    - `price`: Float

- **Order_Product Association Table**:
    - `order_id`: Integer, foreign key referencing Order
    - `product_id`: Integer, foreign key referencing Product

## API Endpoints

The following endpoints are currently available:

### User Endpoints

- `GET /users`: Retrieve all users
- `GET /users/<id>`: Retrieve a user by ID
- `POST /users`: Create a new user
- `PUT /users/<id>`: Update a user by ID
- `DELETE /users/<id>`: Delete a user by ID

### Product Endpoints

- `GET /products`: Retrieve all products
- `GET /products/<id>`: Retrieve a product by ID
- `POST /products`: Create a new product
- `PUT /products/<id>`: Update a product by ID
- `DELETE /products/<id>`: Delete a product by ID

### Order Endpoints

- `POST /orders`: Create a new order
- `DELETE /orders/<order_id>`: Delete an order by ID
- `GET /orders/<order_id>/products`: Retrieve all products in an order
- `POST /orders/<order_id>/products`: Add a product to an order
- `DELETE /orders/<order_id>/products/<product_id>`: Remove a product from an order
- `GET /orders/user/<user_id>`: Retrieve all orders for a specific user

### JWT Authentication

- `GET /token`: Generate a JWT token for authentication

## Testing

- **Database Setup**: Ensure that calling `db.create_all()` creates all required tables in MySQL.
- **Postman**: Use Postman to test the API endpoints. A collection of example requests can be found in the `tests`
  folder.
- **MySQL Workbench**: Use MySQL Workbench to verify that data is correctly stored in the database.

## Technologies Used

- **Flask**: A micro web framework for Python used to build the API.
- **SQLAlchemy**: ORM used to interact with the MySQL database.
- **Flask-Marshmallow**: Used for serialization and validation of data.
- **JWT (JSON Web Tokens)**: Used for user authentication and securing API endpoints.
- **MySQL**: Database used to store user, order, and product data.
- **Flask-CORS**: Allows Cross-Origin Resource Sharing (CORS) for the API.

---

This project is still under development. Stay tuned for updates!
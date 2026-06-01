# Restaurant Order Management System

## Overview

Restaurant Order Management System is an enterprise-style web application developed using Django and Django REST Framework.

The system allows customers to browse menu items, place orders, process payments, and track order status. It also provides administrative features for restaurant management and payment approval workflows.

The project was developed as part of the Information Systems Engineering course.

---

## Features

### Authentication

* User registration and login
* Google OAuth2 authentication
* Session-based authentication

### Restaurant Management

* Menu categories management
* Menu items management
* Restaurant tables management
* CRUD operations for all entities

### Order Management

* Shopping cart functionality
* Checkout process
* Order status tracking
* Customer order history

### Payment System

* Online payment simulation (BLIK Sandbox)
* Offline payment approval
* Failed payment handling
* Payment status tracking

### Asynchronous Processing

* RabbitMQ message broker
* Celery workers
* Background notifications
* Payment processing tasks

### API Documentation

* Swagger/OpenAPI documentation
* REST API endpoints

### Testing

* Automated unit tests
* Integration tests
* Coverage reports

---

## Technology Stack

### Backend

* Python 3.13
* Django
* Django REST Framework

### Database

* MySQL

### Asynchronous Processing

* RabbitMQ
* Celery

### Authentication

* Google OAuth2

### API Documentation

* Swagger / drf-spectacular

### Testing

* pytest
* coverage

### Project Management

* GitHub Projects

---

## Project Architecture

Frontend → Django → MySQL Database

Django → RabbitMQ → Celery Worker

Celery → Payment Processing & Notifications

---

## BLIK Sandbox Simulation

The project includes a sandbox payment simulation inspired by the Polish BLIK payment system.

### Successful Codes

```text
111111
222222
333333
```

### Failed Codes

```text
999999
888888
777777
```

Successful payments create approved orders, while failed payments automatically reject orders.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/stronger1999/restaurant-order-system.git
cd restaurant-order-system
```

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database

Create a MySQL database and update database settings inside:

```text
restaurant_system/settings.py
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Administrator

```bash
python manage.py createsuperuser
```

---

## Running the Application

### Terminal 1 – RabbitMQ

```bash
rabbitmq-server.bat
```

### Terminal 2 – Celery

```bash
celery -A restaurant_system worker -l info -P solo --without-gossip --without-mingle --without-heartbeat
```

### Terminal 3 – Django

```bash
python manage.py runserver
```

---

## API Documentation

Swagger documentation is available at:

```text
http://127.0.0.1:8000/api/docs/
```

---

## Automated Tests

Run tests:

```bash
coverage run -m pytest
```

Generate coverage report:

```bash
coverage report
```

---

## Project Requirements Coverage

* REST API Architecture
* OAuth2 Authentication
* Online Payment Integration
* Offline Payment Approval
* Failed Payment Handling
* RabbitMQ Message Queues
* Celery Background Tasks
* Automated Testing
* Swagger/OpenAPI Documentation
* GitHub Sprint Methodology

---

## Authors
Mhad saghir b
Soufyan L
Information Systems Engineering Project

Restaurant Order Management System

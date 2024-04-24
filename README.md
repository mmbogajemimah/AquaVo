# AquaVo

# Customer Refill Tracking and Water Delivery System

## Description

This project is a web application designed to track customers and their refill dates, manage the delivery of water, and handle the accounting part of the financials. The backend of the system is implemented in Django, providing the necessary APIs for managing customers, refills, deliveries, and financial transactions. The frontend is built using React, providing an intuitive user interface for interacting with the system.

## Features

- **Customer Management:** Create, update, and delete customer profiles.
- **Refill Tracking:** Record and monitor refill dates for each customer.
- **Water Delivery Management:** Track the delivery of water to customers.
- **Financial Accounting:** Manage financial transactions including payments and invoices.
- **Authentication and Authorization:** Secure access to the system with user authentication and authorization.
- **Responsive Design:** Access the system from various devices with a responsive user interface.

## Technologies Used

### Backend:
- **Django:** Python web framework for building robust backend applications.
- **Django REST Framework:** Toolkit for building Web APIs using Django.
- **Django ORM:** Object-Relational Mapping for interacting with the database.
- **Django Authentication System:** Built-in authentication system for user management.
- **PostgreSQL:** Relational database management system for storing data.
  
### Frontend:
- **React:** JavaScript library for building user interfaces.
- **React Router:** Library for routing in React applications.
- **Axios:** HTTP client for making requests to the backend APIs.
- **CSS:** Styling the frontend components.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   ```
## Navigate to the backend directory and install dependencies:
```cd backend
pip install -r requirements.txt
```

## Set up the database:
python manage.py migrate

## Run the Django development server:
python manage.py runserver

## Navigate to the frontend directory and install dependencies:
```
cd frontend
npm install
```

## Start the React development server:
```
npm start
```
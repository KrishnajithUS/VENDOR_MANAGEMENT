# Vendor Management System(Using Django Rest Framework)

A Vendor Management System with Performance Metrics

## Technologies Used:

* Django Rest Framework
* Knox

## **Installation**
____
Vendor Management System can be installed on your system by following the below commands.

### **Python Installation**
___

**Ubuntu**

Ubuntu comes with Python pre-installed, but if you need to install a specific version or if Python is not installed, you can use the terminal to install it.

Open the terminal and type the following command:
```bash
  sudo apt-get install python3
```
This will install the latest version of Python 3.

To check if Python is installed correctly, type the following command:
```bash
python3 --version
```
This should output the version number of Python that you just installed.

**Windows**

To install Python on Windows, follow these steps:
1. Download the latest version of Python from the official website: https://www.python.org/downloads/windows/ .
2. Run the installer and select "Add Python to PATH" during the installation process. 
3. Choose the installation directory and complete the installation process.
4. To check if Python is installed correctly, open the Command Prompt and type the following command:
```bash
python3 --version
```
This should output the version number of Python that you just installed.

**macOS**

macOS comes with Python pre-installed, but if you need to install a specific version or if Python is not installed, you can use Homebrew to install it. 

Follow these steps:
1. Install Homebrew by running the following command in the terminal:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Install Python by running the following command in the terminal:
```bash
brew install python
```
To check if Python is installed correctly, type the following command in the terminal:
```bash
python3 --version
```
This should output the version number of Python that you just installed.

## Setup Project
1. Clone the resporitory: `git clone `
2. Change current directory to `VENDOR_MANAGEMENT` folder:`cd VENDOR_MANAGEMENT`
3. Create a virutal evrironment:

It is highly recommended to create a virtual environment before installing Django.

A virtual environment allows you to isolate your Python environment and avoid conflicts with other Python packages that may be installed on your machine.

To create a virtual environment, open the terminal and navigate to the directory where you want to create the environment. Then type the following command:
```bash
python -m venv myenv
```
This will create a new virtual environment named "myenv".

To activate the virtual environment, type the following command:
```bash
source myenv/bin/activate
```
This will activate the virtual environment and you should see the name of the environment in the terminal prompt.

>Note that to activate your virtual environment on Widows, you will need to run the following code below (See this <a href="https://docs.python.org/3/library/venv.html">link</a> to fully understand the differences between platforms):
```bash
 env/Scripts/activate.bat //In CMD
 env/Scripts/Activate.ps1 //In Powershel

4. Install all backend dependencies with pipenv: `pip install requirements.txt`.
5. Run `python3 manage.py makemigrations` & `python3 manage.py migrate`.
6. Run Server : `python3 manage.py runserver`
7. Create a new user
   ```bash
   python manage.py createsuperuser
   ```
   
# API Docs

## Introduction

This document outlines the RESTful API endpoints provided by our application. It covers the methods, request formats, response formats, required fields, and additional details for each endpoint.

## Base URL

The base URL for all endpoints is `http://localhost:8000/api`

## Endpoints

### Authentication

### Test Credentials

email = admin@gmail.com, password = admin@123


#### `POST /login/`


- **Description:** Generate Token.
- **Permissions:** Authenticated and UnAuthenticated User's.
- **Request Format:**
  ```json
        {
            "email":"string (required)",
            "password":"string (required)"
        }
  ```
- **Response Format:**
  ```json
        {
        "expiry": "string",
        "token": "string"
        }
  ```

### How to pass Authorization Header

To access authenticated endpoints, include the token in the Authorization header with the format `Authorization: Token <token>`.

### Date Format

Any dates in request body must be `yyyy-mm-dd` format.

### Status Codes

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |
| 204 | `NO CONTENT` |



### Vendor 

#### `GET /vendors/`

- **Description:** Retrieve a list of all vendors.
- **Permissions:** Authenticated users only.
- **Response Format:**
  ```json
        [
            {
                "vendor_code": "string",
                "name": "string",
                "contact_details": "string",
                "address": "string"
            }
        ]
  ```

#### `GET /vendors/{vendor_id}/`

- **Description:** Retrieve a specific vendor's details.
- **Permissions:** Authenticated users only.
- **Response Format:**
  ```json
          {
                "vendor_code": "string",
                "name": "string",
                "contact_details": "string",
                "address": "string"
        }
  ```

#### `POST /vendors/`

- **Description:**  Create a new vendor.
- **Permissions:** Authenticated users only.
- **Request Format:**
  ```json
          {
                "vendor_code": "string (required)(primary key)",
                "name": "string (required)",
                "contact_details": "string (required)",
                "address": "string (required)"
        }
  ```
- **Response Format:**
  ```json
          {
                "vendor_code": "string",
                "name": "string",
                "contact_details": "string",
                "address": "string"
        }
  ```

#### `PUT /vendors/{vendor_code}/`

- **Description:**  Update a vendor's details.
- **Info:**  Vendor code cannot be changed.
- **Permissions:** Authenticated users only.
- **Request Format:**
  ```json
          {
                "vendor_code": "string (required)",
                "name": "string (required)",
                "contact_details": "string (required)",
                "address": "string (required)"
        }
  ```
- **Response Format:**
  ```json
          {
                "vendor_code": "string",
                "name": "string",
                "contact_details": "string",
                "address": "string"
        }
  ```

#### `DELETE /vendors/{vendor_code}/`

- **Description:**  Delete a vendor.
- **Permissions:** Authenticated users only.


### Purchase Order

#### `GET /purchase_orders/?vendor_id={vendor_code}`

- **Description:** List all purchase orders with an option to filter by vendor.
- **Permissions:** Authenticated users only.
- **Info:**  query params vendor_id is optional.
- **Response Format:**
  ```json
        [
            {
                    "po_number": "string",
                    "order_date": "string",
                    "expected_delivery_date": "string",
                    "actual_delivery_date": "string",
                    "items": "{'product':'new'}",
                    "quantity": Integer,
                    "status": "pending",
                    "quality_rating": float,
                    "issue_date": "string",
                    "acknowledgment_date": "string",
                    "vendor": "string"
                }
        ]
  ```

#### `GET /purchase_orders/{po_number}/`

- **Description:**  Retrieve details of a specific purchase order.
- **Permissions:** Authenticated users only.
- **Response Format:**
  ```json
           {
                    "po_number": "string",
                    "order_date": "string",
                    "expected_delivery_date": "string",
                    "actual_delivery_date": "string",
                    "items": "{'product':'new'}",
                    "quantity": Integer,
                    "status": "pending",
                    "quality_rating": float,
                    "issue_date": "string",
                    "acknowledgment_date": "string",
                    "vendor": "string"
            }
  ```

#### `POST /purchase_orders/`

- **Description:**   Create a purchase order.
- **Permissions:** Authenticated users only.
- **Info:** status options can be pending, completed, cancelled.
- **Request Format:**
  ```json
        {
            "po_number": "string (required)",
            "expected_delivery_date": "string (required)",
            "actual_delivery_date": "string (optional)",
            "items": json (required),
            "quantity": integer (required),
            "quality_rating": float (optional),
            "status": "string (required)",
            "vendor": vendor_code string (required)
        }
  ```
- **Response Format:**
  ```json
    {
        "po_number": "string",
        "order_date": "string",
        "expected_delivery_date": "string",
        "actual_delivery_date": "string",
        "items": "string",
        "quantity": integer,
        "status": "string",
        "quality_rating": float,
        "issue_date": "string",
        "acknowledgment_date": "string",
        "vendor": "string"
    }
  ```

#### `PUT /purchase_orders/{po_number}/`

- **Description:**  Update a purchase order.
- **Info:**  po_number cannot be changed.
- **Permissions:** Authenticated users only.
- **Request Format:**
  ```json
        {
            "po_number": "string (required)",
            "expected_delivery_date": "string (required)",
            "actual_delivery_date": "string (optional)",
            "items": json (required),
            "quantity": integer (required),
            "quality_rating": float (optional),
            "status": "string (required)",
            "vendor": vendor_code string (required)
        }
  ```
- **Response Format:**
  ```json
    {
        "po_number": "string",
        "order_date": "string",
        "expected_delivery_date": "string",
        "actual_delivery_date": "string",
        "items": "string",
        "quantity": integer,
        "status": "string",
        "quality_rating": float,
        "issue_date": "string",
        "acknowledgment_date": "string",
        "vendor": "string"
    }
  ```

#### `DELETE /vendors/{po_number}/`

- **Description:**   Delete a purchase order.
- **Permissions:** Authenticated users only.



###  Vendor Performance

#### `GET /vendors/{vendor_code}/performance/`

- **Description:**  Retrieve a vendor's performance metrics.
- **Permissions:** Authenticated users only.
- **Response Format:**
  ```json
    {
        "vendor_code": "string",
        "name": "string",
        "on_time_delivery_rate": float,
        "quality_rating_avg": float,
        "average_response_time": float,
        "fulfillment_rate": float
    }
  ```


###  Vendor Update Acknowledgment

#### `GET /purchase_orders/{po_number}/acknowledge/`

- **Description:**  Vendors to acknowledge POs.
- **Permissions:** Authenticated users only.
- **Request Format:**
  ```json
        {
            "acknowledgment_date": "string"

        }
  ```
- **Response Format:**
  ```json
    {
        "vendor": "string",
        "name": "string",
        "acknowledgment_date": "string"
    }
  ```

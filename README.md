# Python Authentication System

[![CodeQL](https://github.com/susantabiswas/python-jwt-template/actions/workflows/codeql.yml/badge.svg)](https://github.com/susantabiswas/python-jwt-template/actions/workflows/codeql.yml)

Authentication is one of the most important things one would want in a service.
This is an authentication system using JWT.

This project is not a ready to use production system but rather shows the various aspects involved for making an authentication service. 

> JWT is a widely used authentication method for backend APIs. It allows users to securely access resources by providing a token that verifies their identity. This token contains encoded user information and is validated by the server for each request.

# Table of Contents
- [Python Authentication System](#python-authentication-system)
- [Table of Contents](#table-of-contents)
- [Project Setup](#project-setup)
  - [Install Dependencies](#install-dependencies)
  - [Setup Databases](#setup-databases)
  - [Run Tests](#run-tests)
  - [Run the Server](#run-the-server)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
    - [Salient points](#salient-points)
- [Usage](#usage)
  - [REST APIs](#rest-apis)
    - [Register a user](#register-a-user)
    - [Login](#login)
    - [Logout](#logout)
    - [User details](#user-details)
- [References](#references)

# Project Setup

## Install Dependencies

## Setup Databases
## Run Tests
## Run the Server

# Project Structure

# Architecture

### Salient points
>
    1. Password Hashing 
    2. JWT Token generation
    3. JWT token invalidation/blocking
    4. High code coverage using unittest


# Usage
## REST APIs
The authentication system supports the following APIs:

### Register a user
Adds a new user to the system
```
/auth/signup
```

### Login
Verifies the credentials and returns a auth JWT
```
/auth/login
```
### Logout
Logs the user out and invalidates the JWT associated with it.
```
/auth/logout
```

### User details
User resource related operations
```
/auth/user
```

# References
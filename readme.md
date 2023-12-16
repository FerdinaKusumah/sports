# Sports applications

This project is for showing rank league sports

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Getting Started and Installation](#getting-started-and-installation)
- [Unittest](#unittest)

## Introduction

This sports application displays teams and league information, designed with simplicity in mind. It is intentionally kept lightweight, relying solely on Django without the need for additional libraries. The primary goal is to minimize code dependencies and keep the application as streamlined as possible.

## Features

 * Authenticate and authorize users
 * Manage teams by adding, editing, and deleting
 * Manage tournaments by adding, editing, and deleting
 * Perform bulk data insertion using csv files
 * Display team statistics
 * Present team rankings

## Requirements

 * Python version 3.10+
 * Django version 5.0
 * Poetry (see [this](https://python-poetry.org/docs/) for installation)
 * Make

## Getting Started and Installation

 * Install poetry (see [this](https://python-poetry.org/docs/) for installation)
 * Install all dependencies by execute this command `make install`
 * Run migration by execute `make migrations && make migrate`
 * If you want all data is ready you can restore example data by execute `make restore`
   * Otherwise you can create new user by execute this command `poetry run python manage.py createsuperuser` to create new users  
 * Run the server by using `make run` then the server will run at port `8000`
 * Login using default credential `admin` and password `admin` to login with example data

## Unittest
 * To run all unit test execute this command `make test`

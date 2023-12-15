# Sports applications

This project is for showing rank league sports

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Getting Started and Installation](#getting-started-and-installation)

## Introduction

Sports applications that showing teams and league information

## Features

 * Add, edit and delete `teams`
 * Add, edit and delete `tournament`
 * Bulk insert data using `csv`
 * Showing statistic for each teams
 * Showing rank for each teams

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
 * Run the server by using `make run` then the server will run at port `8000`


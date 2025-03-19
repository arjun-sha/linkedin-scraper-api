<div align="center" style="text-align: center --force;">
  <img src="/assets/logo.png" style="width: 8%; height: auto;" alt="Logo" />
  <h1 align="center" style="text-align: center --force; "><a href='https://playwright.dev'>Linkedin</a> Scraper API </h1>

  <a href="https://code.turbolab.in/research-and-development/playwright-turnstile/-/tree/master?ref_type=heads">
    <img src="https://img.shields.io/badge/python-%3E%3D3.8-orange" alt="Python Version">
  </a>

  <a href="https://github.com/ambv/black">
        <img src="https://img.shields.io/badge/code%20style-black-black.svg">
    </a>
  <a href="https://github.com/PyCQA/isort">
        <img src="https://img.shields.io/badge/imports-isort-yellow.svg">
    </a>
  <a>
    <img src="https://img.shields.io/badge/Developed-Arjun-orange" alt="Support">
  </a>
</div>

## Overview

This is a FastAPI-based project that scrapes LinkedIn profiles and their connections. The API logs in using Selenium and retrieves profile details using LinkedIn's Voyager API.

---

## Features

- ✅ Undetactable Login Automation with Selenium and Selenium stealth.
- ✅ Scrape profile data asynchronously to increase the speed.
- ✅ Secure API authentication.
- ✅ Cookie Caching system
- ✅ Internal HTTP request retry mechanism.
- ✅ Smart Proxy Rotation
- ✅ Evades TLS level bot detections.

## Upcoming Features

- ✅ Smart Cookie Updations.
- ✅ Integration of DB for Cookie Caching

---

## Getting Started

#### Running locally

1. Clone the repository:

```shell
$ git clone git@github.com:arjun-sha/linkedin-scraper-api.git
```

2. Installing dependencies

```shell
$ cd linkedin-scraper-api
$ pip install -r requirements.txt
```

3. Start the FastAPI server:

_For Linux Baed Systems_

```shell
$ sh start_server.sh
```

_For Others_

```shell
$ gunicorn -c guvicorn_config.py --access-logfile - --error-logfile - --log-level debug linkedin_scraper.web.main:main
```

#### Build with Docker

1. After cloning the project, Navigate to the project directory

```shell
$ cd linkedin-scraper-api
```

2. Build the docker container with docker-compose

```shell
$ docker-compose build
```

3. Start Fast API server with the container

```shell
$ docker-compose up
```

#### Possible Errors

1. If `5000` port is already in use. Kill the port with the following command

_Linux_

```shell
sudo kill -9 $(sudo lsof -t -i:5000)
```
---

## Usage

#### End-Points

1. **Profile Page Scraper**

```
/api/profile
```

**Usage with python**

```python
import requests

url = "http://<host>:<port>/api/profile"

data = {
    "x_api_key": "<Your  API KEY>",
    "email": "<email>",
    "password": "<password>"
}

response = requests.post(url=url, json=data)
```

It will return the profile details of the logged-in user.

**Fields**

- ✅ public_id
- ✅ full_name
- ✅ headline
- ✅ summary
- ✅ industry_name
- ✅ location
- ✅ skills
- ✅ experience
- ✅ education
- ✅ email
- ✅ phone

**Sample Data**

<img src="/assets/profile_data.png" style="width: 75%; height: auto;"/>




---

1. **Connections Scraper**

```
/api/connections
```

This API work in a chunk mode. Each page return a set of connections and a pagination-id. For getting the next page we can use that pagination-id as shown here.

**For scraping first Page connections**

```python
import requests

url = "http://<host>:<port>/api/connections"

data = {
    "x_api_key": "<Your  API KEY>",
    "email": "<email>",
    "password": "<password>"
}

response = requests.post(url=url, json=data)
```

**Output**

```json

{
    "profiles": [<data>],
    "pagination_id": <next_pagination_id>
}

```

**For scraping next page**

```python
import requests

url = "http://<host>:<port>/api/connections"

data = {
    "x_api_key": "<Your  API KEY>",
    "email": "<email>",
    "password": "<password>",
    "pagination_id": "<pagination ID from previous response>"
}

response = requests.post(url=url, json=data)
```


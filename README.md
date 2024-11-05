# Bimedoc Technical Test

Django REST API to extract URL information (domain, title, images, stylesheets) and track Bitcoin-EUR and EUR-GBP rates using Blockchain and ECB APIs.

## Table of Contents

- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Clone the Project](#clone-the-project)
  - [Configuration Environment Variables](#configuration-environment-variables)
  - [Using Docker](#using-docker)
  - [Using PDM](#using-pdm)
  - [Using pip and Virtual Environment](#using-pip-and-virtual-environment)
- [Documentation API Endpoints](#documentation-api-endpoints)
  - [Postman collection](#postman-collection)
  - [Endpoints](#endpoints)
    - [URLInfo Endpoints](#urlinfo-endpoints)
      - [Create URL Info](#create-url-info)
      - [Get All URL Info](#get-all-url-info)
      - [Get URL Info by Public ID](#get-url-info-by-public-id)
      - [Delete URL Info by Public ID](#delete-url-info-by-public-id)
      - [Get or Delete URL Info by URL](#get-or-delete-url-info-by-url)
    - [Crypto Bitcoin Endpoint](#crypto-bitcoin-endpoint)
      - [Retrieve Bitcoin Prices and Exchange Rate Data](#retrieve-bitcoin-prices-and-exchange-rate-data)

## Demo

Live demo of the API is available at [https://bimedoc-technical-test.onrender.com/](https://bimedoc-technical-test.onrender.com/).

> [!Info]  
> Please note that loading may take a few seconds on the first visit due to the use of the free card.

## Prerequisites

- Python 3.12 or higher
- Install [PDM](https://pdm-project.org/) (recommended package manager)
- Docker (optional)

## Getting Started

To get started with the application in your local environment, follow these steps:

### Clone the Project

```bash
git clone https://github.com/Macktireh/bimedoc-technical-test.git
```

```bash
cd bimedoc-technical-test
```

### Configuration Environment Variables

Before running the application, you need to configure the environment variables. Make sure to create a `.env` file based on the provided example file `.env.example`. You can copy the contents of `.env.example` and save it as .env, then update the variables with your actual values.

### Using Docker

If you have Docker installed, you can use the provided `docker-compose.yml` file to run the application in a container. To do this, follow these steps:

1. Build and start the container:

   ```bash
   docker-compose up -d
   ```

2. Access the application at `http://localhost:8000`.

3. Stop the container:

   ```bash
   docker-compose down
   ```

### Using PDM

If you don't have Docker installed, you can use PDM to manage the project dependencies and run the application. To do this, follow these steps:

1. Install the project dependencies:

    ```bash
    pdm install
    ```

2. migrate the database:

    ```bash
    pdm run migrate
    ```

3. Start the application:

    ```bash
    pdm run dev
    ```

4. Access the application at `http://localhost:8000`.


### Using pip and Virtual Environment

If you don't have Docker or PDM installed, you can use pip and virtual environment to manage the project dependencies and run the application. To do this, follow these steps:

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

3. Install the project dependencies:

    ```bash
    pip install -r requirements/base.txt
    ```

4. migrate the database:

    ```bash
    python src/manage.py migrate
    ```

5. Start the application:

    ```bash
    python src/manage.py runserver
    ```

6. Access the application at `http://localhost:8000`.


## Documentation API Endpoints

The application provides a RESTful API for managing and retrieving URL information and accessing Bitcoin price data. It consists of two main components:

- **URLInfo API:** Manages and stores information related to various URLs, including details like domain, protocol, and additional metadata.
- **Crypto Bitcoin API:** Retrieves current Bitcoin prices in EUR and GBP, along with the latest EUR to GBP exchange rate.

The API is designed for efficient data access, making it suitable for applications requiring up-to-date URL metadata and cryptocurrency data.

## Postman collection

You can try out the API endpoints in the Postman collection `postman-collection.json` in the root directory of the project. This collection contains examples of how to use the API endpoints.

To use the Postman collection, you need to import it into your Postman client. Here's how:

1. Open Postman.
2. Click on the "Import" button in the top-right corner of the screen.
3. Select the "Import from Link" option.
4. Enter the URL of the Postman collection file in the "Link" field.
5. Click on the "Import" button.
6. You can now use the Postman collection to interact with the API endpoints.

## Endpoints

### URLInfo Endpoints

#### Create URL Info

Creates URL information in the database.

**URL:** `/api/v1/urlinfo/`

**Request Body Parameters:**

- `url` (required) - URL to create information for. Example: `{"url": "http://example.com"}`

**Response:**

```
{
    "detail": "The URL info has been successfully created"
}
```

#### Get All URL Info

Fetches all stored URL information.

**URL:** `/api/v1/urlinfo/`

**Response:**

```
[
    {
        "publicId": "123e4567-e89b-12d3-a456-426614174000",
        "url": "http://example.com",
        "protocol": "http",
        "subdomain": "www",
        "domainName": "example.com",
        "fullDomainName": "www.example.com",
        "title": "Example Site",
        "images": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
        "stylesheetCount": 2,
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-02T14:00:00Z"
    },
    ...
]
```

#### Get URL Info by Public ID

Fetches specific URL information by public ID.

**URL:** `/api/v1/urlinfo/detail/{public_id}`

**Path Parameter:**

- `public_id` (required) - Unique identifier for the URL info. Example: `123e4567-e89b-12d3-a456-426614174000`

**Response:**

```
{
    "publicId": "123e4567-e89b-12d3-a456-426614174000",
    "url": "http://example.com",
    "protocol": "http",
    "subdomain": "www",
    "domainName": "example.com",
    "fullDomainName": "www.example.com",
    "title": "Example Site",
    "images": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
    "stylesheetCount": 2,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-02T14:00:00Z"
}
```

#### Delete URL Info by Public ID

Deletes a specific URL info entry by public ID.

**URL:** `/api/v1/urlinfo/detail/{public_id}`

**Path Parameter:**

- `public_id` (required) - Unique identifier for the URL info.

**Response:**

```
{
    "detail": "The URL info has been successfully deleted"
}
```

#### Get or Delete URL Info by URL

Fetches or deletes URL information based on the URL parameter.

**URL:** `/api/v1/urlinfo/detail/?url={url}`

**Query Parameter:**

- `url` (required) - URL to retrieve or delete information for. Example: `?url=http://example.com`

**Response:**

**GET:**

```
{
    "publicId": "123e4567-e89b-12d3-a456-426614174000",
    "url": "http://example.com",
    "protocol": "http",
    "subdomain": "www",
    "domainName": "example.com",
    "fullDomainName": "www.example.com",
    "title": "Example Site",
    "images": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
    "stylesheetCount": 2,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-02T14:00:00Z"
}
```

**DELETE:**

```
{
    "detail": "The URL info has been successfully deleted"
}
```

### Crypto Bitcoin Endpoint

#### Retrieve Bitcoin Prices and Exchange Rate Data

Fetches Bitcoin price in EUR, exchange rate from EUR to GBP, and Bitcoin price in GBP.

**URL:** `/api/v1/crypto/bitcoin/`

**Response:**

```
{
    "bitcoin_eur": 34000.5,
    "eur_to_gbp": 0.86,
    "bitcoin_gbp": 29240.43
}
```







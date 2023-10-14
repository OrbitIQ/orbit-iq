# orbit-iq

## Overview

The `orbit-iq` project comprises several services, which are defined in the `docker-compose.yml`:

1. **API**: This is the backend service, built from the context in `./api`. It runs on port `8080`.
2. **Website**: This is the frontend service, built from the context in `./website`. It runs on port `3000`.
3. **Database (DB)**: A PostgreSQL database service running on port `5432`.
4. **init-db**: A service to initialize the database.

## Prerequisites

1. Install Docker: [Official Docker Installation Guide](https://docs.docker.com/get-docker/)
    * Docker Desktop is reccomended, it should auto install Docker Compose too if I remember correctly
2. Install Docker Compose: [Official Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

## Running the services

1. **Starting all services**:
    ```bash
    docker-compose up
    ```

    If you want to run the services in the background, you can use the `-d` flag:
    ```bash
    docker-compose up -d
    ```

    You can then view the logs using:
    ```bash
    docker-compose logs -f
    ```

    This command will start the `api`, `website`, `db`, and `init-db` services. However, if you are working on the website, you might want to run the website locally without Docker (details in the next section).

2. **Stopping the services**:
    ```bash
    docker-compose down
    ```

## Development: Working on the Website

If you're developing for the website, you might not want to run the website service using Docker. Here's how you can run the other services using Docker and the website locally:

1. Start only the required services:

    ```bash
    docker-compose up api db init-db
    ```

    This will only start the `api` and `db`
    and `init-db` services.

2. Navigate to the `website` directory:

    ```bash
    cd website
    ```

3. Start the website (assuming you have Node.js installed):

    Install dependencies
    ```bash
    npm install
    ```

    Start the website
    ```bash
    npm run dev
    ```

    This will start the website on port 3000 (or the port specified in your configuration).

4. Once done, remember to stop the Docker services:

    ```bash
    docker-compose down
    ```

## Notes

- Ensure that the ports 8080 (for API), 3000 (for Website), and 5432 (for PostgreSQL) are available on your machine, if you get an error in the docker logs about the port being in use, you should stop the service using that port.
- The database data is persisted using Docker volumes. If you want to reset the database, you can remove the volume using `docker volume rm orbit-iq_db-data`.


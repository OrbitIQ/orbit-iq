# orbit-iq

## Overview

The `orbit-iq` project comprises several services, which are defined in the `docker-compose.yml`:

1. **API**: This is the backend service, built from the context in `./api`. It runs on port `8080`.
2. **Website**: This is the frontend service, built from the context in `./website`. It runs on port `3000`.
3. **Database (DB)**: A PostgreSQL database service running on port `5432`.
4. **init-db**: A service to initialize the database.
5. **crawler**: A service that runs every 24h to crawl various websites for satellite data and dump it into the table `crawler_dump`
6. **validator**: A service that creates proposed changes to the `official_satellites` table based on the data in `crawler_dump` after doing some validation and data integrity checks.

## Prerequisites

1. Install Docker: [Official Docker Installation Guide](https://docs.docker.com/get-docker/)
   - Docker Desktop is reccomended, it should auto install Docker Compose too if I remember correctly
2. Install Docker Compose: [Official Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

## Running the services

1. **Starting all services**:

   ```bash
   docker-compose up
   ```

   We probably should be running the following command, which will force docker to rebuild the images. So that we don't run into weird caching issues with Docker using old images even if we've made changes.

   ```bash
   docker-compose up --build --force-recreate
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

### Tests:

1. Build and Run the Testing Services:

   ```bash
   docker-compose -f docker-compose.test.yml up --build integration_api_test
   ```

2. Or directly run the Testing Services:

   ```bash
   docker-compose -f docker-compose.test.yml up integration_api_test
   ```

## Notes

- Ensure that the ports 8080 (for API), 3000 (for Website), and 5432 (for PostgreSQL) are available on your machine, if you get an error in the docker logs about the port being in use, you should stop the service using that port.
- The database data is persisted using Docker volumes. If you want to reset the database, you can remove the volume using `docker volume rm orbit-iq_db-data`.

## Documentation

### Tables

`official_satellites` - The list of confirmed satellites, the goal of this table is to be a single source of truth for all confirmed satellites. This is what should be exported when UCS publishes a new list of satellites.

`official_satellite_changelog` - A log of all changes to the `official_satellites` table. This is used to see historical changes and trends to the list of satellites.

`crawler_dump` - Pretty unstructured data of the data that the web crawler finds. This is just raw data that is used by the `validator` to create proposed changes

`proposed_changes` - These are proposed changes that the `validator` creates from combining data from the `crawler_dump` data and doing data integrity and validation on the data the web crawler has detected which may be incorrect.
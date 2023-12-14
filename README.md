# OrbitIQ

This is a project created for helping maintainers of the [Union of Concerned Scientists (UCS)'s Satellite Database](https://www.ucsusa.org/resources/satellite-database) to keep track of satellites and their data. It web scrapes various websites for satellite data and then uses that data to create proposed changes to the UCS Satellite Database. The maintainers can then review the proposed changes and accept or reject them.

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

## Demo
TODO

## Built With
[![Docker][Docker]][docker-url] [![React][React.js]][React-url] [![TailwindCSS][TailwindCSS]][tailwindcss-url] [![Python][Python]][python-url] [![Flask][Flask]][flask-url] [![PostgreSQL][PostgreSQL]][postgresql-url]

## Contributors
This was a project created as part of Amber Field's CS 639 Capstone class at The University of Wisconsin - Madison. Here's the team that worked on it!

<div align="center">
    <a href="https://github.com/AdamSchmidty">
      <img src="https://github.com/AdamSchmidty.png" width="100" height="100" alt="Adam Schmidt">
    </a>
    <a href="https://github.com/davidteather">
      <img src="https://github.com/davidteather.png" width="100" height="100" alt="David Teather">
    </a>
    <a href="https://github.com/Gugu0099">
      <img src="https://github.com/Gugu0099.png" width="100" height="100" alt="Gulinazi Julati">
    </a>
    <a href="https://github.com/nori210">
      <img src="https://github.com/nori210.png" width="100" height="100" alt="Georgia Li">
    </a>
    <a href="https://github.com/rudyb2001">
      <img src="https://github.com/rudyb2001.png" width="100" height="100" alt="Rudy Banerjee">
    </a>
    <a href="https://github.com/stevenlai1688">
      <img src="https://github.com/stevenlai1688.png" width="100" height="100" alt="Steven Lai">
    </a>
  </div>

| GitHub Profile | LinkedIn Profile | Full Name         |
| -------------- | ---------------- | ----------------- |
| [AdamSchmidty](https://github.com/AdamSchmidty) | [LinkedIn](https://www.linkedin.com/in/adam-m-schmidt) | Adam Schmidt |
| [davidteather](https://github.com/davidteather) | [LinkedIn](https://www.linkedin.com/in/davidteather) | David Teather |
| [Gugu0099](https://github.com/Gugu0099) | [LinkedIn](https://www.linkedin.com/in/gulinazi-julati/) | Gulinazi Julati |
| [nori210](https://github.com/nori210) | [LinkedIn](https://www.linkedin.com/in/jiaxuan-li-1ba857294) | Georgia Li |
| [rudyb2001](https://github.com/rudyb2001) | [LinkedIn](https://www.linkedin.com/in/anirudhbanerjee) | Rudy Banerjee |
| [stevenlai1688](https://github.com/stevenlai1688) | [LinkedIn](https://www.linkedin.com/in/steven-yisiang-lai) | Steven Lai |


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

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/OrbitIQ/orbit-iq.svg?style=for-the-badge
[contributors-url]: https://github.com/OrbitIQ/orbit-iq/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/OrbitIQ/orbit-iq.svg?style=for-the-badge
[forks-url]: https://github.com/OrbitIQ/orbit-iq/network/members
[stars-shield]: https://img.shields.io/github/stars/OrbitIQ/orbit-iq.svg?style=for-the-badge
[stars-url]: https://github.com/OrbitIQ/orbit-iq/stargazers
[issues-shield]: https://img.shields.io/github/issues/OrbitIQ/orbit-iq.svg?style=for-the-badge
[issues-url]: https://github.com/OrbitIQ/orbit-iq/issues
[license-shield]: https://img.shields.io/github/license/OrbitIQ/orbit-iq.svg?style=for-the-badge
[license-url]: https://github.com/OrbitIQ/orbit-iq/blob/master/LICENSE.txt
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=FFFFFF
[Docker-url]: https://www.docker.com/
[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=FFFFFF
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=FFFFFF
[Python-url]: https://www.python.org/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=FFFFFF
[postgresql-url]: https://www.postgresql.org/
[TailwindCSS]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=FFFFFF
[tailwindcss-url]: https://tailwindcss.com/
[product-screenshot]: images/screenshot.png
[demo-url]: todo
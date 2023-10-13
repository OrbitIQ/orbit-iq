# 1. Build stage: Using an official Node.js runtime as a parent image
FROM node:16 AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build the app for production
RUN npm run build

# 2. Serve stage: Serve the built app using a lightweight node server or any other server of your choice
FROM node:16

# Set the working directory
WORKDIR /app

# Copy the built app from the previous stage
COPY --from=build /app/dist ./dist

# Globally install a server (serve is used as an example, but you can use any server of your choice)
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Command to serve the app
CMD ["serve", "-s", "dist", "-l", "3000"]

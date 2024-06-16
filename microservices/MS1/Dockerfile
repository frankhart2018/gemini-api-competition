# Use an official Node.js runtime as the base image
FROM node:slim

# Set the working directory in the Docker image
WORKDIR /usr/src/app

# Copy package.json and package-lock.json into the Docker image
COPY package*.json ./

# Install the project dependencies inside the Docker image
RUN npm install

# If you are building your code for production
# RUN npm ci --only=production

# Copy the rest of the project files into the Docker image
COPY . .

# Expose port 3000 for the application
EXPOSE 4000

# Define the command to run the application
CMD [ "node", "app.js" ]
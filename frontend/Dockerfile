# Stage 1: Build the React application
FROM node:18-alpine AS builder
# Alpine images are typically multi-arch and good for ARM.
# If specific ARM is needed and node:18-alpine doesn't work,
# one might use arm64v8/node:18-alpine or similar.

WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock if you use Yarn)
# This step leverages Docker layer caching. If these files haven't changed,
# Docker won't re-run npm install.
COPY package.json ./
# Assuming npm is used, copy package-lock.json. If yarn, use yarn.lock.
# If neither exists, this line can be omitted, but it's good practice.
COPY package-lock.json ./

# Install dependencies
# If using yarn: RUN yarn install --frozen-lockfile
RUN npm install

# Copy the rest of the frontend application code
COPY . .

# Build the React application for production
# This command should match the build script in your package.json
RUN npm run build

# Stage 2: Serve the built application with Nginx
FROM nginx:alpine
# nginx:alpine is also generally multi-arch.

# Nginx server port
EXPOSE 80

# Remove default Nginx configuration
# RUN rm /etc/nginx/conf.d/default.conf # Optional, can just overwrite

# Copy custom Nginx configuration for SPA
# This will be created as frontend/nginx.conf and copied here
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the static build files from the 'builder' stage to Nginx's web root
# The build output directory is typically 'build' or 'dist' for React apps.
# Create React App usually outputs to 'build'.
COPY --from=builder /app/build /usr/share/nginx/html

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]

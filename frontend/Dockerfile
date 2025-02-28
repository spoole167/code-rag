# Use official Node.js image
FROM node:18
WORKDIR /app

# Install dependencies
COPY package.json  ./
RUN npm install

# Copy app files
COPY . .

# Build React app
RUN npm run build

# Serve the app with a lightweight server
CMD ["npx", "serve", "-s", "build"]

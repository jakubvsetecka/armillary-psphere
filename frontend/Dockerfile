FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install

EXPOSE 3000

# Instead of copying all files and building, we'll mount the source at runtime
# and use npm start which typically runs the dev server with file watching
CMD ["npm", "start"]

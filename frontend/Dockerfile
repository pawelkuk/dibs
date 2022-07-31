FROM node:alpine
WORKDIR /frontend
ENV PATH /frontend/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm i --prefix ./
COPY . ./
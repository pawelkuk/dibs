FROM node
WORKDIR /read-model
ENV PATH /read-model/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm i --prefix ./
COPY . ./
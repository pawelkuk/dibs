FROM node
WORKDIR /benchmark
ENV PATH /benchmark/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm i --prefix ./
COPY . ./

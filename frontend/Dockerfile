FROM node
WORKDIR /home/node
RUN mkdir app
COPY . /home/node/app
WORKDIR /home/node/app
RUN npm install
CMD ["npm", "start", "dev"]
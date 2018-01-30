FROM node

ENV NODE_ENV=production
WORKDIR /usr/src/app
COPY . /usr/src/app/

RUN yarn install && \
    yarn global add gulp && \
    gulp build

EXPOSE 3003

CMD ["yarn", "run", "server"]

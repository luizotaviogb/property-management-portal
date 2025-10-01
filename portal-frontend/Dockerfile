FROM node:22.17.0 as build
WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn
COPY . .
RUN npm run build --prod

FROM nginx:stable-alpine
COPY --from=build /usr/src/app/dist/portal-frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
# syntax=docker/dockerfile:1
FROM hugomods/hugo:exts AS build
WORKDIR /src
COPY site/ /src/
RUN hugo --minify

FROM caddy:2-alpine
COPY --from=build /src/public /srv
COPY docker/Caddyfile.container /etc/caddy/Caddyfile
EXPOSE 8080

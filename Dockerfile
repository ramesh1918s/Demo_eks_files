
FROM nginx:1.25-alpine

LABEL maintainer="vayubus-team"
LABEL app="vayubus"
LABEL version="1.0.0"

# install curl for healthcheck
RUN apk add --no-cache curl

# remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# copy app files
COPY src/ /usr/share/nginx/html/

# copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# expose port
EXPOSE 8080

# healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
CMD curl -f http://127.0.0.1:8080/health || exit 1

CMD ["nginx", "-g", "daemon off;"]

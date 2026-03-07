
FROM nginx:1.25-alpine

LABEL maintainer="vayubus-team"
LABEL app="vayubus"
LABEL version="1.0.0"

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy app
COPY src/ /usr/share/nginx/html/

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup \
    && chown -R appuser:appgroup /usr/share/nginx/html \
    && chown -R appuser:appgroup /var/cache/nginx \
    && chown -R appuser:appgroup /var/log/nginx \
    && touch /var/run/nginx.pid \
    && chown appuser:appgroup /var/run/nginx.pid

USER appuser

EXPOSE 8080

# Updated healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD wget -q --spider http://localhost:8080 || exit 1

CMD ["nginx", "-g", "daemon off;"]

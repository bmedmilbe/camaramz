FROM nginx:alpine

ARG CACHE_BYPASS=1 

# Copy to templates instead of overwriting default.conf directly
COPY local.conf /etc/nginx/templates/default.conf.template

CMD ["/bin/sh", "-c", "envsubst '$CERTIFICATES_URL $REMITTANCE_URL $TOUR_URL $CMS_URL' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]

EXPOSE 80
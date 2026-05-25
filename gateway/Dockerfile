FROM nginx:alpine
# Copy to templates instead of overwriting default.conf directly
COPY local.conf /etc/nginx/templates/default.conf.template
EXPOSE 80
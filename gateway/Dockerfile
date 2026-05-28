FROM nginx:alpine

ARG CACHE_BYPASS=1 

# 1. Wipe out both conf.d and the template folders to ensure no auto-generation interferes
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/templates/*

# 2. Copy your template to override nginx.conf.template directly
COPY local.conf /etc/nginx/templates/nginx.conf.template

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80
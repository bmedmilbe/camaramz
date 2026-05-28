FROM nginx:alpine

ARG CACHE_BYPASS=1 

# 1. Clear out the default configuration so it doesn't conflict
RUN rm -f /etc/nginx/conf.d/default.conf

# 2. Copy your template to the templates directory
COPY local.conf /etc/nginx/templates/default.conf.template

# 3. Clean up the CMD. The official Nginx image automatically runs envsubst 
#    on any .template file in that directory and starts the server natively.
CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80
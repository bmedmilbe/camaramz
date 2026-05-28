FROM nginx:alpine

ARG CACHE_BYPASS=1 

# 1. Clean out the out-of-the-box file completely
RUN rm -f /etc/nginx/conf.d/default.conf

# 2. FIX: Rename this to local.conf.template. 
# This outputs to /etc/nginx/conf.d/local.conf, completely avoiding default.conf conflicts.
COPY local.conf /etc/nginx/templates/local.conf.template

# 3. Environment variable telling Nginx entrypoint NOT to try modifying ports on its own
ENV NGINX_ENTRYPOINT_LOCAL_RESOLVERS=1

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80
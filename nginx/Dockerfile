FROM nginx:1.25

# Eliminar configuraciones por defecto
RUN rm /etc/nginx/conf.d/default.conf

# Copiar configuración principal
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar configuración de sitios
COPY conf.d/aladino.conf /etc/nginx/conf.d/

# Crear directorio para certificados SSL
RUN mkdir -p /etc/letsencrypt/live/www.altasfundacionaladina.org && \
    mkdir -p /etc/letsencrypt/live/api.altasfundacionaladina.org
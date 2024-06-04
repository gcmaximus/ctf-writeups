# docker build -t never-gonna-tell-a-lie-and-type-you . && docker run -p 8080:8080 -t never-gonna-tell-a-lie-and-type-you
FROM erseco/alpine-php-webserver

USER root

ARG FLAG=GPNCTF{fake_flag}
RUN echo "$FLAG" > /flag.txt

WORKDIR /var/www/html

# Copy your PHP files to the container
COPY --chmod=0744 index.php .
USER nobody

# Expose port 8080 for the PHP server
EXPOSE 8080

# Start the PHP server
CMD ["php", "-S", "0.0.0.0:8080"]

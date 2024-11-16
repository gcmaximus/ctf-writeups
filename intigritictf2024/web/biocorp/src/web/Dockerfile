FROM php:apache

# Copy application files and set permissions
COPY app/ /var/www/html/
COPY flag.txt /flag.txt

# Enable mod_rewrite for Apache
RUN a2enmod rewrite

# Set all files in /var/www/html to be owned by root and read-only for www-data
RUN chown -R root:root /var/www/html && chmod -R 755 /var/www/html

# Make the flag file read-only and owned by root
RUN chmod 444 /flag.txt && chown root:root /flag.txt

# Set the working directory
WORKDIR /var/www/html

# Expose the port
EXPOSE 80

# Run Apache in the foreground
CMD ["apache2-foreground"]

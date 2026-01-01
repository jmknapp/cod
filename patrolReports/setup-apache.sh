#!/bin/bash
# Setup Apache2 with SSL for USS Cod Patrol Reports
# Run as root or with sudo

set -e

DOMAIN="codpatrols.com"

echo "=== Setting up Apache2 for $DOMAIN ==="

# 1. Enable required Apache modules
echo "Enabling Apache modules..."
a2enmod ssl
a2enmod rewrite
a2enmod proxy
a2enmod proxy_http
a2enmod headers
a2enmod expires

# 2. Copy site configs
echo "Installing site configurations..."
cp /home/jmknapp/cod/patrolReports/codpatrols-http.conf /etc/apache2/sites-available/codpatrols.conf
cp /home/jmknapp/cod/patrolReports/codpatrols-ssl.conf /etc/apache2/sites-available/codpatrols-ssl.conf

# 3. Enable HTTP site first (for Certbot)
echo "Enabling HTTP site..."
a2ensite codpatrols.conf

# 4. Test and reload Apache
echo "Testing Apache configuration..."
apache2ctl configtest
systemctl reload apache2

echo ""
echo "=== HTTP site is now live ==="
echo ""
echo "Next steps to enable HTTPS:"
echo ""
echo "1. Run Certbot to get SSL certificate:"
echo "   sudo certbot --apache -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "2. After certbot succeeds, enable the SSL site:"
echo "   sudo a2ensite codpatrols-ssl.conf"
echo "   sudo systemctl reload apache2"
echo ""
echo "3. Certbot should have already set up auto-renewal."
echo "   Verify with: sudo certbot renew --dry-run"
echo ""

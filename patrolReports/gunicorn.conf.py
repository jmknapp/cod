"""
Gunicorn configuration for USS Cod Patrol Reports
Production deployment at /var/www/html/codpatrols
"""
import multiprocessing

# Binding
bind = "127.0.0.1:5013"

# Workers
workers = 4
worker_class = "sync"
timeout = 120

# Logging
accesslog = "/var/log/codpatrols/access.log"
errorlog = "/var/log/codpatrols/error.log"
loglevel = "info"

# Process naming
proc_name = "codpatrols"

# Working directory
chdir = "/var/www/html/codpatrols"

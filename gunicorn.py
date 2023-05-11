workers = 4
max_requests = 1000
timeout = 30
bind = "127.0.0.1:8000"
preload_app = True
accesslog = "gunicorn/log/access.log"
errorlog = "gunicorn/log/error.log"

echo "Starting local workers"

celery -A main.celery worker -l info
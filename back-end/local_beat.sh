echo "Starting local beat for celery tasks"

celery -A main.celery beat --max-interval 1 -l info
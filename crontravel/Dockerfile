FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN ls -alt
RUN pip3 install -r requirements.txt --no-cache-dir 
# CMD ["gunicorn", "crontravel.wsgi:application", "--bind", "0:8000"]
CMD ["python", "manage.py", "runserver", "0:8000"]
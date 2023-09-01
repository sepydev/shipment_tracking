FROM python:3.10.13-alpine3.18

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app
copy requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

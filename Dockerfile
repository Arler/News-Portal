from python:3.13-slim
WORKDIR /NewsPortalApp
COPY ./requirements.txt /NewsPortalApp/
RUN pip install -r requirements.txt
COPY ./NewsPortal .
CMD ["sh", "-c", "python manage.py migrate &&\
    python manage.py runserver 0.0.0.0:8000"]
EXPOSE 8000
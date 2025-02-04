FROM python:3.7
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install ca-certificates && rm -rf /var/cache/apk/*
COPY ./host.crt /usr/local/share/ca-certificates
RUN update-ca-certificates
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PYTHONPATH="$PYTHONPATH:/app"
CMD python ./src/controllers/controller.py cloud

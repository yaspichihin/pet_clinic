FROM python:3.10.9

RUN mkdir /pet_clinic

WORKDIR /pet_clinic

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "./wsgi.py"]
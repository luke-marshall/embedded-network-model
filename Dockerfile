FROM python:2.7         
ADD . /simulation
WORKDIR /simulation
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]
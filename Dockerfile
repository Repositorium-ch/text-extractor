FROM downloads.unstructured.io/unstructured-io/unstructured:0.12.6

RUN python3.10 -m pip install flask waitress

COPY ./app/app.py /usr/src/app.py

CMD ["python3", "-u", "/usr/src/app.py"]

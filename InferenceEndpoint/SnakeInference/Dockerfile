FROM mxnet/python:latest_cpu_mkl_py3

RUN pip install bottle
RUN pip install numpy

WORKDIR /home/model

COPY main.py /home/model/main.py
COPY api.py /home/model/api.py
COPY convert_utils.py /home/model/convert_utils.py

COPY *.params /home/model/
COPY *-symbol.json /home/model/

EXPOSE 8080

ENTRYPOINT ["python3", "main.py"]


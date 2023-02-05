FROM python:3.11.1-slim-buster

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ngc-chaos ./ngc-chaos

CMD ["bash"]
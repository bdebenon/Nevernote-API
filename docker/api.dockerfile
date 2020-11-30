FROM python:3.7

# Download repo
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/bdebenon/Nevernote-API.git && cd Nevernote-API && git checkout ca71c32

# Install dependencies:
RUN pip install -r /Nevernote-API/requirements.txt

WORKDIR /Nevernote-API

#ENTRYPOINT [ "python" ]
ENTRYPOINT [ "sleep" ]
CMD [ "100000"]
#CMD [ "app.py"]

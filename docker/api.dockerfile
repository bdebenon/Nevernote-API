FROM python:3.7

# Download repo
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/bdebenon/Nevernote-API.git && cd Nevernote-API && git checkout c3a56e0

# Install dependencies:
RUN pip install -r /Nevernote-API/requirements.txt

WORKDIR /Nevernote-API

ENTRYPOINT [ "python" ]
CMD [ "app.py", "-i", "0.0.0.0", "-p", "80"]


FROM python:3.6
MAINTAINER GaetanoCarlucci <gaetano.carlucci@gmail.com>

RUN apt-get update -q && apt-get install git && apt-get clean
RUN cd / && git clone https://github.com/GaetanoCarlucci/CPULoadGenerator.git /CPULoadGenerator
RUN pip install -r /CPULoadGenerator/requirements.txt

WORKDIR /CPULoadGenerator
ENTRYPOINT ["./CPULoadGenerator.py"]
CMD ["--help"]

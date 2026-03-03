FROM python:3.13
LABEL maintainer="GaetanoCarlucci <gaetano.carlucci@gmail.com>"

RUN apt-get update -q && apt-get install git && apt-get clean
RUN cd / && git clone https://github.com/GaetanoCarlucci/CPULoadGenerator.git /CPULoadGenerator
RUN pip install -r /CPULoadGenerator/requirements.txt

WORKDIR /CPULoadGenerator
ENTRYPOINT ["./cpu_load_generator.py"]
CMD ["--help"]

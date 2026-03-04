# Image to run the CPU load generator in a container.
# Build: docker build -t cpuloadgen .
# Run:   docker run --rm cpuloadgen -c 0 -l 0.2 -d 10
FROM python:3.13
LABEL maintainer="GaetanoCarlucci <gaetano.carlucci@gmail.com>"

RUN apt-get update -q && apt-get install git && apt-get clean
RUN cd / && git clone https://github.com/GaetanoCarlucci/CPULoadGenerator.git /CPULoadGenerator
RUN pip install -r /CPULoadGenerator/requirements.txt

WORKDIR /CPULoadGenerator
ENTRYPOINT ["python", "cpu_load_generator.py"]
CMD ["--help"]

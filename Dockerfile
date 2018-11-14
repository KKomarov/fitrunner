FROM python:3.7.1-stretch

RUN mkdir -p /usr/share/man/man1 && \
    apt-get update && apt-get install -y --no-install-recommends \
    default-jre

RUN mkdir /FitNesse \
  && curl -fsSL -o fitnesse-standalone.jar "http://www.fitnesse.org/fitnesse-standalone.jar?responder=releaseDownload&release=20180127"

EXPOSE 7080

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD java -Xmx256m -jar fitnesse-standalone.jar -p 7080

USER 1000:1000

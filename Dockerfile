FROM java:latest

RUN mkdir /FitNesse \
  && curl -fsSL -o fitnesse-standalone.jar "http://www.fitnesse.org/fitnesse-standalone.jar?responder=releaseDownload&release=20180127"

EXPOSE 80
CMD java -Xmx256m -jar fitnesse-standalone.jar

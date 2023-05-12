FROM maven:3.3-jdk-8

# 	instalacja biblioteki do synchronizowania plików
RUN echo "deb [check-valid-until=no] http://cdn-fastly.deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list
RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list
RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list
RUN apt -o Acquire::Check-Valid-Until=false update
RUN apt install rsync -y

# katalog projektu 
WORKDIR /usr/src/mymaven

#	nazwa aplikacji
ENV APP_NAME=*.jar
# 	katalog z lokalizacja targeta po buildzie
ENV TARGET_DIR=/target
# 	polecenie budowania
ENV BUILD_CMD="mvn clean install"
# 	profile budowania
ENV BUILD_PROFILES=

# 	punkt startowy kontenra
COPY ./start.sh /start.sh
RUN chmod 777 /start.sh
ENTRYPOINT /start.sh
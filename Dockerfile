FROM centos

RUN yum install python3 -y

#Project files copy in directories
COPY cgi-bin /var/www/cgi-bin
COPY index.html /var/www/

#Files was created in Windows - convert it
RUN yum install dos2unix -y
RUN dos2unix /var/www/cgi-bin/login.py
RUN dos2unix /var/www/cgi-bin/logout.py
RUN dos2unix /var/www/cgi-bin/user.py
RUN dos2unix /var/www/cgi-bin/FileCookieRepository.py
RUN dos2unix /var/www/cgi-bin/FileUserRepository.py
RUN dos2unix /var/www/cgi-bin/UserClass.py

#Create files executable
RUN chmod +x /var/www/cgi-bin/login.py
RUN chmod +x /var/www/cgi-bin/logout.py
RUN chmod +x /var/www/cgi-bin/user.py
RUN chmod +x /var/www/cgi-bin/FileCookieRepository.py
RUN chmod +x /var/www/cgi-bin/FileUserRepository.py
RUN chmod +x /var/www/cgi-bin/UserClass.py

#Permitions for directories
RUN chmod 777 /var/www
RUN chmod 777 /var/www/cgi-bin

WORKDIR /var/www/

CMD python3 -m http.server --cgi 8000

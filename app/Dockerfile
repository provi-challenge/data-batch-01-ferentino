FROM python
WORKDIR /app_python
COPY . .
RUN apt-get update && apt-get -y install python3-pip 
RUN pip install requests \  
    pip install sqlalchemy \
    pip install psycopg2
#   pip install pandas\
#   pip install numpy

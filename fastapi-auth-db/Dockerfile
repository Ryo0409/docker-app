FROM python
USER root
WORKDIR /root

COPY main.py /root/
COPY api/ /root/api/
COPY common/ /root/common/

RUN apt-get update
RUN apt-get -y install locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN echo "set clipboard=unnamed,autoselect" > /root/.vimrc
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install fastapi[all]
RUN pip install sqlalchemy
RUN pip install python-jose[cryptography]
RUN pip install passlib[bcrypt]
RUN pip install psycopg2

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

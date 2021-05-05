FROM python:3.8-slim
MAINTAINER Chris Thomas

# copy local python scripts into container
WORKDIR /src
ADD producer.py palendromicoddnumber.py consumer.py queuewriter.py millerrabin.py aks_primality.py aprcl_primality.py get_ip.py staticfilewriter.py requirements.txt /src/

# create virtualenv
RUN python3 -m venv . \
    && . bin/activate \
    && pip3 install -r requirements.txt \
    && pip3 list

# puts virtualenv utils at top of path
# commands from inside container will run venv versions
# https://stackoverflow.com/questions/44077407/is-there-a-way-to-automatically-activate-a-virtualenv-as-a-docker-entrypoint
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
#
ENV VIRTUAL_ENV=/src
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["python"]

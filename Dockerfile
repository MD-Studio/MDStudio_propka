FROM mdstudio/mdstudio_docker3:0.0.1

COPY . /home/mdstudio/lie_propka

RUN chown mdstudio:mdstudio /home/mdstudio/lie_propka

WORKDIR /home/mdstudio/lie_propka

RUN pip install numpy scipy && pip install .

USER mdstudio

CMD ["bash", "entry_point_lie_propka.sh"]

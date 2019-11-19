FROM mdstudio/mdstudio_docker3:0.0.1

COPY . /home/mdstudio/mdstudio_propka

RUN chown -R mdstudio:mdstudio /home/mdstudio/mdstudio_propka
RUN chmod -R 755 /home/mdstudio

WORKDIR /home/mdstudio/mdstudio_propka

RUN pip install numpy scipy && pip install .

USER mdstudio

CMD ["bash", "entry_point_mdstudio_propka.sh"]

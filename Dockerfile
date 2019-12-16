FROM mdstudio/mdstudio_docker3:0.0.3

# Set permissions and install package
COPY . /home/mdstudio
RUN chown -R mdstudio:mdstudio /home/mdstudio
RUN chmod -R 755 /home/mdstudio
WORKDIR /home/mdstudio
RUN pip install numpy scipy && pip install .
USER mdstudio

# Set entrypoint and start process
CMD ["bash", "entry_point_mdstudio_propka.sh"]

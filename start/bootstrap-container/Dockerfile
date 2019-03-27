FROM centos:centos7

USER 0
ENV HOME=/home/bootstrap

RUN mkdir -p $HOME

ADD ./copy/ $HOME/
RUN chmod -R 777 $HOME

CMD ["/home/bootstrap/bootstrap"]
FROM centos:centos7

USER 0
ENV HOME=/home/rell

RUN mkdir -p $HOME

ADD ./copy/ $HOME/
RUN chmod -R 777 $HOME

CMD ["/home/rell/bootstrap"]
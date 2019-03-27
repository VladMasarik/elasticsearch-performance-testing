FROM centos:centos7

USER 0
ENV HOME=/home/rally

RUN yum install -y epel-release && \
    yum install -y gcc && \
    yum install -y python34.x86_64 python34-devel.x86_64 python34-pip.noarch && \
    yum install -y centos-release-scl && \ 
    yum install -y git19 

RUN pip3 install esrally

RUN mkdir -p $HOME

RUN esrally

ADD ./secret/ $HOME/secret/
ADD ./copy/ $HOME/copy/
RUN chmod -R 777 $HOME

CMD ["scl", "enable", "git19", "--", "sh", "$HOME/copy/scr"]
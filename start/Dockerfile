FROM centos:centos7

USER 0
ENV HOME=/home/rell

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

# --track-path=$HOME/copy \

# CMD esrally \
# --track=geopoint \
# --target-hosts=elasticsearch \
# --pipeline=benchmark-only \
# --client-options="use_ssl:true,verify_certs:false,ca_certs:'$HOME/secret/admin-ca',client_cert:'$HOME/secret/admin-cert',client_key:'$HOME/secret/admin-key'"

CMD ["scl", "enable", "git19", "--", "sh", "$HOME/copy/scr"]
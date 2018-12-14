FROM centos:centos7

RUN yum install -y epel-release

RUN yum install -y gcc python34.x86_64 python34-devel.x86_64 python34-pip.noarch centos-release-scl

RUN yum install -y git19 

RUN scl enable git19 bash

RUN pip3 install esrally

RUN esrally configure

ADD ./secret/ /secret/
ADD /home/origin/copy/ /copy/

CMD scl enable git19 bash

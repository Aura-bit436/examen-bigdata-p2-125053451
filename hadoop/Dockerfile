FROM alpine:3.20

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN apk add --no-cache \
    openjdk17-jdk \
    python3 \
    py3-pip \
    openssh \
    bash \
    wget \
    curl \
    tar \
    procps

RUN wget --progress=dot:giga https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz \
    -O /tmp/hadoop.tar.gz \
    && tar -xzf /tmp/hadoop.tar.gz -C /opt/ \
    && mv /opt/hadoop-3.3.6 /opt/hadoop \
    && rm /tmp/hadoop.tar.gz

RUN adduser -D -h /home/hadoop hadoop \
    && mkdir -p /run/sshd /home/hadoop/.ssh \
    && chmod 700 /home/hadoop/.ssh \
    && chown -R hadoop:hadoop /home/hadoop \
    && ssh-keygen -A \
    && echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config \
    && echo "PasswordAuthentication no" >> /etc/ssh/sshd_config \
    && echo "PermitRootLogin no" >> /etc/ssh/sshd_config

RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN printf '%s\n' \
    '<?xml version="1.0"?>' \
    '<configuration>' \
    '  <property>' \
    '    <name>mapreduce.framework.name</name>' \
    '    <value>local</value>' \
    '  </property>' \
    '</configuration>' \
    > /opt/hadoop/etc/hadoop/mapred-site.xml

RUN printf '%s\n' \
    '<?xml version="1.0"?>' \
    '<configuration>' \
    '  <property>' \
    '    <name>fs.defaultFS</name>' \
    '    <value>file:///</value>' \
    '  </property>' \
    '</configuration>' \
    > /opt/hadoop/etc/hadoop/core-site.xml

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]

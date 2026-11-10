FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    python3 \
    openssh-server \
    openssh-client \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xzf hadoop-3.3.6.tar.gz -C /opt/ && \
    mv /opt/hadoop-3.3.6 /opt/hadoop && \
    rm hadoop-3.3.6.tar.gz

RUN useradd -m -s /bin/bash usuario && \
    mkdir -p /var/run/sshd /home/usuario/.ssh /root/.ssh && \
    ssh-keygen -t rsa -P '' -f /home/usuario/.ssh/id_rsa && \
    cat /home/usuario/.ssh/id_rsa.pub >> /home/usuario/.ssh/authorized_keys && \
    chown -R usuario:usuario /home/usuario/.ssh && \
    chmod 700 /home/usuario/.ssh && chmod 600 /home/usuario/.ssh/authorized_keys && \
    ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

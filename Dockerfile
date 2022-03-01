# FROM - 所有Dockerfile的第一个指令都必须是 FROM ，
# 用于指定一个构建镜像的基础源镜像，如果本地没有就会从公共库中拉取，没有指定镜像的标签会使用默认的latest标签，
# 如果需要在一个Dockerfile中构建多个镜像，可以使用多次。
#基于的基础镜像
FROM python:3.7.0

# MAINTAINER - 描述镜像的创建者，名称和邮箱。
MAINTAINER tangzhuangkun

# 复制当前目录的所有文件到/usr/src/app/disguise目录下。
COPY . /usr/src/app/disguise

# COPY - 复制本机文件或目录，添加到指定的容器目录, 本例中将 requirements.txt 复制到镜像中。
# COPY ./requirements.txt /requirements.txt

# WORKDIR 指定工作目录
# 格式为 WORKDIR <工作目录路径>。如该目录不存在，WORKDIR 会帮你建立目录。
# 使用 WORKDIR 指令可以来指定工作目录（或者称为当前目录），以后各层的当前目录就被改为指定的目录,最好不要在RUN中用cd手动切换目录。
# 设置app文件夹是工作目录
WORKDIR /usr/src/app/disguise

RUN pip3 install -r /usr/src/app/disguise/requirements.txt

# ENTRYPOINT - 在启动容器的时候提供一个默认的命令项。
ENTRYPOINT [ "python3" ]

# RUN - 目录中的 disguise_controller.py 和 scheduler.py 。
CMD [ "/usr/src/app/disguise/disguise_controller.py","/usr/src/app/disguise/scheduler.py" ]
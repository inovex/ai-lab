FROM tensorflow/tensorflow:1.13.1-py3

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

ARG NB_USER="ai-lab"
ARG NB_UID="1000"
ARG WORKDIR="/rl"

# Install gym and conda dependencies
RUN apt-get update --fix-missing && \
    apt-get install -yq --no-install-recommends \
    xvfb xauth libglu1-mesa libgl1-mesa-dri python-opengl graphviz ffmpeg \
    wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV MINICONDA_VERSION 4.7.12.1
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENV BASH_ENV ~/.bashrc
SHELL ["/bin/bash", "-c"]

COPY requirements.txt /tmp/requirements.txt
COPY conda_env_cpu.yml /tmp/conda_env.yml

# Create conda environment
RUN conda env create -f /tmp/conda_env.yml
# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 /tmp/conda_env.yml | cut -d' ' -f2)" >> ~/.bashrc

# install requirements
RUN pip --no-cache-dir install -r /tmp/requirements.txt && \
    rm -rf /tmp/*

# create user -m (creates home if it doesn't exist) -s (users standard shell) -u (UID)
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER
USER $NB_UID

EXPOSE 8888
# serve jupyter notebooks from this folder
WORKDIR $WORKDIR

CMD source activate ai-lab-hska-rl && \
    jupyter lab --port=8888 --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password=''

FROM tensorflow/tensorflow:2.1.0-gpu-py3-jupyter

RUN apt-get update && apt-get install -y git wget tar 

RUN pip3 --no-cache-dir install \
    scipy scikit-image matplotlib pandas numpy opencv-python open3d mlflow && \
    python -m ipykernel.kernelspec

COPY ./config/jupyter_notebook_config.py /root/.jupyter/

# Jupyter has issues with being run directly:
# https://github.com/ipython/ipython/issues/7062
# We just add a little wrapper script.
COPY ./config/run_jupyter.sh /

# Jupyter
EXPOSE 8888

WORKDIR /

VOLUME "/notebooks"
WORKDIR "/notebooks"

CMD ["/run_jupyter.sh"]

FROM ivukotic/ml_base:latest

LABEL maintainer Ilija Vukotic <ivukotic@cern.ch>

# adding apache and neo4j

RUN wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
RUN echo 'deb https://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --allow-unauthenticated \
    apache2 \
    neo4j

##############################
# Python 2 packages
##############################

RUN pip2 --no-cache-dir install \
        h5py \
        tables \
        ipykernel \
        metakernel \
        jupyter \
        matplotlib \
        numpy \
        pandas \
        Pillow \
        scipy \
        sklearn \
        qtpy \
        seaborn \
        tensorflow-gpu \
        keras \
        elasticsearch \
        gym \
        graphviz \
        JSAnimation \
        Cython
RUN python2 -m ipykernel.kernelspec

#############################
# Python 3 packages
#############################

RUN pip3 --no-cache-dir install \
        h5py \
        tables \
        ipykernel \
        metakernel \
        jupyter \
        jupyterlab \
        matplotlib \
        numpy \
        pandas \
        Pillow \
        scipy \
        sklearn \
        qtpy \
        seaborn \
        tensorflow-gpu \
        keras \
        elasticsearch \
        gym \
        graphviz \
        JSAnimation \
        ipywidgets \
        Cython
RUN python3 -m ipykernel.kernelspec

# build info
RUN echo "Timestamp:" `date --utc` | tee /image-build-info.txt

COPY environment.sh /environment.sh
COPY run.sh    /run.sh
RUN chmod 755 /run.sh /environment.sh

RUN jupyter serverextension enable --py jupyterlab --sys-prefix

COPY jupyter_notebook_config.py /root/.jupyter/
RUN export SHELL=/bin/bash


#execute service
CMD ["/.run"]
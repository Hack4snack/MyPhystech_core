# set up miniconda
curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# restart terminal
conda config --set always_yes true
conda create -n phystech python=3.6
conda activate phystech
rm Miniconda3-latest-Linux-x86_64.sh

# install packages
conda install matplotlib numpy pandas scikit-learn tqdm
conda install -c anaconda django gensim requests
pip install vk
pip install natasha==0.10.0
pip install gensim==3.8.3
pip install yargy==0.12.0

# install BigARTM
apt-get install git build-essential libboost-all-dev cmake
pip install -U protobuf==3.10.0
git clone --branch v0.9.0 --depth=1 https://github.com/bigartm/bigartm.git
cd bigartm && mkdir build
cd build && cmake -DPYTHON=python3 ..
make
make install && export ARTM_SHARED_LIBRARY=/usr/local/lib/libartm.so

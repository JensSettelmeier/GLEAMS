![GLEAMS logo](images/logo_GLEAMS.png)

## GLEAMS

GLEAMS is a Learned Embedding for Annotating Mass Spectra. GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network to embed them into a 32-dimensional space in which spectra generated by the same peptide are close together. It then detects "spectrum communities" of spectra generated by the same peptide.

This repository contains the gleams module code, a file containing trained network weights, and scripts for encoding and embedding spectra.o

### System Requirements and installation

This code has been tested on a Ubuntu 16.04 LTS 64-bit machine with an Intel i7 6700k, Nvidia RTX (2070 and 2080 Ti tested), 24 GB Ram. Any modern Linux distribution should be fine. We strongly recommend using Anaconda to set up the python dependencies.
After cloning the repo, you can create an conda environment with the environment.yml file in the repo root folder.

```
cd GLEAMS
conda create environment.yml
```

We run it with the following dependencies:

absl-py                            0.9.0              
alabaster                          0.7.12             
alembic                            1.4.2              
altair                             3.3.0              
anaconda-client                    1.7.2              
anaconda-navigator                 1.9.12             
anaconda-project                   0.8.3              
apache-airflow                     1.10.6             
apricot-select                     0.4.1              
argcomplete                        1.10.3             
argh                               0.26.2             
asn1crypto                         1.3.0              
astor                              0.7.1              
astroid                            2.3.3              
astropy                            4.0                
atomicwrites                       1.3.0              
attrs                              19.3.0             
autopep8                           1.4.4              
Babel                              2.8.0              
backcall                           0.1.0              
backports.functools-lru-cache      1.6.1              
backports.shutil-get-terminal-size 1.0.0              
backports.tempfile                 1.0                
backports.weakref                  1.0.post1          
beautifulsoup4                     4.8.2              
bitarray                           1.2.1              
bkcharts                           0.2                
bleach                             3.1.0              
bokeh                              1.4.0              
boto                               2.49.0             
Bottleneck                         1.3.2              
brotlipy                           0.7.0              
cached-property                    1.5.1              
certifi                            2019.11.28         
cffi                               1.14.0             
chardet                            3.0.4              
Click                              7.0                
cloudpickle                        1.3.0              
clyent                             1.2.2              
colorama                           0.4.3              
colorlog                           4.0.2              
conda                              4.8.3              
conda-build                        3.18.11            
conda-package-handling             1.6.0              
conda-verify                       3.4.2              
configparser                       3.5.0              
contextlib2                        0.6.0.post1        
croniter                           0.3.30             
cryptography                       2.8                
cycler                             0.10.0             
Cython                             0.29.15            
cytoolz                            0.10.1             
dask                               2.11.0             
decorator                          4.4.1              
defusedxml                         0.6.0              
diff-match-patch                   20181111           
dill                               0.3.1.1            
distributed                        2.11.0             
docutils                           0.16               
entrypoints                        0.3                
et-xmlfile                         1.0.1              
faiss                              1.6.0              
fastcache                          1.1.0              
filelock                           3.0.12             
flake8                             3.7.9              
Flask                              1.1.1              
Flask-Admin                        1.5.3              
Flask-AppBuilder                   1.12.5             
Flask-Babel                        0.12.2             
Flask-Caching                      1.3.3              
Flask-Login                        0.4.1              
Flask-OpenID                       1.2.5              
Flask-SQLAlchemy                   2.4.0              
flask-swagger                      0.2.13             
Flask-WTF                          0.14.3             
fsspec                             0.6.2              
future                             0.18.2             
gast                               0.3.3              
gevent                             1.4.0              
glob2                              0.7                
gmpy2                              2.0.8              
google-pasta                       0.2.0              
graphviz                           0.14               
greenlet                           0.4.15             
grpcio                             1.23.0             
gunicorn                           19.9.0             
h5py                               2.10.0             
HeapDict                           1.0.1              
html5lib                           1.0.1              
hypothesis                         5.5.4              
idna                               2.8                
imageio                            2.6.1              
imagesize                          1.2.0              
importlib-metadata                 1.5.0              
intervaltree                       3.0.2              
ipykernel                          5.1.4              
ipython                            7.12.0             
ipython-genutils                   0.2.0              
ipywidgets                         7.5.1              
iso8601                            0.1.12             
isort                              4.3.21             
itsdangerous                       1.1.0              
jdcal                              1.4.1              
jedi                               0.14.1             
jeepney                            0.4.2              
Jinja2                             2.10.3             
joblib                             0.14.1             
json-merge-patch                   0.2                
json5                              0.9.1              
jsonschema                         3.2.0              
jupyter                            1.0.0              
jupyter-client                     5.3.4              
jupyter-console                    6.1.0              
jupyter-core                       4.6.1              
jupyterlab                         1.2.6              
jupyterlab-server                  1.0.6              
Keras                              2.2.5              
Keras-Applications                 1.0.8              
Keras-Preprocessing                1.1.0              
keyring                            21.1.0             
kiwisolver                         1.1.0              
lazy-object-proxy                  1.4.3              
libarchive-c                       2.8                
lief                               0.9.0              
llvmlite                           0.31.0             
locket                             0.2.0              
lockfile                           0.12.2             
lxml                               4.5.0              
Mako                               1.1.0              
Markdown                           2.6.11             
MarkupSafe                         1.1.1              
marshmallow                        3.5.0              
marshmallow-sqlalchemy             0.17.2             
matplotlib                         3.1.3              
mccabe                             0.6.1              
mistune                            0.8.4              
mkl-fft                            1.0.15             
mkl-random                         1.1.0              
mkl-service                        2.3.0              
mock                               4.0.1              
more-itertools                     8.2.0              
mpmath                             1.1.0              
msgpack                            0.6.1              
multipledispatch                   0.6.0              
multiprocessing-logging            0.3.0              
navigator-updater                  0.2.1              
nbconvert                          5.6.1              
nbformat                           5.0.4              
networkx                           2.4                
nltk                               3.4.5              
nose                               1.3.7              
notebook                           6.0.3              
numba                              0.48.0             
numexpr                            2.7.1              
numpy                              1.18.1             
numpydoc                           0.9.2              
olefile                            0.46               
openpyxl                           3.0.3              
packaging                          20.1               
pandas                             0.25.3             
pandocfilters                      1.4.2              
parso                              0.5.2              
partd                              1.1.0              
path                               13.1.0             
pathlib2                           2.3.5              
pathtools                          0.1.2              
patsy                              0.5.1              
pendulum                           1.4.4              
pep8                               1.7.1              
pexpect                            4.8.0              
pickleshare                        0.7.5              
Pillow                             7.0.0              
pip                                20.0.2             
pkginfo                            1.5.0.1            
pluggy                             0.13.1             
ply                                3.11               
prometheus-client                  0.7.1              
prompt-toolkit                     3.0.3              
protobuf                           3.11.0             
psutil                             5.6.7              
ptyprocess                         0.6.0              
py                                 1.8.1              
pyarrow                            0.15.1             
pycairo                            1.19.1             
pycocotools                        2.0                
pycodestyle                        2.5.0              
pycosat                            0.6.3              
pycparser                          2.19               
pycrypto                           2.6.1              
pycurl                             7.43.0.5           
pydocstyle                         4.0.1              
pyflakes                           2.1.1              
Pygments                           2.5.2              
pygpu                              0.7.6              
PyJWT                              1.7.1              
pylint                             2.4.4              
pyodbc                             4.0.0-unsupported  
pyOpenSSL                          19.1.0             
pyparsing                          2.4.6              
PyQt5                              5.12.3             
PyQt5-sip                          4.19.18            
PyQtWebEngine                      5.12.1             
pyrsistent                         0.15.7             
PySocks                            1.7.1              
pyteomics                          4.1.2              
pytest                             5.3.5              
pytest-arraydiff                   0.3                
pytest-astropy                     0.8.0              
pytest-astropy-header              0.1.2              
pytest-doctestplus                 0.5.0              
pytest-openfiles                   0.4.0              
pytest-remotedata                  0.3.2              
python-daemon                      2.1.2              
python-dateutil                    2.8.1              
python-editor                      1.0.4              
python-jsonrpc-server              0.3.4              
python-language-server             0.31.7             
python3-openid                     3.1.0              
pytz                               2019.3             
pytzdata                           2019.3             
PyWavelets                         1.1.1              
pyxdg                              0.26               
PyYAML                             5.3                
pyzmq                              18.1.1             
QDarkStyle                         2.8                
QtAwesome                          0.6.1              
qtconsole                          4.6.0              
QtPy                               1.9.0              
requests                           2.22.0             
rope                               0.16.0             
Rtree                              0.9.3              
ruamel-yaml                        0.15.87            
scikit-image                       0.16.2             
scikit-learn                       0.22.1             
scikit-optimize                    0.5.2              
scipy                              1.4.1              
seaborn                            0.10.0             
SecretStorage                      3.1.2              
Send2Trash                         1.5.0              
setproctitle                       1.1.10             
setuptools                         45.2.0.post20200210
simplegeneric                      0.8.1              
singledispatch                     3.4.0.3            
six                                1.14.0             
snowballstemmer                    2.0.0              
sortedcollections                  1.1.2              
sortedcontainers                   2.1.0              
soupsieve                          1.9.5              
spectrum-utils                     0.3.2              
Sphinx                             2.4.0              
sphinxcontrib-applehelp            1.0.1              
sphinxcontrib-devhelp              1.0.1              
sphinxcontrib-htmlhelp             1.0.2              
sphinxcontrib-jsmath               1.0.1              
sphinxcontrib-qthelp               1.0.2              
sphinxcontrib-serializinghtml      1.1.3              
sphinxcontrib-websupport           1.2.0                          
SQLAlchemy                         1.3.13             
statsmodels                        0.11.0             
sympy                              1.5.1              
tables                             3.6.1              
tabulate                           0.8.7              
tblib                              1.6.0              
tenacity                           4.12.0             
tensorboard                        1.14.0             
tensorflow                         1.14.0             
tensorflow-estimator               1.14.0             
termcolor                          1.1.0              
terminado                          0.8.3              
testpath                           0.4.4              
text-unidecode                     1.2                
Theano                             1.0.4              
thrift                             0.13.0             
toolz                              0.10.0             
tornado                            6.0.3              
tqdm                               4.42.1             
traitlets                          4.3.3              
typed-ast                          1.4.1              
typing-extensions                  3.7.4.1            
tzlocal                            1.5.1              
ujson                              1.35               
umap-learn                         0.3.10             
unicodecsv                         0.14.1             
urllib3                            1.25.8             
watchdog                           0.10.2             
wcwidth                            0.1.8              
webencodings                       0.5.1              
Werkzeug                           1.0.1              
wheel                              0.34.2             
widgetsnbextension                 3.5.1              
wrapt                              1.11.2             
WTForms                            2.3.1              
wurlitzer                          2.0.0              
xlrd                               1.2.0              
XlsxWriter                         1.2.7              
xlwt                               1.3.0              
xmltodict                          0.12.0             
yapf                               0.28.0             
zict                               1.0.0              
zipp                               2.2.0              
zope.deprecation                   4.4.0         

Further we used CUDA Version 10.0 and Driver Version 410.78, as well as cudnn version 7.4.1.

To be able to run it with a RTX Nvidia card you need to execute before at the beginning of your python session.

```
config_4RTX = tf.ConfigProto()
config_4RTX.gpu_options.allow_growth = True
```

If you also want to suppress the future warnings of tensorflow and Keras, add the following:

```
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    from tensorflow import keras
    from tensorflow.keras.preprocessing.text import Tokenizer
    from keras.backend.tensorflow_backend import set_session
    import tensorflow as tf
```



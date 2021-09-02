# SatLink Installation

SatLink needs a Python 3 installation to run. It is recommended an environment with python 3.9.

You can download Python in [python.org](https://www.python.org/downloads/).

To install, just copy all the folders and files to any directory and make sure all packages/libraries are installed.

## Packages

SatLink has dependencies and needs some packages to run. They are: [itur](https://pypi.org/project/itur/#description),
[Numpy](https://numpy.org/), [tqdm](https://github.com/tqdm/tqdm), [pathos](https://github.com/uqfoundation/pathos),
[pandas](https://pandas.pydata.org/), [Astropy](https://www.astropy.org/).

To use the graphical user interface, it also needs [PyQt5](https://riverbankcomputing.com/software/pyqt/intro).

One can install SatLink simply by running **first_setup.py**. It will install all the packages, including PyQt for the GUI usage.

Alternatively, run the following command:
    
    pip install -r requirements.txt

If an IDE, like [PyCharm](https://www.jetbrains.com/pt-br/pycharm/), 
is being used, it will automatically detect the requirements file and ask to install the packages (including PyQt).

Lastly, the packages can be installed individually. Here's the code with the currently tested versions:

    pip install itur==0.2.1
    pip install tqdm==4.56.0
    pip install pandas==1.2.1
    pip install pathos==0.2.7
    pip install astropy==4.2
    pip install pyqt5==5.15.2
    pip install matplotlib==3.4.1

##Using SatLink
Run **main_window.py** to start the user interface. Please refer to [GUI usage](gui_use.md) for more information.

For more detailed information about the code-based functions and classes, please refer to [Code-based usage](code_use.md).
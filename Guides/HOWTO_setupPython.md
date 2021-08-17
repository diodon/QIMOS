# HOW TO setup your Python environment

This document will guide you over the necessary steps to setup a Python working environment on you AIMS interactive HPC space. The idea of setting an enviroment is to have in your computer space a directory with all the packages you will need to run the **Ocean Observer** - **QIMOS** python tools.

You have to have access to AIMS interactive HPC using you AIMS credentials.

We will install the following packages: 

1. [xarray]: to manipulate netCDF files
2. [pandas]. to manipulate tabular data
3. [tabulate]. to format text tables
4. [argparse]. utility used to parse command line arguments

We will be using python 3.6 as it is the most stable version available in the AIMS HPC. Version 3.5, which is a very stable version has reached its end-of-life so many modern packages no longer work with this version

## Create your directory

Setup a directory where you will be working. In the HPC is better to work with the terminal: 

1. open a terminal session
2. create a new directory under your root folder:

    `mkdir ./QIMOS`

3. change your working directory to the newly created directory: 

    `cd QIMOS`

## Load Python

In the HPC you need to download the modules you plan to work with in every new terminal session you open. There are few modules available in the HPC. TO look at what is available do: 

    `module avail`

In the resulting list you will see *python/3.6.3*. To load this module: 

    `module load python/3.6.3`

Now you have python 3.6 available in your terminal. To check just type:

    `python3`

and you should see something similar to this: 

```
Python 3.6.3 (default, May  7 2019, 15:44:53) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-18)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

to quit python type `ctrl-d` 



## Create a virtual environment

We will create a new environment, inside the directory we've just created, that will contain all the packages and settings needed to run our python session. A python environment is a new directory with a specific internal structure of directories. You need to name the environment (e.g. *imos* ) as you will refer it by its name. You could also create many different environments, depending on your coding needs.

Let's create the *imos* environment. For this, type the following command (assuming that you're already in the QIMOS directory, check it with `pwd`):

    python3 -m venv imos

You can see that there is a new directory called *imos*. This is our environment and we need to *activate* it with the following command: 

    source imos/bin/activate

If the environment was successfully activated, you will see *(imos)* in the command prompt: 

    (imos) [<your user name>@hpc-interactive QIMOS]$

to de-activate your environment just type: 

    deactivate



## install python packages


Now we will install the basics python packages we will use. To install a package we use the command `pip`. pip is a package-management system written in Python used to install and manage software packages. Let's install `numpy`, the package used to manipulate multi-dimensional matrices: 

    pip install numpy

pip will collect the package files from the repository and install it into your environment:

```
(imos) [<your user name>@hpc-interactive QIMOS]$ pip install numpy
Collecting numpy
  Using cached https://files.pythonhosted.org/packages/45/b2/6c7545bb7a38754d63048c7696804a0d947328125d81bf12beaa692c3ae3/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl
Installing collected packages: numpy
Successfully installed numpy-1.19.5
You are using pip version 9.0.1, however version 21.2.4 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

```

Don't pay attention to the last message as we cannot upgrade the current version of pip (we need super-user permission)

Now install the packages: 

- xarray
- pandas
- argparse
- tabulate
- matplotlib

You can list the packages and its versions available in your environment with: 

    pip list







   






# HOW TO setup your Python environment

This document will guide you over the necessary steps to set up a Python working environment on a dedicated HPC machine. The idea of setting an environment is to have in your virtual computer space a directory with all the packages you will need to run the **Ocean Observer** - **QIMOS** python tools. You will be able to activate your environment and work with the tools without to be worried about package upgrades and version's compatibilities.

There many resources on the Internet to learn more about python environments, you can have a look for example at [here](https://realpython.com/python-virtual-environments-a-primer/) and [here](https://docs.python-guide.org/dev/virtualenvs/)

Also, to work with a python console, I recommend to use [ipython](https://ipython.org/) (interactive python) which has many features that easy the way of coding and testing. Ipython is well integrated with [jupyter](https://jupyter.org/), and eventually we will be running jupyter notebooks. Ipython is already installed in our machine


The following steps will guide you to: 

1. Login into our machine
2. Create a working directory
3. Create a python environment
4. Download the required python packages into your environment
5. Test python installation and packages
6. Download tools from Ocean Observer repository
7. Test some tools


## Access to our dedicated virtual machine

To have a standardised environment for all of us, we have configured a dedicated Ubuntu (linux) machine inside AIMS HPC. It is a modest installation, but it will allow us to run our python scripts. For the moment, we don't have a graphical interface (like Gnome), but we're working to have it soon. So, the only way to access our machine is using `ssh` from your terminal.

**TIP**: if you have access to AIMS fastX interactive environment, you can log in into our machine from a terminal window there. However, it doesn't mean that you will have graphic capabilities.

To access the machine type from your console: 

   `ssh 10.10.42.10`

and use your AIMS credentials to log in. You will enter into a linux terminal in your home directory. The name of the machine is *eklein-gdal*, so the prompt will be `<your-user-name>@eklein-gdal:~$ `



## Create your working directory

Set up a directory where you will be working. In the terminal session, create a new directory under your home folder:

    `mkdir ./OceanObserver`



## Create a python environment

As it was mentioned before, a python environment is a directory that contains all the packages you will need to run specific tools. You can always activate the environment and use the packages that are inside, independently of the packages installed system-wide or in other environments.

To create your python environment:

1. Move to you working directory: the environment will reside under this directory.

   `cd OceanObserver`.

2. change your working directory to the newly created directory: 

    `cd OceanObserver`

3. Initialise your <empty> new environment. *imos* is the name of your environment:

   `python3 -m venv imos`

4. Activate your environment. This will add *(imos)* at the beginning of your terminal prompt 

   `source imos/bin/activate`

5. List the packages and their corresponding version available in your environment. You should have just a couple of them:

   `pip list`

**NOTE:** to deactivate your python environment just type `deactivate`


## install python packages
 
Now you need to install some packages that are required to run the Ocean Observer scripts. You can do this by providing a list of packages, but it is much safer to do it one by one, so in case of an error we will be able to understand better what happened.

The packages you will install are: 

- **numpy**: Numerical python. this is the package needed to work with matrices. It is our main toolbox
- **netcdf4**: this is a basic package to work with netCDF files
- **xarray**: this package help us to work with netCDF files in a more easy way and incorporate many methods to manipulate, group, select and plot variables from a nc file
- **pandas**: this package works with tabular data. It should be installed automatically by **xarray** so no need to install it manually
- **matplotlib**: package to make plots. Its syntax is almost identical to the plotting functions in MATLAB
- **tabulate**: to format text tables

Having your environment activated, to install a package type: 

   `pip install <package name>`

example: 

   `pip install numpy`

Do this for all the packages listed above. You can check now the installed packages with: 

   `pip list`

You can continue to install new packages as needed. Remember that the packages will live inside your environment. Once you desactivate it, you won't be able to use it.



## Test python and packages

Currently, the version of python installed in our machine is 3.8.10. To invoque python type

   `python3`

The number 3 in necessary to make a distinction with pyton 2.7, which is also available in the system. You should have something similar to this in your terminal: 

```
Python 3.8.10 (default, Jun  2 2021, 10:49:15) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Let's now have a look to one of the mooring files. You will open a connection to a file stored in the [AODN THREDDS server](http://thredds.aodn.org.au/thredds/catalog/IMOS/catalog.html). This will not download the file. Only when you request the data, the specific data will be downloaded. You will use the `xarray `package. Follow these steps: 

1. load the xarray package: `import xarray as xr`
2. open a connection with a file. This is temperature file from GBRCCH mooring array: `nc = xr.open_dataset('http://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/QLD/GBRCCH/Temperature/IMOS_ANMN-QLD_TZ_20200615T010500Z_GBRCCH_FV01_GBRCCH-2006-SBE39-43_END-20201215T005000Z_C-20210202T032709Z.nc')`
3. The file is now linked to the `nc` variable. To have a look at the variables and attributes just `print(nc)`:

```
print(nc)

<xarray.Dataset>
Dimensions:                (TIME: 54204)
Coordinates:
  * TIME                   (TIME) datetime64[ns] 2020-06-14 ... 2020-12-19T04...
    LATITUDE               float64 ...
    LONGITUDE              float64 ...
    NOMINAL_DEPTH          float32 ...
Data variables:
    TIMESERIES             int32 ...
    TEMP                   (TIME) float32 ...
    TEMP_quality_control   (TIME) float32 ...
    DEPTH                  (TIME) float32 ...
    DEPTH_quality_control  (TIME) float32 ...
Attributes: (12/56)
    abstract:                      The Queensland and Northern Australia moor...
    acknowledgement:               Any users of IMOS data are required to cle...
    author:                        Australian Institute of Marine Science
    author_email:                  adc@aims.gov.au
    cdm_data_type:                 Station
    citation:                      The citation in a list of references is: "...
    ...                            ...
    time_deployment_end_origin:    TimeLastGoodData
    time_deployment_start:         2020-06-15T01:05:00Z
    time_deployment_start_origin:  TimeFirstGoodData
    title:                         CCH mooring deployed 14/06/2020 to 14/12/2...
    toolbox_input_file:            D:\Backup_AIMS_20200623\Trip7484\Data\CCH-...
    toolbox_version:               2.6.10 - PCWIN64
>>> print(nc)
<xarray.Dataset>
Dimensions:                (TIME: 54204)
Coordinates:
  * TIME                   (TIME) datetime64[ns] 2020-06-14 ... 2020-12-19T04...
    LATITUDE               float64 ...
    LONGITUDE              float64 ...
    NOMINAL_DEPTH          float32 ...
Data variables:
    TIMESERIES             int32 ...
    TEMP                   (TIME) float32 ...
    TEMP_quality_control   (TIME) float32 ...
    DEPTH                  (TIME) float32 ...
    DEPTH_quality_control  (TIME) float32 ...
Attributes: (12/56)
    abstract:                      The Queensland and Northern Australia moor...
    acknowledgement:               Any users of IMOS data are required to cle...
    author:                        Australian Institute of Marine Science
    author_email:                  adc@aims.gov.au
    cdm_data_type:                 Station
    citation:                      The citation in a list of references is: "...
    ...                            ...
    time_deployment_end_origin:    TimeLastGoodData
    time_deployment_start:         2020-06-15T01:05:00Z
    time_deployment_start_origin:  TimeFirstGoodData
    title:                         CCH mooring deployed 14/06/2020 to 14/12/2...
    toolbox_input_file:            D:\Backup_AIMS_20200623\Trip7484\Data\CCH-...
    toolbox_version:               2.6.10 - PCWIN64

```

You will see the already familiar structure of the file.

4. to look at the dimensions of this dataset, `nc.dims`. To look at the coordinates, `nc.coords`, nad to see the names of the data variables, `nc.data_vars`
5. To retrieve the global attributes, `nc.attrs` (it is a python dictionary). To read any global attribute, for example `time_coverage_start` type: `nc.time_coverage_start`. Or a variable attribute, like `standard_name`: `nc.TEMP.standard_name`. You probably agree that this is way more friendly than the standard netCDF package.
6. to close the connection with the file, `nc.close()`
7. to quit python, type `quit()` or `ctrl-d`



## Download tools from Ocean Observer repository

The [Ocean Observer repository](https://github.com/diodon/QIMOS) is a set of tools to explore, manipulate and visualise IMOS ANMN files in python and R. It also contains some How-To guides and other tools.

You can navigate the repository and select the tools of your interest. Eventually you will have access to clone the repository and make changes to its content. For the moment, just download the whole repo as a zip file:  

   `wget https://github.com/diodon/QIMOS/archive/refs/heads/main.zip`

and unzip it: 

   `unzip main.zip`

you will end with a *QIMOS-main* directory which is a copy of the full GitHub repository.



## Try somo of the tools

Go to `QIMOS-main/Code/Python` directory. We will run the tool `exploreMooring.py`. This short script will present you with a list of files from one ANMN site (velocity or temperature) and allows you to select one of the files to retrieve a some of its basic attributes. You could also download the full list of names in case you need to use them in your programs. To run the script (remember to have your environment activated!)

   `python3 exploreMooring.py -site TAN100 -param V`

the result will be something similar to: 

```
      Deployment  Instrument                            Depth  Start Date    End Date    Creation Date
--  ------------  ----------------------------------  -------  ------------  ----------  ---------------
 0          1007  Sentinel or Monitor Workhorse ADCP    103    2010-08-02    2010-11-08  2020-07-03
 1          1011  Sentinel or Monitor Workhorse ADCP    104.5  2010-11-11    2011-04-29  2020-07-03
 2          1104  Sentinel or Monitor Workhorse ADCP    104    2011-04-30    2011-11-05  2020-07-03
 3          1111  Sentinel or Monitor Workhorse ADCP    105    2011-11-07    2012-02-23  2020-07-06
 4          1202  Sentinel or Monitor Workhorse ADCP    103.5  2012-02-26    2012-08-23  2021-01-19
 5          1208  Sentinel or Monitor Workhorse ADCP    104    2012-08-25    2013-02-05  2020-07-06
 6          1301  Sentinel or Monitor Workhorse ADCP    103.5  2013-02-08    2013-08-04  2020-07-06
 7          1307  Sentinel or Monitor Workhorse ADCP    103    2013-08-06    2014-02-12  2020-07-07
 8          1402  Sentinel or Monitor Workhorse ADCP    103.3  2014-02-15    2014-08-13  2020-07-07
 9          1408  Sentinel or Monitor Workhorse ADCP    101    2014-08-15    2015-01-12  2020-07-08
10          1501  Sentinel or Monitor Workhorse ADCP    101.5  2015-01-12    2015-07-25  2020-07-09
11          1507  Sentinel or Monitor Workhorse ADCP    101.2  2015-07-25    2016-06-16  2020-07-09
12          1606  Sentinel or Monitor Workhorse ADCP    101    2016-06-16    2017-01-05  2020-07-13
13          1701  Sentinel or Monitor Workhorse ADCP    102    2017-01-05    2017-05-17  2020-07-13
14          1801  Sentinel or Monitor Workhorse ADCP    103.8  2018-01-04    2018-12-13  2021-01-28
15          1812  Sentinel or Monitor Workhorse ADCP    103.8  2018-12-13    2019-08-07  2021-01-19
16          1907  Sentinel or Monitor Workhorse ADCP    104    2019-08-07    2020-02-20  2020-03-30
17          2002  Sentinel or Monitor Workhorse ADCP     69    2020-02-22    2020-10-09  2020-11-10
18          2002  Sentinel or Monitor Workhorse ADCP     70.1  2020-02-22    2020-10-09  2020-11-10
19          2009  Sentinel or Monitor Workhorse ADCP     69    2020-10-09    2021-05-12  2021-07-16
20          2009  Sentinel or Monitor Workhorse ADCP     70.1  2020-10-09    2021-05-12  2021-07-16
Select file number ('s' to save the list or 'e' to exit): 

```

and suppose you select the file number 0:

```
Selected file: IMOS/ANMN/QLD/TAN100/Velocity/IMOS_ANMN-QLD_AETVZ_20100802T044000Z_TAN100_FV01_TAN100-1007-Sentinel-or-Monitor-Workhorse-ADCP-103_END-20101108T091500Z_C-20200703T033315Z.nc
IMOS ANMN Explorer
File: http://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/QLD/TAN100/Velocity/IMOS_ANMN-QLD_AETVZ_20100802T044000Z_TAN100_FV01_TAN100-1007-Sentinel-or-Monitor-Workhorse-ADCP-103_END-20101108T091500Z_C-20200703T033315Z.nc
----------------------------  ------------------------------------------------------------------------------------
Title:                        NW Cape January 2010 - Tantabiddi - Shelf Edge
Site code:                    TAN100
Deployment code:              TAN100-1007
Start Date:                   2010-08-02T04:40:00Z
End Data:                     2010-11-08T09:15:00Z
Instrument:                   RDI ADCP - WORKHORSE SENTINEL-300
Instrument S/N:               12411
Instrument sampling interval  600.0
Instrument Nominal Depth:     103.0
Cell depths Above Sensor:     6.06, 10.06, 14.06, 18.06, 22.06, 26.06, 30.06, 34.06, 38.06, 42.06, 46.06, 50.06,
                              54.06, 58.06, 62.06, 66.06, 70.06, 74.06, 78.06, 82.06, 86.06, 90.06, 94.06, 98.06,
                              102.06, 106.06, 110.06
Data Variables:               TIMESERIES, TEMP, PRES_REL, SSPD, PITCH, ROLL, HEADING, TX_VOLT, DEPTH, VCUR, UCUR,
                              WCUR, CSPD, CDIR, ECUR, ABSIC1, ABSIC2, ABSIC3, ABSIC4, CMAG1, CMAG2, CMAG3,
                              CMAG4, PERG1, PERG2, PERG3, PERG4, ABSI1, ABSI2, ABSI3, ABSI4
----------------------------  ------------------------------------------------------------------------------------

```

The `File: ` in the table is the URL of the file that could be used to establish a connection with in the AODN THREDDS server. You also have details about the instrument and data variables available.

Every script has a small help that explain how to use it. Just type `python3 <script name.py> --help` to have the instructions on how to use it: 

```
python3 exploreMooring.py --help

usage: exploreMooring.py [-h] -site SITE -param PARAM

Explore velocity or temperature AODN individual files

optional arguments:
  -h, --help    show this help message and exit
  -site SITE    site code, like NRMMAI
  -param PARAM  parameter, like V for velocity, T temperature
```

If you find any bug in any of the scripts, or have comment, please open an issue in the GitHub repository. If you have any questions, please [write me](email:e.klein@aims.gov.au) or better, promote the discussion inside the group!

We will continue to develop the Ocean Observer repository, and your contributions will be very much welcome.


Enjoy!


EKS



   






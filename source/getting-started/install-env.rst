Install customized HPC env 
============================

.. note::

   The following assumes that you have access to CSC Finland's computing resources. In case you do not have access to CSC's resources,
   you can still install all the required Python libraries used in the lessons by installing the `environment.yml <https://github.com/AaltoGIS/GeoHPC/blob/master/env/environment.yml>`__
   using mamba/micromamba/miniconda package managers. If you are new to Python's package managers, you can `learn more from here <https://pythongis.org/part1/chapter-01/nb/06-installation.html>`__.


Log in to Puhti
------------------

The first step to start creating your own space for **High Performance Computing (HPC)** 
is to log in in the **CSC Puhti supercomputer**.

.. admonition:: CSC Puhti!

    To log in to the web interface of Puhti supercomputer you need a *CSC account* or *HAKA* credentials.

    .. button-link:: https://www.puhti.csc.fi/public/
            :color: primary
            :shadow:
            :align: center

            👉 Log in to Puhti


Directories overview
----------------------

You will find three different spaces in the Diretory. Each of them can be used in different needs due to its capacity.

- home with **10 GB capacity** for personal files
- projappl with **50 GB capacity** for intermediate processes
- scratch with **1 TB capacity** for big output

We will proceed using projappl to install our personal environment.


Create your personal folder
-----------------------------

Once you are logged in you will see the *User Interface* of Puhti that shows the Apps you can use with HPC (Figure 1). 
We are going to install a containerized Python environment in our **projappl** directory that later on will be connected to **Jupyter Lab**. 

Start opening the **projappl** Directory

.. figure:: img/img1.png
    
    *Figure 1. Puhti - User Interface*

Once you have opened the **projappl Directory**, in the left side, you will see the code of your project like *project_200xxxx* 
in two different Disk section like **projappl** and **scratch**. You should know that the scratch Disk must be used temporary 
because it has a regular clean up (every 180 days) meanwhile the projappl Disk has no clean up. In the projappl Disk 
the capacity is 50GiB and in the scratch Disk the capacity is 1TiB. You can read more about the 
Disk partition in `CSC Disk areas <https://docs.csc.fi/computing/disk/>`_. For the lesson, use **projappl**. 

Start creating a new folder called **GIT-HPC** (Figure 2).

.. figure:: img/img2.png
    
    *Figure 2. Puhti - projappl Directory personal set up*


Clone the repository
----------------------

Once you have your folder ready it is time to clone the repository with the needed material like the coding Notebooks and the **environment.yml** file 
that we will use to creating our environment. Take a look in the menu on top you have the option **>_ Open in Terminal** like in Figure 3.

Open your folder in terminal.

.. figure:: img/img3.png
    
    *Figure 3. Puhti - Home Directory and Open in Terminal button*

Then, you will have a view of the terminal like in Figure 4. It will contain your new folder as a directory and your user log in.

.. figure:: img/img4.png
    
    *Figure 4. Puhti - Terminal*

We will clone the Repository in Puhti using **Git**. Copy and paste in your open terminal the next line (ommit the symbol $):

.. code-block:: bash

    $ git clone https://github.com/AaltoGIS/GeoHPC.git

It should be like in Figure 5.

.. figure:: img/img5.png
    
    *Figure 5. Puhti - Clone the repository using terminal*

You can also explore a bit the repository on GitHub here:

.. button-link:: https://github.com/AaltoGIS/GeoHPC
            :color: primary
            :shadow:
            :align: center

            👉 GeoHPC Repository

Once the Repository is cloned it should be abvailable in your Directory. You can check using the next command:

.. code-block:: bash

    $ ls

If you are willing to know more about Linux commands you can check in the `Linux commands from CSC documention <https://docs.csc.fi/support/tutorials/env-guide/using-linux-in-command-line/>`_.

Finally you can clear the terminal (optionally) using the command:


.. code-block:: bash

    $ clear

Enable *Tykky* module
-------------------------

The Tykky module is a container wrapper that helps to install software in HPC. It can be used to containerize a conda environment 
using an **environment.yml** file. We will activate the Tykky module and install a customized environment that we will use further 
with our notebooks.


Enable *Tykky* module:

.. code-block:: bash

    $ module add tykky

Be sure that you have added *Tykky* using **module list**, it will tell like in Figure 6.
    
.. code-block:: bash

    $ module list

.. figure:: img/img6.png
    
    *Figure 6. Puhti - Modules*


Containerize Python environment
---------------------------------

We will start creating a new folder called **env_container** where we will containerize our Python environment. Simply, 
use the terminal and the next command line:

.. code-block:: bash

    $ mkdir env_container

You will notice that now you have a new folder like in Figure 7.

.. figure:: img/img8.png
    
    *Figure 7. Puhti - A new folder for environment*

Now, we will containerize our environment using *tykky*. We need to specify two paths: 1) the directory 
where you will containerize the environment, and 2) the **environment.yml** file path.

The command we will use has the form *conda-containerize new --prefix {directory} {environment.yml}*

Our folder-directory will be our newly created folder **env_container** and the environment 
file is located in the folder **env** in our cloned repository. It is recommended to create 
the containerized environment outside the git folder *GeoHPC* so it is not compromised in case you need update 
or delete the folder then the environment is not compromised.

.. code-block:: bash

    $ conda-containerize new --mamba --prefix env_container GeoHPC/env/environment.yml


Once the environment is installed you will see the message *Done*. This installation 
process might take approximately 15 minutes. Your terminal might give a message like in Figure 9.

.. figure:: img/img9.png
    
    *Figure 8. Puhti - Environment containerized using tykky*

If everything looks like this so far you have installed successfully a customized Python 
environment in HPC. In the next page you will learn how to use this environment with Jupyter Notebooks and HPC resources. 

Activate your environment (optional)
---------------------------------------

You can use the next command (be sure you replace 200xxxx with your project number) to activate your environment and run scripts:

.. code-block:: bash

    $ export PATH="/projappl/project_200xxxx/GIT-HPC/env_container/bin:$PATH"






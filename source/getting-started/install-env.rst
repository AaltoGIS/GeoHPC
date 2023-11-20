Install customized HPC env 
============================

The first step to start creating your own space for **High Performance Computing (HPC)** 
is to Log in in the **CSC Puhti supercomputer**.

.. admonition:: CSC Puhti!

    To log in to Puhti supercomputer you need a *CSC account* or *HAKA* credentials.

    .. button-link:: https://www.puhti.csc.fi/public/welcome.html
            :color: primary
            :shadow:
            :align: center

            👉 Log in to Puhti

Once you are logged in you will see the *User Interface* of Puhti that contains that Apps that you can connect the HPC resources (Figure 1). 
Then, we are going to install a containerized Python environment in our **Home Directory** that later on will be connected to **Jupyter Lab**. 

Start opening the **Home Directory**

.. figure:: img/img1.png
    
    *Figure 1. Puhti - User Interface*

Once you have opened the **Home Directory**, in the left side, you will see the code of your project like *project_200xxxx* 
in two different Disk section like **projappl** and **scratch**. You should know that the scratch Disk must be used temporary 
because it has a regular clean up (every 180 days) meanwhile the projappl Disk has no clean up. In the projappl Disk 
the capacity is 50GiB and in the scratch Disk the capacity is 1TiB. You can read more about the Disk partition in `CSC Disk areas <https://docs.csc.fi/computing/disk/>`_

For the lesson, feel free to use any of **scratch** or **projappl**. Start creating a new folder called **GIT-HPC** and create 
two empty subfolder **env** and **git** (Figure 2).

.. figure:: img/img2.png
    
    *Figure 2. Puhti - Home Directory personal set up*

Continue...
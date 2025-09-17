.. geohpc documentation master file, created by
   sphinx-quickstart on Thu Nov 16 13:23:50 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. figure:: _static/web-banner.png


The **Spatial Data Science with High Performance Computing (HPC)** website is
designed for students, professionals, and especially personnel of higher-education 
institutions in Finland who are working with `CSC Finland's supercomputers <https://csc.fi/en/>`__ and interested
to use the computational resources in *Parallel* for *Spatial Data Science* processes 
with Python. Although the website has a focus on utilizing CSC Finland's computing resources, the parallelization operations
work similarly on other computing clusters as well. Thus, the lessons can be useful for anyone who has access to some sort of
computing cluster to distribute their computations.

The website is composed of a short **Introduction** to CSC's resources and followed by
a **Getting started** section where you will find briefly how to set up a HPC environment 
for further processes (only applicable for CSC Finland's clients).
Then, short examples of how to use the **HPC storage** in case you
want to use it straightforward. Finally, the website contains various **Lessons** with different
*Spatial Data Processes* using HPC resources in parallel showing how supercomputers can
facilitate your work using specific Python programing tools designed for parallel processing.

The resources on this website are part of `Geoportti Research Infrastructure <https://www.geoportti.fi>`__ which is
a shared service for researchers, teachers, and students using geospatial data and geocomputing tools.
Geoportti RI helps the researchers in Finland to use, to refine, to preserve, and to share their geospatial resources.
Learn more about `Geoportti RI services <http://www.geoportti.fi/services/>`__.

Prerequirements
-----------------
The HPC Lessons requires previous knowledge in spatial algorithms (Spatial Analysis) 
and some programing skills. In a more specific specific way as next:

- Medium/Advanced Python programming skills
- Basic knowledge on Jupyter Lab
- Basic spatial algorithms knowledge
- Basic CSC's set up knowledge especifically for Puhti supercomputer (Optional)

The instructions about how to access and set up Puhti supercomputer are included so in case
you haven't used it before you will be able to.

Course format
----------------
The course start with **Introduction** for theoretical overview of HPC resources and it continues 
with a **Getting started** section that will show you how to access and create an online session
in you browser for using the HPC computational resources for the Lessons. Then, it has a previous 
overview of how to manage Allas **HPC storage** in case you need it for your project.
and then the Lessons starts where you can see an overview on the web.

Running Lessons
------------------

To download all the materials on this website, you can use Git to clone the repository:

.. code-block:: bash

    $ git clone https://github.com/AaltoGIS/GeoHPC.git

Alternatively, you can download the files as a `ZipFile <https://github.com/AaltoGIS/GeoHPC/archive/refs/heads/master.zip>`__.

Once you have cloned and installed the environment specified in the section
:doc:`Installing customized HPC environment <getting-started/install-env>` you will be able to run the Lessons
located under the folder:

.. code-block:: bash

    GeoHPC/source/lessons

Simply open every notebook and follow the instructions cell by cell.


Content
---------
Find a detailed structure of the website here.

.. toctree::
   :maxdepth: 1
   :caption: Presentations

   course-info/introduction
   course-info/overview

.. toctree::
   :maxdepth: 1
   :caption: Webinars

   webinars/geohpc-webinar-2024

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   getting-started/activate-account
   getting-started/load-geoconda
   getting-started/install-env
   .. getting-started/set-up-jupyter
   .. getting-started/desktop-connect

.. toctree::
   :maxdepth: 2
   :caption: HPC storage

   connect-hpc/allas-access

.. toctree::
   :maxdepth: 3
   :caption: Lesson 1

   lessons/L1/01_CellularTowers-Parallelization.ipynb

.. toctree::
   :maxdepth: 3
   :caption: Lesson 2

   lessons/L2/02_ShortestPath-Parallelization.ipynb

.. toctree::
   :maxdepth: 3
   :caption: Lesson 3 - SYKE

   lessons/L3/03_LandCoverClassification_syke_Parallelization.ipynb

.. toctree::
   :maxdepth: 3
   :caption: Lesson 4 - FGI

   lessons/L4/04_MergedTiledVectorData-Parallel.rst

.. toctree::
   :maxdepth: 3
   :caption: Lesson 5 - Overture Maps

   lessons/L5/05_OvertureMaps-POI-Parallelization.ipynb



.. .. toctree::
..    :maxdepth: 2
..    :caption: Long run development test

..    lessons/test/01_ShortestPath-LongRun-16cores.ipynb


Access Allas 
===============

Allas is a storage server part of CSC resources that can be accessed from anywhere with CSC credentials and internet. 
Allas storage is allocated by specific project_200xxxx and it can be active while the project is active.

Data files are stored in Buckets (container) and can be accessed with protocol Swift or S3. If you want to know more about Allas take a look the `Allas documentation <https://docs.csc.fi/data/Allas/introduction/>`_. 

In this Lesson we are going to access our data in Allas with the S3 Protocol. We will first configure Allas and S3 and then we will use it in our notebook. If you want to know more about S3 in Allas find examples in the 
`CSC's S3 connection in Allas (in construction) <https://github.com/CSCfi/csc-user-guide/blob/ktiits-boto3/docs/data/Allas/using_allas/python_boto3.md>`_. 

Start accessing your Terminal in your project_200xxxx directory in Puhti or directly using Jupter Lab. Both options work.

.. admonition:: My CSC!

    To log in to My CSC you need a *CSC account* or *HAKA* credentials.

    .. button-link:: https://my.csc.fi/login
            :color: primary
            :shadow:
            :align: center

            👉 Log in to My CSC


Configure S3 and Allas
==========================

To configure S3 in your project first you have to add Allas module, type the next command.

.. code-block:: bash

    $ module add allas

You can confirm that Allas module is added using `module list`

Then, configure Allas using S3 protocol, using the next command.

.. code-block:: bash

    $ allas-conf --mode s3cmd

Afterwards, it will ask for you **CSC Password** and you will choose the project_200xxxx that you want to add connection. The success message looks like Figure 2.

.. figure:: img/02-allas.png
    
    *Figure 1. Allas - S3 connection success*

Connect to Allas using Python
================================

Read file from Allas
-----------------------

If you want to read data directly from your **Bucket** in Allas here is a sample code

.. code-block:: python

    import pandas as pd
    import boto3

    # create connection s3
    s3_client = boto3.client("s3", endpoint_url='https://a3s.fi')

    # define bucket name and object name
    bucket_name = "MyBucket"
    object_name = "MyFolder/MyFile.csv"

    # read
    df = pd.read_csv(response.get("Body"), sep=";")

    df.head()

Download file from Allas
------------------------------

If you want to download data from your **Bucket** in Allas to your local disk. Here a sample code.

.. code-block:: python

    import pandas as pd
    import boto3    

    # create connection s3
    s3_resource = boto3.resource('s3', endpoint_url='https://a3s.fi')

    # destination path
    destination_path = 'MyLocalDisk/MyLocalFolder/MyNewFile.csv'

    # --------------- Save to local

    # define bucket name and object name
    bucket_name = "MyBucket"
    object_name = "MyFolder/MyFile.csv"

    s3_resource.Object(bucket_name, object_name).download_file(destination_path)

    print(f'File saved in {destination_path}')

Upload file to Allas
-----------------------

If you want to upload files from local disk to your new **Bucket** here is a sample code

.. code-block:: python

    import pandas as pd
    import boto3 

    # create connection s3
    s3_resource = boto3.resource('s3', endpoint_url='https://a3s.fi')

    # --------------- Save to Allas

    # define bucket name and object name
    bucket_name = "MyNewBucket"
    object_name = "MyFolder/MyFile.csv"

    # create a new bucket
    s3_resource.create_bucket(Bucket=bucket_name)

    # source path
    source_path = 'MyLocalDisk/MyLocalFolder/MyLocalFile.csv'

    # send to new project
    s3_resource.Object(bucket_name, object_name).upload_file(source_path)

    # list uploaded files in Bucket
    my_bucket = s3_resource.Bucket(bucket_name)

    for my_bucket_object in my_bucket.objects.all():

        print(my_bucket_object.key)


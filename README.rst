OVERVIEW
========
Django module for synchronize local tables to google fusiontables. The goal of this module is synchronized chosen local tables to google fusion tables in real time. Synchronization response on save, update or delete row. Also there is a way to run synchronization from command line.

**Notic** Currently this module is still not in final version. Make sure everything works fine befor use on production.

REQUIREMENTS
------------
**Notic** This module require access key file to google apps. You must create google app with configured fusiontables app. 

*  Python>=3.4
*  Django>=1.9

Install
-------

You can install it only from git repository.

    git clone https://github.com/kula1922/kfusiontables.git
    cd kfusiontables
    make install 

Add `kfusiontables` to `INSTALLED_APPS`

    INSTALLED_APPS = [
        ...
        'kfusiontables'
    ]

Usage
-----
Add to `settings.py`.

    KFUSIONTABLES_ACCESS_FILE_PATH = <path_to_your_google_app_access_key>.json

Set Inheritance from `KFTModel` for models you want synchronize with google fusiontables.

    from kfusiontables.models import KFTModel
    ...
    class TestModel1(KFTModel):
        field1 = models.CharField(max_length=255)
        ...

**Notic** `KFTModel` inherit directly from `django.db.models.Model`.

Settings
--------
Required:
Set path to google app access key. You can read more [here](https://developers.google.com/api-client-library/php/auth/service-accounts#authorizingrequests).

*  KFUSIONTABLES_ACCESS_FILE_PATH = <path_to_your_google_app_access_key>.json

Optional:

Turn on/off single for update row when save, update od delete
*  KFUSIONTABLES_ROW_SYNC_SIGNALS = True (default True)

Turn on/off single for update table schema when run migrations.
*  KFUSIONTABLES_MIGRATE_SYNC_SIGNALS = True (default True)

Turn on/off single for update rows when run migrations.
*  KFUSIONTABLES_SKIP_ROW_SYNC_ON_MIGRATE = True (default True)

Commandline interface
---------------------
Table name - `<app_label;model_name>`

Separator for multi inputs - `,`

Commands:
*  `kft get_tables` Show local tables and google fusiontables tables.
*  `kft create_tables` Create google fusiontables tables for given models.
*  `kft update_tables` Update google fusiontables tables schema for given models.
*  `kft drop_tables` Delete tables from google fusiontables.
*  `kft get_rows` Show rows from google fusiontables.
*  `kft insert_rows` Insert rows from local tables to google fusiontables tables for given models.
*  `kft update_rows` Update rows from local tables to google fusiontables tables for given models.
*  `kft delete_rows` Delete rows from google fusiontables tables for given models.
*  `kft_sync sync_tables`Not implemented yet. Synchronize local tables to google fusiontables.
*  `kft_sync sync_rows` Not implemented yet. Synchronize local rows to google fusiontables.

Flags:
*  `--all` Run for all tables or rows.
*  `-f, --force` Ignore errors.
*  `--table-id` Run for google fusiontables table id.
*  `--table-ids` Run for google fusiontables table ids.
*  `--table-name` Run for local model. Get model via 'app_label;model_name'.
*  `--table-names` Run for local models. Get models via 'app_label;model_name'.
*  `--row-id` Not implemented yet. Run for local row_id.
*  `--row-ids` Not implemented yet. Run for local row_ids.

Examples
--------

Create KFTModel

    from django.db import models
    from kfusiontables.models import KFTModel
    
    class TestModel1(KFTModel):
        field1 = models.CharField(max_length=255)
        field2 = models.CharField(max_length=255)

    class TestModel1(KFTModel):
        field1 = models.CharField(max_length=255)
        field2 = models.CharField(max_length=255)

Create new google fusiontables tables.

    kft create_tables --table-names='myapp;test_model1', 'myapp;test_model2'
    
Show local and google fusiontables tables.

    kft show_tables --all
    
Update google fusiontables table schema.

    kft update_tables --table-name='myapp;test_model1'
    
Delete google fusiontables table.

    kft delete_tables --table-name='myapp;test_model1'
    
Insert row from local to google fusiontables table.

    kft insert_rows --table-name='myapp;test_model1'
    
Show row from google fusiontables table.

    kft get_rows --table-id=GOOGLEFUSIONTABLEID
    
Update rows from local tables to google fusiontables table.

    kft update_rows --all
    
Delete rows from google fusiontables table.

    kft delete_rows --table-name='myapp;test_model1'

Synchronize all local tables to google fusiontables.

    kft_sync sync_tables --all --force

Synchronize all local tables to google fusiontables.

    kft_sync sync_rows --table-name='myapp;test_model1' --row-ids=1,4,6

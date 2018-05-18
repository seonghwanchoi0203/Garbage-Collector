**WhenToMeet**
https://www.when2meet.com/?6863817-Dy1bm

**Lucichart**
https://www.lucidchart.com/invitations/accept/eff342fb-fe10-4132-87b1-7918baf8c959

# Garbage-Collector
**Tutorials here**
- Github (https://education.github.com/git-cheat-sheet-education.pdf) 
- Git (https://gist.github.com/derhuerst/1b15ff4652a867391f03)
- Brew (https://brew.sh/)
- Django (https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website)
- Postgres   (http://www.postgresql.org)

**Install system packages**

Ubuntu:
```sh
$ sudo apt-get update
$ sudo apt-get install postgresql postgis postgresql-9.3-postgis-2.1 libpq-dev python-dev
```

Mac:
```sh
# install homebrew package manager
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install postgresql postgis python-dev geoip
$ xcode-select --install
```

Links to the above packages and dependencies can be found here:

- postgres   (http://www.postgresql.org/download/linux/)
- libpq-dev  (https://packages.debian.org/sid/libpq-dev)
- python-dev (http://packages.ubuntu.com/precise/python-dev)


**Install Postgis**

```sh
brew install postgis
```

**Database**
```sh
postgres=# CREATE DATABASE test;
postgres=# CREATE USER test WITH PASSWORD 'test';
postgres=# GRANT ALL PRIVILEGES ON DATABASE test to test;
postgres=# \connect test;
test=# CREATE EXTENSION postgis;
test=# CREATE EXTENSION postgis_topology;
test=#\q
```

**Enter the developer python environment**

Make sure your python3.6 is named as python3

```sh
$ cd Garbage-Collector && source develop.sh
```

**Usage**
```sh
$ python3 manage.py runserver
```

Open a brower and type 

```sh
$ http://127.0.0.1:8000/
```


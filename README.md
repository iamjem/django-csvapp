# CSV Starter Project

## Installation

The following instructions walk through running the project using Vagrant.

1. Install [Vagrant](http://www.vagrantup.com/).
2. Install Berkself (`vagrant plugin install vagrant-berkshelf --plugin-version 2.0.1`) and Omnibus (`vagrant plugin install vagrant-omnibus`) plugins for Vagrant.
3. Clone this project to your VM root (`cd ~/VM/csvapp && git clone git@github.com:iamjem/django-csvapp.git .`).
4. Install Berkshelf via Bundler (`gem install bundler` and `bundle install`).
5. Install Vagrant cookbooks with Berkshelf (`berks install`).
6. Start the VM (`vagrant up`) and wait patiently...
7. SSH into your VM (`vagrant ssh`).
8. Create and source a python virtualenv (`mkdir ~/envs && virtualenv ~/envs/csv` and `source ~/envs/csv/bin/activate`).
9. Change directories into the vagrant root and install the requirements with pip (`cd /vagrant && pip install -r requirements.txt`).
10. Sync the database and run migrations (`cd project && python manage.py syncdb` and `python manage.py migrate`). NOTE: You WILL want to create a superadmin because the app requires authentication.
11. Run the SocketIO dev server (`python manage.py socketio_runserver`).
12. Open up your browser on the host machine and navigate to http://localhost:8000/


## Running tests

The test suite covers API endpoints, pubsub, and the Celery tasks. Use the following command to run tests `python manage.py test csvapp --settings=csvproject.settings.unittest`.

## A Note on Celery

Celery is set up to run synchronously for local development to avoid having to run a separate process.
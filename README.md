# CSV Starter Project

## Installation

The following instructions walk through running the project using Vagrant.

1. Install [Vagrant](http://www.vagrantup.com/).
2. Install Berkself (`vagrant plugin install vagrant-berkshelf`) and Omnibus (`vagrant plugin install vagrant-omnibus`) plugins for Vagrant.
3. Install Berkshelf via Bundler (`gem install bundler` and `bundle install`).
4. Install Vagran cookbooks with Berkshelf (`berks install`).
5. Start the VM (`vagrant up`) and wait patiently...
6. SSH into your VM (`vagrant ssh`)
7. Create and source a python virtualenv (`mkdir ~/envs && virtualenv ~/envs/csv` and `source ~/envs/csv/bin/activate`).
8. Change directories to the symlinked Vagrant root and clone this project (`cd /vagrant && git clone git@github.com:iamjem/django-csvapp.git .`).
9. Install the requirements with pip (`pip install -r requirements.txt`).
10. Sync the database and run migrations (`cd project && python manage.py syncdb` and `python manage.py migrate`). NOTE: You WILL want to create a superadmin because the app requires authentication.
11. Run the SocketIO dev server (`python manage.py socketio_runserver`).
12. Open up your browser on the host machine and navigate to http://localhost:8000/


## Running Tests

Use the following command to run tests `python manage.py test csvapp --settings=csvproject.settings.unittest`.
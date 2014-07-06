# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network :forwarded_port, guest:8000, host: 8000
  config.berkshelf.enabled = true
  config.omnibus.chef_version = :latest

  config.vm.provision :chef_solo do |chef|
    chef.add_recipe "apt"
    chef.add_recipe "build-essential"
    chef.add_recipe "openssl"
    chef.add_recipe "postgresql::server"
    chef.add_recipe "redisio::install"
    chef.add_recipe "redisio::enable"
    chef.add_recipe "python"

    chef.json = { 
      postgresql: {
        version: "9.3",
        enable_pgdg_apt: true,
        password: {
          postgres: "password"
        }
      },
      build_essential: {
        compiletime: true
      }
    }
  end

  config.vm.provision :shell do |s|
    $script = <<-eos
      sudo -u postgres createdb development
      sudo apt-get -q -y install git-core python-virtualenv python-dev libevent-dev
    eos

    s.inline = $script
  end

end

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.boot_timeout = 600

  config.vm.provider "virtualbox" do |vb|
    vb.name = "edge-gateway-stack"
    vb.memory = 4096
    vb.cpus = 2
  end

  # SSH
  config.vm.network "forwarded_port",
    guest: 22, host: 2222,
    id: "ssh", auto_correct: true

  # WireGuard (UDP)
  config.vm.network "forwarded_port",
    guest: 51820, host: 51820,
    protocol: "udp"

  config.vm.provision "shell", path: "provision/bootstrap.sh"
end

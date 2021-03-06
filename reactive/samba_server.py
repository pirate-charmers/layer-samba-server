from charmhelpers import fetch
from charmhelpers.core import hookenv
from charms.reactive import set_state, when, when_not
from libsmb import SambaHelper

smb = SambaHelper()


@when_not("samba-server.installed")
def install_samba_server():
    hookenv.status_set("maintenance", "Installing Samba")
    fetch.apt_update()
    fetch.apt_install(["samba"])
    smb.clean_example_config()
    smb.reload_config()
    smb.update_config()
    smb.save_config()
    hookenv.status_set("maintenance", "Samba is installed")
    set_state("samba-server.installed")


@when("config.changed", "samba-server.installed", "layer-service-account.configured")
def update_config():
    hookenv.status_set("maintenance", "Configuring Samba")
    smb.update_config()
    smb.save_config()
    hookenv.log("Config file written", hookenv.INFO)
    hookenv.status_set("active", "Samba is ready")

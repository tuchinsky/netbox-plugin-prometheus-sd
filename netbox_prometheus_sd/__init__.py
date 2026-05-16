from netbox.plugins import PluginConfig

class NetBoxPrometheusSDConfig(PluginConfig):
    name = 'netbox_prometheus_sd'
    verbose_name = 'NetBox Prometheus SD'
    description = 'A Netbox plugin to export targets for Prometheus'
    version = '0.1.0'
    base_url = 'prometheus-sd'

config = NetBoxPrometheusSDConfig

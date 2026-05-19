from netbox.plugins import PluginConfig

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0.0.dev0"

class NetBoxPrometheusSDConfig(PluginConfig):
    name = 'netbox_prometheus_http_sd'
    verbose_name = 'NetBox Prometheus HTTP SD'
    description = 'A Netbox plugin to export targets for Prometheus HTTP service discovery'
    version = __version__
    base_url = 'prometheus-http-sd'

config = NetBoxPrometheusSDConfig

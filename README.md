# netbox-plugin-prometheus-http-sd

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![CI](https://img.shields.io/github/actions/workflow/status/tuchinsky/netbox-plugin-prometheus-http-sd/publish.yml)
[![PyPI](https://img.shields.io/pypi/v/netbox-plugin-prometheus-http-sd)](https://pypi.org/project/netbox-plugin-prometheus-http-sd/)

## Demo

```bash
docker-compose up -d

docker exec netbox-plugin-prometheus-http-sd-netbox-1 /opt/netbox/netbox/manage.py load_initializer_data --path /etc/netbox/initializer-data
```

Login into Netbox (http://localhost:8080) and create **Config Context** named `prometheus_role_map` with the following JSON structure:
```json
{
    "prometheus_exporters": {
        "default": [
            {
                "job": "node-exporter",
                "port": 9100
            }
        ],
        "etcd": [
            {
                "job": "node-exporter",
                "port": 9100
            },
            {
                "job": "etcd-exporter",
                "port": 2379
            }
        ],
        "postgresql": [
            {
                "job": "node-exporter",
                "port": 9100
            },
            {
                "job": "postgresql-exporter",
                "port": 9187
            }
        ],
        "vault": [
            {
                "job": "vault-exporter",
                "scheme": "https",
                "metrics_path": "/v1/sys/metrics",
                "params": {
                    "format": [
                        "prometheus"
                    ]
                },
                "port": 8200
            }
        ]
    }
}
```
Each role can have multiple jobs (one target per job is generated)

If role is not found, the `default` entry is used

## Usage

The plugin exposes a single API endpoint (no web UI):
```
GET /api/plugins/prometheus-http-sd/targets/
```

Device or Virtual Machine is included only if all of the following are true:
1. It has status `active`
2. The custom field `role` is present and non‑empty

## Metrics labels

Labels:
* `job` – Prometheus job name defined in the mapping
* `__meta_netbox_name` – object name
* `__meta_netbox_type` – `device` or `vm`
* `__meta_netbox_cf_<custom_field>` – every custom field prefixed with `__meta_netbox_cf_`

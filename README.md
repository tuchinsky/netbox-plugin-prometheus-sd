# netbox-plugin-prometheus-sd

## Demo

```bash
docker-compose up -d

docker exec netbox-plugin-prometheus-sd-netbox-1 /opt/netbox/netbox/manage.py load_initializer_data --path /etc/netbox/initializer-data
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
                "port": 8200
            }
        ],
        "postgresql": [
            {
                "job": "node-exporter",
                "port": 9100
            },
            {
                "job": "postgresql-exporter",
                "port": 8200
            }
        ],
        "kafka": [
            {
                "job": "node-exporter",
                "port": 9100
            },
            {
                "job": "kafka-exporter",
                "port": 8200
            },
            {
                "job": "kafka-jmx-exporter",
                "port": 8201
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
GET /api/plugins/prometheus-sd/targets/
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

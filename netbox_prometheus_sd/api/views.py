from rest_framework.views import APIView
from rest_framework.response import Response
from dcim.models import Device
from virtualization.models import VirtualMachine
from extras.models import ConfigContext

# 'ip' or 'dns'
TARGET_SOURCE = 'ip'

class PrometheusTargetsView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        mapping = self._get_prometheus_mapping()
        targets = []

        for device in Device.objects.filter(status='active'):
            if not device.custom_field_data or 'role' not in device.custom_field_data:
                continue

            ip = device.primary_ip4 or device.primary_ip6
            if TARGET_SOURCE == 'ip' and not ip:
                continue

            self._add_targets(
                targets, ip, device.name, 'device', mapping,
                device.custom_field_data
            )

        for vm in VirtualMachine.objects.filter(status='active'):
            if not vm.custom_field_data or 'role' not in vm.custom_field_data:
                continue

            ip = vm.primary_ip4 or vm.primary_ip6
            if TARGET_SOURCE == 'ip' and not ip:
                continue

            self._add_targets(
                targets, ip, vm.name, 'vm', mapping,
                vm.custom_field_data
            )

        return Response(targets)

    def _get_prometheus_mapping(self):
        context = ConfigContext.objects.filter(name='prometheus_role_map').first()
        if context and context.data:
            return context.data.get('prometheus_exporters', {})
        return {
            'default': [{'job': 'node-exporter', 'port': 9100}]
        }

    def _add_targets(self, targets, ip, name, obj_type, mapping, cf_data):
        role = cf_data['role']
        exporters = mapping.get(role, mapping.get('default', []))

        for exporter in exporters:
            job = exporter['job']
            port = exporter['port']

            if TARGET_SOURCE == 'dns':
                address = name
            elif TARGET_SOURCE == 'ip':
                address = str(ip.address.ip)
            else:
                raise ValueError(
                    f"Incorrect value TARGET_SOURCE: '{TARGET_SOURCE}'. "
                    "Acceptable values: 'ip', 'dns'."
                )

            # default labels
            labels = {
                "job": job,
                "__meta_netbox_name": name,
                "__meta_netbox_type": obj_type,
            }

            # add all custom fields as labels with prefix '__meta_netbox_cf_'
            for cf_key, cf_value in cf_data.items():
                labels[f"__meta_netbox_cf_{cf_key}"] = str(cf_value)

            targets.append({
                "targets": [f"{address}:{port}"],
                "labels": labels
            })

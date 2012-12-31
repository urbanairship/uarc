from collections import defaultdict, namedtuple
import ConfigParser
import os
import warnings


# Filenames should go from least to most specific
DEFAULT_FILENAMES = [
    '/etc/ua/uarc',
    # Cross-platform home directory resolution
    os.path.join(os.path.expanduser('~'), '.uarc'),
    os.path.join(os.path.abspath(os.curdir), '.uarc'),
]

# Append value of UARC envvar if it exists
if os.getenv('UARC'):
    DEFAULT_FILENAMES.append(os.getenv('UARC'))


class UarcException(Exception):
    """Base class for all uarc related exceptions"""


class AppAliasNotFound(UarcException):
    """App alias does not exist in uarc"""
    def __init__(self, alias):
        super(AppAliasNotFound, self).__init__('Alias %r not found' % alias)


Device = namedtuple('Device', ('alias', 'family', 'id'))


class App(object):
    _device_families = set(('apid', 'pin', 'token'))

    def __init__(self, name, data):
        d = dict(data)
        self.name = name
        self.key = d.get('key')
        self.secret = d.get('secret')
        self.master = d.get('master')

        # Mapping of aliases to Device objects
        self._aliases = {}

        # Mapping of device families to id
        self._devices = defaultdict(dict)

        self._load_device_aliases(data)

    def _load_device_aliases(self, data):
        """Given an iter of tuples, parse platform specific device aliases

        apid.* => apids, pin.* => device pins, token.* => device_tokens
        """
        for k, v in data:
            if not k.startswith('device.'):
                # Not a device alias entry, skip
                continue

            _, alias = k.split('.', 1)

            if ':' not in v:
                self.warn(self.name, k, v, "Missing '<device_family>:'")
                continue

            device_family, device_id = v.split(':', 1)

            if device_family not in self._device_families:
                self.warn(
                    self.name, k, v,
                    '%r is an invalid device family. Must be one of %s' % (
                        device_family, ', '.join(self._device_families)
                    )
                )
                continue

            self._add_device_alias(alias, device_family, device_id)

    def _add_device_alias(self, alias, family, id_):
        # Register lists of device ids by family and map to aliases
        self._devices[family][id_] = alias
        # Register alias to type, id tuple
        self._aliases[alias] = Device(alias=alias, family=family, id=id_)

    def warn(self, app, key, value, msg):
        """Raises a UserWarning about uarc errors"""
        warnings.warn(
            "Error in [{app}] in key {key} with value {key}:\n{msg}".format(
                app=app, key=key, value=value, msg=msg)
        )

    def get_device(self, alias):
        """Returns a Device object this alias or None"""
        return self._aliases.get(alias)

    @property
    def apids(self):
        """Returns a mapping of APIDs to aliases"""
        return self._devices['apid']

    @property
    def device_pins(self):
        """Returns a mapping of device PINs to aliases"""
        return self._devices['pin']

    @property
    def device_tokens(self):
        """Returns a mapping of device tokens to aliases"""
        return self._devices['token']


class Uarc(object):
    def __init__(self, filenames=DEFAULT_FILENAMES):
        self._config = ConfigParser.SafeConfigParser()
        self.files = self._config.read(filenames)

    def get_app(self, name):
        """Returns an app instance for the given name.

        Raises AppAliasNotFound exception if alias does not exist
        """
        if name not in self._config.sections():
            raise AppAliasNotFound(name)
        return App(name, self._config.items(name))

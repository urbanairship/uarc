from collections import defaultdict
import ConfigParser
import os


# Filenames should go from least to most specific
DEFAULT_FILENAMES = [
    '/etc/ua/uarc',
    os.path.expanduser('~'),  # Cross-platform home directory resolution
    os.path.abspath(os.curdir),
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


class App(object):
    _device_families = set(('apid', 'pin', 'token'))

    def __init__(self, name, data):
        d = dict(data)
        self.name = name
        self.key = d.get('key')
        self.secret = d.get('secret')
        self.master = d.get('master')
        self.devices = defaultdict(dict)

        self._load_device_aliases(data)

    def _load_device_aliases(self, data):
        """Given an iter of tuples, parse platform specific device aliases

        apid.* => apids, pin.* => device pins, token.* => device_tokens
        """
        for k, v in data:
            parts = k.split('.', 1)
            if len(parts) == 1:
                # No "."s, move on
                continue
            prefix, rest = parts

            if prefix in self._device_families:
                self.devices[prefix][rest] = v

    @property
    def apids(self):
        """Returns a mapping of aliases to APIDs"""
        return self.devices['apid']

    @property
    def device_pins(self):
        """Returns a mapping of aliases to device PINs"""
        return self.devices['pin']

    @property
    def device_tokens(self):
        """Returns a mapping of aliases to device tokens"""
        return self.devices['token']


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

import pkg_resources

from magiclog import log


def main():
    log.configure()
    data = pkg_resources.resource_stream(__package__, '__init__.py')
    log.info('Writing local copy of v2 to v2.py...')
    with open('v2.py', 'wb') as h:
        h.write(data.read())
    log.info('Appending v2.py and VERSION to MANIFEST.in...')
    data = pkg_resources.resource_stream(__package__, 'MANIFEST.in')
    with open('MANIFEST.in', 'ab') as h:
        h.write(data.read())


if __name__ == '__main__':
    main()

from aspen.testing.client import Client, FileUpload

import json
import pytest


import gdr


@pytest.fixture
def client():
    return Client('www', '.')


def test_resolve_resolves():
    deps = gdr.resolve('requirements.txt', 'Flask==0.11.1')
    assert len(deps) == 6         # vvv assumes case-insensitive ordering
    assert deps[1] == dict(name='Flask', version='0.11.1', license='BSD')


def test_v1_can_be_hit(client):
    file_upload = FileUpload(filename='requirements.txt', data='Flask==0.11.1')
    out = json.loads(client.POST('/v1', data={'file': file_upload}).body)
    assert len(out) == 1
    assert len(out[0]['deps']) == 6
    assert out[0]['deps'][1] == dict(name='Flask', version='0.11.1', license='BSD')


def test_v1_accepts_multiple_files(client):
    one = FileUpload(filename='requirements.txt', data='Flask==0.11.1')
    two = FileUpload(filename='requirements.txt', data='itsdangerous==0.24')

    class Kludge:
        def items(self):
            for f in (one, two):
                yield 'file', f

    out = json.loads(client.POST('/v1', data=Kludge()).body)
    assert len(out) == 2
    assert len(out[0]['deps']) == 6
    assert out[0]['deps'][1] == dict(name='Flask', version='0.11.1', license='BSD')
    assert len(out[1]['deps']) == 1
    assert out[1]['deps'][0] == dict(name='itsdangerous', version='0.24', license='UNKNOWN')

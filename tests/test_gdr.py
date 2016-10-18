from aspen.testing.client import Client, FileUpload

import json
import pytest


import gdr


RTD = """\
# Base packages
pip==8.1.1
virtualenv==15.0.1
docutils==0.11
Sphinx==1.3.5
Pygments==2.0.2
mkdocs==0.14.0
git+https://github.com/rtfd/readthedocs-build.git@db4ad19df4f432bfbbd56d05964c58b6634356f3#egg=readthedocs-build-2.0.6.dev
django==1.8.3

django-tastypie==0.12.2
django-haystack==2.5.0
celery-haystack==0.7.2
django-guardian==1.3.0
django-extensions==1.3.8
djangorestframework==3.0.4
django-vanilla-views==1.0.4
pytest-django==2.8.0

requests==2.3.0
slumber==0.6.0
lxml==3.3.5

django-countries==3.4.1

# Basic tools
redis==2.10.3
celery==3.1.23
django-celery==3.1.16
git+https://github.com/pennersr/django-allauth.git@d869aff9#egg=django-allauth
dnspython==1.11.0

# VCS
httplib2==0.7.7

# Search
elasticsearch==1.5.0
pyelasticsearch==0.7.1
pyquery==1.2.2

# Utils
django-gravatar2==1.0.6
doc2dash==1.1.0
pytz==2013b
beautifulsoup4==4.1.3
Unipath==0.2.1
django-kombu==0.9.4
django-secure==0.1.2
mimeparse==0.1.3
mock==1.0.1
stripe==1.20.2
django-copyright==1.0.0
django-formtools==1.0
django-dynamic-fixture==1.8.5
docker-py==1.3.1
django-textclassifier==1.0
django-annoying==0.8.4
django-messages-extends==0.5

# Docs
sphinxcontrib-httpdomain==1.4.0
commonmark==0.5.5
recommonmark==0.1.1

# Version comparison stuff
Distutils2==1.0a3
packaging==15.2

# Commenting stuff
git+https://github.com/zestedesavoir/django-cors-middleware.git@def9dc2f5e81eed53831bcda79ad1c127ecb3fe2
nilsimsa==0.3.7

# Pegged git requirements
git+https://github.com/alex/django-filter.git#egg=django-filter
git+https://github.com/ericflo/django-pagination.git@e5f669036c#egg=django_pagination-dev
git+https://github.com/alex/django-taggit.git#egg=django_taggit-dev
"""


@pytest.fixture
def client():
    return Client('www', '.')


def test_resolve_resolves():
    deps = gdr.resolve('requirements.txt', 'Flask==0.11.1')
    assert len(deps) == 6         # vvv assumes case-insensitive ordering
    assert deps[1] == dict(name='Flask', version='0.11.1', license='BSD')

def test_resolve_choketh_not_on_unicode():
    deps = gdr.resolve('requirements.txt', 'requests==2.11.1')
    assert deps[0] == dict(name='requests', version='2.11.1', license='Apache')

def test_resolve_choketh_on_errors():
    with pytest.raises(gdr.ResolutionError) as e:
        gdr.resolve('requirements.txt', 'this is a bad requirements.txt')
    assert e.value.args[0].startswith('Traceback')

def test_resolve_choketh_not_on_rtd():
    deps = gdr.resolve('requirements.txt', RTD)
    assert len(deps) == 90
    assert deps[14] == dict(name='Django', version='1.8.3', license='BSD')


def test_v1_can_be_hit(client):
    file_upload = FileUpload(filename='requirements.txt', data='Flask==0.11.1')
    deps = json.loads(client.POST('/v1', data={'file': file_upload}).body)
    assert len(deps) == 1
    assert len(deps[0]['deps']) == 6
    assert deps[0]['deps'][1] == dict(name='Flask', version='0.11.1', license='BSD')

def test_v1_can_hit_back(client):
    file_upload = FileUpload(filename='requirements.txt', data='Flasky garbage')
    deps = json.loads(client.POST('/v1', data={'file': file_upload}).body)
    assert len(deps) == 1
    assert deps[0]['error'].startswith('Traceback')

def test_v1_accepts_multiple_files(client):
    one = FileUpload(filename='requirements.txt', data='Flask==0.11.1')
    two = FileUpload(filename='requirements.txt', data='itsdangerous==0.24')

    class Kludge:
        def items(self):
            for f in (one, two):
                yield 'file', f

    deps = json.loads(client.POST('/v1', data=Kludge()).body)
    assert len(deps) == 2
    assert len(deps[0]['deps']) == 6
    assert deps[0]['deps'][1] == dict(name='Flask', version='0.11.1', license='BSD')
    assert len(deps[1]['deps']) == 1
    assert deps[1]['deps'][0] == dict(name='itsdangerous', version='0.24', license='UNKNOWN')

def test_v1_can_handle_rtd(client):
    file_upload = FileUpload(filename='requirements.txt', data=RTD)
    deps = json.loads(client.POST('/v1', data={'file': file_upload}).body)
    assert len(deps[0]['deps']) == 90
    assert deps[0]['deps'][14] == dict(name='Django', version='1.8.3', license='BSD')

from __future__ import absolute_import, division, print_function, unicode_literals

import os
from aspen.website import Website

project_root = os.path.dirname(__file__)
www_root = os.path.join(project_root, 'www')
website = Website(project_root=project_root, www_root=www_root)

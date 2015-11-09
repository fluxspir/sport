#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import models

try:
    models.init()
    meta.Base.metadata.create_all(bind=meta.session.bind.engine)
    sys.exit(0)

except KeyboardInterrupt:
    sys.exit(1)

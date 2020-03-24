# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Ffr(MakefilePackage):
    """FFR: FrontFlow/red, developed in Frontier Simulation Software
    for Industrial Science(FSIS) project supported by IT program of
    Ministry of Education, Culture, Sports, Science and Technology(MEXT),
    JAPAN."""

    homepage = "http://www.ciss.iis.u-tokyo.ac.jp/rss21/theme/multi/fluid/fluid_softwareinfo.html"
    url      = "file://{0}/OPEN_FFR.zip".format(os.getcwd())

    version('3.1.004', 'ed45fc49b7dacf9fa47bc91943b3ec61')

    depends_on('mpi', type=('build', 'run'))

    parallel = False

    patch('FFR_V3.1.004-gfortran.patch',
          when='@3.1.004%gcc', level=0)
    patch('FFR_V3.1.004-makefile-gnu.patch',
          when='@3.1.004%gcc', level=0)
    patch('FFR_V3.1.004-makefile-intel.patch',
          when='@3.1.004%intel', level=0)

    def setup_environment(self, build_env, run_env):
        build_env.set('PREFIX', self.prefix)

    def install(self, spec, prefix):
        make('install')

        mkdirp(prefix.share.docs)
        install(os.path.join('OPEN_FFR', 'Procedure_Linux_6_30.pdf'),
                prefix.share.docs)

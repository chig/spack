# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Eigenexa(AutotoolsPackage):
    """EigenEXA, a part of KMATHLIB, is a high performance eigen-solver.
    """

    homepage = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/eigenexa/"
    url      = "https://www.r-ccs.riken.jp/labs/lpnctrt/assets/img/EigenExa-2.4b.tgz"

    version('2.6_20190903', url='file://{0}/EigenExa-2.6_20190903.tar.gz'.format(os.getcwd()),
             sha256='a72a2c8c5e5432378efcd0639d1dbbf4bd2bb2fcc142e3091e0660503bf2a398')
    version('2.4b', sha256='7c0fa47594af3f86a2ab583f2aaddcf6867212458b079a3436a819f05c39939c')

    variant('avx', default=False, description='Enable AVX features.')
    variant('avx2', default=False, description='Enable AVX2 features.')
    variant('mic-avx512', default=False, description='Enable MIC-AVX512 features.')
    variant('skylake-avx512', default=False, description='Enable SKYLAKE-AVX512 features.')

    depends_on('mpi', type=('build', 'run'))
    depends_on('scalapack')

    # In EigenExa, the combination of netlib-scalapack and openblas may give
    # incorrect calculation results.
    cmsg = '\nThe combination of netlib-scalapack and openblas can cause ' \
           + 'incorrect calculation results of eigenexa.\n' \
           + 'You can use netlib-lapack instead of openblas by specifying ' \
           + '"^netlib-lapack".'
    conflicts('^netlib-scalapack ^openblas', msg=cmsg)

    parallel = False

    def configure_args(self):
        spec = self.spec
        lapack_blas = spec['scalapack'].libs \
            + spec['lapack'].libs + spec['blas'].libs
        options = [
            'CC={0}'.format(spec['mpi'].mpicc),
            'F77={0}'.format(spec['mpi'].mpifc),
            'FC={0}'.format(spec['mpi'].mpifc),
            'LAPACK_LIBS={0}'.format(lapack_blas.ld_flags)]
        if '+avx' in spec:
            options.append('--enable-avx')
        elif '+avx2' in spec:
            options.append('--enable-avx2')
        elif '+mic-avx512' in spec:
            options.append('--enable-mic-avx512')
        elif '+skylake-avx512' in spec:
            options.append('--enable-skylake-avx512')
        return options

    def configure(self, spec, prefix):
        configure('--prefix={0}'.format(prefix), *self.configure_args())

    def install(self, spec, prefix):
        make('install')

        mkdirp(prefix.bin)
        install(os.path.join('benchmark', 'eigenexa_benchmark'), prefix.bin)
        install(os.path.join('benchmark', 'IN'), prefix.bin)

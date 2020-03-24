# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Genesis(AutotoolsPackage):
    """GENESIS is a Molecular dynamics and modeling software
    for bimolecular systems such as proteins, lipids, glycans,
    and their complexes.
    """

    homepage = "https://www.r-ccs.riken.jp/labs/cbrt/"
    url      = "https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2019/10/genesis-1.4.0.tar.bz2"

    version('1.4.0', '132d53e7edbd593d67ec53cd4618748a')

    resource(when='@1.4.0',
             name='user_guide',
             url='https://www.r-ccs.riken.jp/labs/cbrt/wp-content/uploads/2019/10/GENESIS-1.4.0.pdf',
             sha256='da2c3f8bfa1e93adb992d3cfce09fb45d8d447a94f9a4f884ac834ea7279b9c7',
             expand=False,
             placement='doc')

    variant('openmp', default=True, description='Enable OpenMP.')
    variant('gpu', default=False, description='Enable GPU.')
    variant('single', default=False, description='Enable single precision.')
    variant('hmdisk', default=False, description='Enable huge molecule on hard disk.')

    conflicts('%clang', when='+openmp')
    conflicts('~openmp', when='@:1.4.0')

    depends_on('mpi', type=('build', 'run'))
    depends_on('cuda', when='+gpu')
    depends_on('lapack')

    parallel = False

    def configure_args(self):
        spec = self.spec
        options = []
        if '~openmp' in spec:
            options.append('--disable-openmp')
        if '+single' in spec:
            options.append('--enable-single')
        if '+hmdisk' in spec:
            options.append('--enable-hmdisk')
        if '+gpu' in spec:
            options.append('--enable-gpu')
            options.append('--with-cuda=%s' % spec['cuda'].prefix)
        return options

    def configure(self, spec, prefix):
        # need to unset environment variables of compiler
        env['F77'] = ''
        env['FC'] = ''
        env['CXX'] = ''
        env['CC'] = ''
        if '^openblas' in spec:
            env['LAPACK_LIBS'] = "`pkg-config --libs openblas`"
        configure('--prefix={0}'.format(prefix), *self.configure_args())

    def install(self, spec, prefix):
        make('install')
        install_tree('doc', prefix.share.doc)

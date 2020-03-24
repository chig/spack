# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import subprocess


class Scale(MakefilePackage):
    """SCALE (Scalable Computing for Advanced Library and Environment) is
    a basic library for weather and climate model of the earth and planets
    aimed to be widely used in various models.
    The SCALE library is developed with co-design by researchers of
    computational science and computer science."""
    homepage = "http://r-ccs-climate.riken.jp/scale/"
    url      = "http://r-ccs-climate.riken.jp/scale/download/archives/scale-5.3.4.tar.gz"

    version('5.3.4', '43128e8db74ff6cb715b79c0951007da')
    version('5.2.6', '8049ae8bb96127236fefd91547d4cd6e')

    depends_on('mpi', type=('build', 'link', 'run'))
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')

    patch('add_makefile_top.patch', level=0)
    patch('gnu-ompi-aarch64.patch', level=0, when='%gcc target=aarch64:')
    patch('fx100-own_compiler.patch', level=0, when='%fj target=s64fx:')

    parallel = False

    def setup_environment(self, build_env, run_env):
        build_env.set('PREFIX', self.prefix)

    def build(self, spec, prefix):
        scale_sys_str = ''
        if os.uname()[0] == 'Linux':
            if os.uname()[-1] == 'x86_64':
                if self.compiler.PrgEnv_compiler == 'gcc':
                    if 'openmpi' in spec:
                        scale_sys_str = 'Linux64-gnu-ompi'
                elif self.compiler.PrgEnv_compiler == 'intel':
                    if 'mpich' in spec:
                        scale_sys_str = 'Linux64-intel-mpich2'
                    elif 'intel-mpi' in spec:
                        scale_sys_str = 'Linux64-intel-impi'
                elif self.compiler.PrgEnv_compiler == 'pgi':
                    if 'openmpi' in spec:
                        scale_sys_str = 'Linux64-pgi-ompi'
            elif os.uname()[-1] == 'aarch64':
                if self.compiler.PrgEnv_compiler == 'gcc':
                    if 'openmpi' in spec:
                        scale_sys_str = 'Linux64-gnu-ompi'
            elif os.uname()[-1] == 's64fx':
                if self.compiler.PrgEnv_compiler == 'fj':
                    scale_sys_str = 'FX100'
        elif os.uname()[0] == 'Darwin':
            if os.uname()[-1] == 'x86_64':
                if 'openmpi' in spec:
                    scale_sys_str = 'MacOSX-gnu-ompi'
        if scale_sys_str == '':
            raise InstallError('unsupported arch and compiler combination.')
        env['SCALE_SYS'] = scale_sys_str

        # set SCALE_NETCDF_INCLUDE
        nc_str = subprocess.Popen(('nc-config', '--cflags', '--fflags'),
                                  stdout=subprocess.PIPE).communicate()[0]
        try:
            env['SCALE_NETCDF_INCLUDE'] = nc_str.replace('\n', ' ')
        except TypeError:  # for python3
            env['SCALE_NETCDF_INCLUDE'] = nc_str.decode().replace('\n', ' ')

        # set SCALE_NETCDF_LIBS
        nc_str = subprocess.Popen(('nc-config', '--libs', '--flibs'),
                                  stdout=subprocess.PIPE).communicate()[0]
        try:
            env['SCALE_NETCDF_LIBS'] = nc_str.replace('\n', ' ')
        except TypeError:  # for python3
            env['SCALE_NETCDF_LIBS'] = nc_str.decode().replace('\n', ' ')

        make()

    def install(self, spec, prefix):
        make('install')

        install_tree('doc', prefix.share.docs)
        install_tree(os.path.join('scale-rm', 'test'),
                     os.path.join(prefix.share, 'test'))

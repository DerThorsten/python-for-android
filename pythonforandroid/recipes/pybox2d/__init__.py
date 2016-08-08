from pythonforandroid.logger import shprint
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory
import sh
from os.path import join

from pythonforandroid.toolchain import (
    NDKRecipe,
    Recipe,
    current_directory,
    info,
    shprint,
)
from multiprocessing import cpu_count

class Pybox2dRecipe(NDKRecipe):
    name = 'pybox2d'
    version = 'master'
    #url = 'https://github.com/DerThorsten/liquidfun/archive/{version}.zip'
    url = 'https://github.com/DerThorsten/liquidfun/archive/{version}.zip'

    # version = '5.5.47'
    # url = 'http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-{version}.tar.gz'
    # 
    depends = ['python2']
    # 

    # patches = ['add-custom-platform.patch']

    #patches = ['disable-soversion.patch']

    def should_build(self, arch):
        return True#not self.has_libs(arch, 'libmysql.so')

    def get_recipe_env(self,arch):
        env = super(Pybox2dRecipe, self).get_recipe_env(arch)
        env['PYTHON_ROOT'] = self.ctx.get_python_install_dir()
        env['ANDROID_NDK'] = self.ctx.ndk_dir
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        env['SITEPACKAGES_PATH'] = self.ctx.get_site_packages_dir()
        
    def build_arch(self, arch):
        
        print "PYDIR",self.ctx.get_python_install_dir()


        env = super(Pybox2dRecipe, self).get_recipe_env(arch)
        #env = self.get_recipe_env(arch)
        cvsrc = self.get_build_dir(arch.arch)
        instDir = self.ctx.get_python_install_dir()

        keys = dict(
            ctx=self.ctx,
            arch=arch,
            arch_noeabi=arch.arch.replace('eabi', ''),
            pyroot=self.ctx.get_python_install_dir()
        )


        env['LDSHARED'] = env['CC'] + ' -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions'
        env['CFLAGS'] += " -I{pyroot}/include/python2.7 " \
                        " -I{ctx.ndk_dir}/platforms/android-{ctx.android_api}/arch-{arch_noeabi}/usr/include" \
                        " -I{ctx.ndk_dir}/sources/cxx-stl/gnu-libstdc++/{ctx.toolchain_version}/include" \
                        " -I{ctx.ndk_dir}/sources/cxx-stl/gnu-libstdc++/{ctx.toolchain_version}/libs/{arch.arch}/include".format(**keys)
        env['CXXFLAGS'] = env['CFLAGS'] + ' -fexceptions -frtti'
        env['LDFLAGS'] += " -L{ctx.ndk_dir}/sources/cxx-stl/gnu-libstdc++/{ctx.toolchain_version}/libs/{arch.arch}" \
                " -lpython2.7" \
                " -lgnustl_shared".format(**keys)
                


        with current_directory(join(self.get_build_dir(arch.arch), 'liquidfun/Box2D')):

            sh.cp(
                "{ctx.ndk_dir}/sources/cxx-stl/gnu-libstdc++/{ctx.toolchain_version}/libs/{arch.arch}/libgnustl_shared.so".format(ctx=self.ctx,arch=arch),
                self.ctx.get_libs_dir(arch.arch)
            )
        

            #shprint(sh.cp, '-t', '.', join(self.get_recipe_dir(), 'p4a.cmake'))
            # shprint(sh.mkdir, 'Platform')
            # shprint(sh.cp, '-t', 'Platform', join(self.get_recipe_dir(), 'Linux.cmake'))
            shprint(sh.rm, '-f', 'CMakeCache.txt')
            shprint(sh.cmake, '-G', 'Unix Makefiles',
                    # '-DCMAKE_MODULE_PATH=' + join(self.get_build_dir(arch.arch), 'libmysqlclient'),
                    '-DP4A=ON','-DANDROID_ABI={}'.format(arch.arch),
                    #'-DCMAKE_TOOLCHAIN_FILE={}/platforms/android/android.toolchain.cmake'.format(cvsrc),
                    '-DBOX2D_BUILD_STATIC=0',
                    '-DBOX2D_BUILD_EXAMPLES=0',
                    '-DBOX2D_BUILD_UNITTESTS=0',
                    '-DBOX2D_CODE_COVERAGE=0',
                    '-DCMAKE_INSTALL_PREFIX=./install',
                    '-DPYTHON_INCLUDE_PATH={}/include/python2.7'.format(instDir),
                    '-DPYTHON_LIBRARY={}/lib/libpython2.7.so'.format(instDir),
                    #'-DCMAKE_TOOLCHAIN_FILE=p4a.cmake', 
                    _env=env)
            shprint(sh.make, _env=env)

            #self.install_libs(arch, join('libmysql', 'libmysql.so'))

    # def get_recipe_env(self, arch=None):
    #   env = super(Pybox2dRecipe, self).get_recipe_env(arch)
    #   env['WITHOUT_SERVER'] = 'ON'
    #   ncurses = self.get_recipe('ncurses', self)
    #   # env['CFLAGS'] += ' -I' + join(ncurses.get_build_dir(arch.arch),
    #   #                               'include')
    #   env['CURSES_LIBRARY'] = join(self.ctx.get_libs_dir(arch.arch), 'libncurses.so')
    #   env['CURSES_INCLUDE_PATH'] = join(ncurses.get_build_dir(arch.arch),
    #                                     'include')
    #   return env
    # 
    # def build_arch(self, arch):
    #   env = self.get_recipe_env(arch)
    #   with current_directory(self.get_build_dir(arch.arch)):
    #       # configure = sh.Command('./configure')
    #       # TODO: should add openssl as an optional dep and compile support
    #       # shprint(configure, '--enable-shared', '--enable-assembler',
    #       #         '--enable-thread-safe-client', '--with-innodb',
    #       #         '--without-server', _env=env)
    #       # shprint(sh.make, _env=env)
    #       shprint(sh.cmake, '.', '-DCURSES_LIBRARY=' + env['CURSES_LIBRARY'],
    #               '-DCURSES_INCLUDE_PATH=' + env['CURSES_INCLUDE_PATH'], _env=env)
    #       shprint(sh.make, _env=env)
    # 
    #       self.install_libs(arch, 'libmysqlclient.so')


recipe = Pybox2dRecipe()

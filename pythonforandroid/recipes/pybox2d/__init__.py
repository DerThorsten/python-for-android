import sh
from os.path import join
from pythonforandroid.toolchain import (
    Recipe,
    current_directory,
    info,
    shprint,
)
from  pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
from multiprocessing import cpu_count

class Pybox2dRecipe(CppCompiledComponentsPythonRecipe):

    name = 'pybox2d'
    version = 'v44'
    url = 'https://github.com/DerThorsten/liquidfun/archive/{version}.zip'
    depends = ['python2']


    def should_build(self, arch):
        return True#not self.has_libs(arch, 'libmysql.so')

    
    def build_arch(self, arch):
        
        env = super(Pybox2dRecipe, self).get_recipe_env(arch)

        super(Pybox2dRecipe, self).get_recipe_env(arch)
        
        instDir = self.ctx.python_installs_dir

        with current_directory(join(self.get_build_dir(arch.arch), 'liquidfun/Box2D')):

            sh.cp(
                "{ctx.ndk_dir}/sources/cxx-stl/gnu-libstdc++/{ctx.toolchain_version}/libs/{arch.arch}/libgnustl_shared.so".format(ctx=self.ctx,arch=arch),
                self.ctx.get_libs_dir(arch.arch)
            )
        
            shprint(sh.rm, '-f', 'CMakeCache.txt')
            shprint(sh.cmake, '-G', 'Unix Makefiles',
                    '-DP4A=ON','-DANDROID_ABI={}'.format(arch.arch),
                    '-DPYBIND11_HAS_NO_STD_TO_STRING=1',
                    '-DBOX2D_BUILD_STATIC=0',
                    '-DBOX2D_BUILD_EXAMPLES=0',
                    '-DBOX2D_BUILD_UNITTESTS=0',
                    '-DBOX2D_CODE_COVERAGE=0',
                    #'-DPYBIND11_PYTHON_VERSION=2.7',
                    '-DCMAKE_INSTALL_PREFIX=./install',
                    '-DPYTHON_EXECUTABLE={}/bin/python2.7'.format(instDir),
                    '-DPYTHON_INCLUDE_DIR={}/include/python2.7'.format(instDir),
                    '-DPYTHON_LIBRARY={}/lib/libpython2.7.so'.format(instDir),
                    #'-DCMAKE_TOOLCHAIN_FILE=p4a.cmake', 
                    _env=env)
            shprint(sh.make, _env=env)

            self.install_libs(arch, join('Box2D/Release', 'libliquidfun.so'))


            sh.cp('-R','python/pybox2d',
                self.ctx.get_site_packages_dir()
            )



recipe = Pybox2dRecipe()

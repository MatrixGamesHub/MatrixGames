
from distutils.core import setup
import py2exe, sys, os

gameConsolePath = 'Applications/GameConsole'

sys.path.insert(0, gameConsolePath)
sys.argv.append('py2exe')

logo = os.path.join('dist/images/logo.ico')

distDir = "dist/MatrixGames"

if not os.path.isdir(distDir):
    os.makedirs(distDir)

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.version = "0.1"
        self.product_version = "0.1"
        self.company_name = "VonAncken"
        self.copyright = "(c) 2016"
        self.name = "Matrix Games - Game Console"

RT_MANIFEST = 24
MANIFEST = """<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
  <assemblyIdentity
    version="0.6.8.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s Program</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
          level="asInvoker"
          uiAccess="false"
        />
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
        type="win32"
        name="Microsoft.VC90.CRT"
        version="9.0.21022.8"
        processorArchitecture="x86"
        publicKeyToken="1fc8b3b9a1e18e3b"
      />
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
        type="win32"
        name="Microsoft.Windows.Common-Controls"
        version="6.0.0.0"
        processorArchitecture="x86"
        publicKeyToken="6595b64144ccf1df"
        language="*"
      />
    </dependentAssembly>
  </dependency>
</assembly> """

targetWxGameConsole = Target(
    script = os.path.join(gameConsolePath, 'GameConsole.py'),
    other_resources = [(RT_MANIFEST, 1, MANIFEST % dict(prog="Matrix Games - Game Console"))],
    icon_resources = [(1, logo)],
    )


def GetGamesFiles(path):
    res = []
    path = os.path.abspath(path)

    if os.path.isfile(path):
        path = os.path.dirname(path)

    basePath = os.path.dirname(path)


    for root, dirs, files in os.walk(path):
        if '__pycache__' in root:
            continue

        p = root.split(basePath)[-1]
        p = p if len(p) == 0 or p[0] != '\\' else p[1:]
        l = []
        for f in files:
            l.append(os.path.join(root, f))

        res. append([p, l])
    return res


setup(
    options = {'build': {'build_base': 'build'},
               'py2exe': {
                 'bundle_files': 1,
                 'compressed': True,
                 'includes': [],
                 'dist_dir': distDir,
               }
              },
    windows = [targetWxGameConsole],
    zipfile = None,
    data_files = GetGamesFiles("Games"),
)
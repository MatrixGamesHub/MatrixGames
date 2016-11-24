
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

import os
import sys
import shutil

WORKDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
PYTHON  = sys.executable


def check():
    logging.info("checking for wxPython...")
    try:
        import wx
    except ImportError:
        logging.error("Please install wxPython - http://www.wxpython.org/")
        sys.exit(1)
    logging.info("    ok.")

    logging.info("checking for py2exe...")
    try:
        import py2exe
    except ImportError:
        logging.error("Please install py2exe - http://www.py2exe.org/")
        sys.exit(1)
    logging.info("    ok.")

    logging.info("checking for python executable...")
    if not os.path.exists(PYTHON):
        logging.error("Please setup the python executable in this script!")
        sys.exit(1)
    logging.info("    ok.")



def clean():
    logging.info("cleaning...")
    if os.path.exists(os.path.join(WORKDIR, "dist")):
       os.system("rd /s /q \"%s\"" % os.path.join(WORKDIR, "dist"))

    if os.path.exists(os.path.join(WORKDIR, "build")):
       os.system("rd /s /q \"%s\"" % os.path.join(WORKDIR, "build"))

    if os.path.exists(os.path.join(WORKDIR, "release")):
       os.system("rd /s /q \"%s\"" % os.path.join(WORKDIR, "release"))

    if os.path.exists(os.path.join(WORKDIR, "version.info")):
       os.system("del \"%s\"" % os.path.join(WORKDIR, "version.info"))

    logging.info("    done.")

def compile():
    clean()
    os.chdir(WORKDIR)

    logging.info("running py2exe...")
    os.system("%s Setup.py build" % PYTHON)
    logging.info("    done.")

def install():
    if not os.path.exists(os.path.join(WORKDIR, "dist")):
        compile()

    sys.path.insert(0, "src")
    import Constants

if __name__ == "__main__":
    logging.info("Matrix Games - wxGameConsole")
    check()

    if len(sys.argv) > 1:
        if sys.argv[1] == "clean":
            clean()
        elif sys.argv[1] == "compile":
            clean()
            compile()
        elif sys.argv[1] == "install":
            install()
        sys.exit(0)

    install()
    logging.info("all done.")

"""
FireWorks implementation for the computation of electronic structure for
molecules in the Metatlas database.

-----------    ----------    -----------
| Create  |    | Run    |    | Process |
| Orca    | => | Orca   | => | Output  |
| Input   |    | Calc   |    | File    |
-----------    ----------    -----------
"""
import pybel
import sys
from multiprocessing import Pool
from glob import glob
from fireworks import Firework, FWorker
from fireworks.core.rocket_launcher import rapidfire
from metatlas import ProtonateMolecule, create_launchpad


def multirapid(nthreads):
    pool = Pool(processes=nthreads)
    pool.map(rapid, range(nthreads))

def rapid(dummy):
    lpad = create_launchpad(LOCAL_DB_CONFIG)
    rapidfire(lpad, FWorker(), nlaunches=25000)

def add_fws(reset=False):
    if reset:
        lpad.reset('', require_password=False)
    lpad = create_launchpad(LOCAL_DB_CONFIG)

    for fname in glob(QM9_DATA_HOME+'/*'):
        pm3 = Firework(ProtonateMolecule(xyzparent=fname),
                       name=fname.split('.')[0])

        lpad.add_wf(pm3)
    return


if __name__ == "__main__":
    LOCAL_DB_CONFIG = '/home/bkrull/.fireworks/local_db.ini'
    QM9_DATA_HOME = '/home/bkrull/Documents/data/qm9'
    PROJECT_HOME = 'scr/'

    nthreads = int(sys.argv[1])
    multirapid(nthreads)

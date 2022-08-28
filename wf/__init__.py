"""
Assemble and sort some COVID reads...
"""

import subprocess
from pathlib import Path

from latch import large_task, small_task, workflow
# from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchAuthor, LatchDir, LatchFile, LatchMetadata, LatchParameter
from enum import Enum
from typing import Union, Optional, List
from latch.resources.launch_plan import LaunchPlan

class GuideTree(Enum):
    sl = 'Single Linkage Tree' # Single Linkage Tree
    upgma = 'UPGMA' # UPGMA
    nj = 'Neighbor Joining Tree' # Neighbor Joining Tree

famsa_exports = '''
GUIDE TREE EXPORTS

export a neighbour joining guide tree to the Newick format
./famsa -gt nj -gt_export ./test/adeno_fiber/adeno_fiber nj.dnd
./famsa -gt upgma -gt_export input.fasta tree.dnd

# export a distance matrix to the CSV format (lower triangular) 
./famsa -dist_export ./test/adeno_fiber/adeno_fiber dist.csv

# export a pairwise identity (PID) matrix to the CSV format (square) 
./famsa -dist_export -pid -square_matrix ./test/adeno_fiber/adeno_fiber pid.csv
'''

@large_task
def famsa_alignment(
    input: LatchFile,
    output: str = 'famsa-alignment',
    guideTree: Union[GuideTree,LatchFile] = GuideTree.sl,
    medoidTree: Optional[int] = 0,
    gzip: bool = False,
    ) -> LatchFile:

    input_path = Path(input).resolve()
    output+='.aln'
    
    if gzip: output+='.gz'
    output_path = Path(output).resolve()

    gtOptions = {
        'Single Linkage Tree':'sl',
        'UPGMA':'upgma',
        'Neighbor Joining Tree':'nj'
        }

    gtFile=''
    if isinstance(guideTree, GuideTree):
        gtValue = str(guideTree.value)
        for gt in gtOptions.keys():
            if gt == gtValue:
                gtValue = gtOptions[gt]
    else:
        gtValue = 'import'
        gtFile = Path(guideTree).resolve()

    famsa_cmd = [
        './FAMSA/famsa',
        '-gt',
        gtValue,
        str(gtFile),
        str(input_path),
        str(output_path)
    ]

    if isinstance(guideTree, GuideTree): famsa_cmd.pop(3)
    if isinstance(medoidTree, int): famsa_cmd[1:1] = ['-medoidtree','-medoid_threshold',str(medoidTree)]
    if gzip: famsa_cmd[1:1] = ['-gz','-gz-lev','9']

    subprocess.run(famsa_cmd)

    return LatchFile(str(output_path), f"latch:///{output_path}")

"""The metadata included here will be injected into your interface."""

metadata = LatchMetadata(
    display_name="FAMSA",
    author=LatchAuthor(
        name="Shivaramakrishna Srinivasan",
        email="shivaramakrishna.srinivasan@gmail.com",
        github="github.com/shivaramakrishna99",
    ),
    repository="https://github.com/shivaramakrishna99/famsa-latch",
    license="GPL-3.0",
    parameters= {
        "input": LatchParameter(
            display_name="Input",
            description="Enter text or FASTA",
        ),
        "guideTree": LatchParameter(
            display_name="Guide Tree",
            description="Choose between three guide trees",
        ),
        "medoidTree": LatchParameter(
            display_name="Enable medoid trees for sets with minimum specified sequences",
            description="",
            section_title="Medoid Tree"
        ),
        "output": LatchParameter(
            display_name="Filename",
            description="Name output file",
            section_title="Output"
        ),
        'gzip': LatchParameter(
            display_name="Compress File",
            description="Enable gzipped output",
        ),
    },
)

@workflow(metadata)
def famsa(
    input: LatchFile,
    output: str = 'famsa-alignment',
    guideTree: Union[GuideTree,LatchFile] = GuideTree.sl,
    medoidTree: Optional[int] = 0,
    gzip: bool = False,
    ) -> LatchFile:
    """F
    FAMSA Long Desc
    """
    return famsa_alignment(
    input=input,
    output=output,
    guideTree=guideTree,
    medoidTree=medoidTree,
    gzip=gzip
)


"""
Add test data with a LaunchPlan. Provide default values in a dictionary with
the parameter names as the keys. These default values will be available under
the 'Test Data' dropdown at console.latch.bio.
"""
LaunchPlan(
    famsa,
    "Refresh Bio's Data",
    {
        "input": LatchFile("s3://latch-public/test-data/3701/FAMSA/test/adeno_fiber/adeno_fiber"),
        "guideTree": LatchFile("s3://latch-public/test-data/3701/FAMSA/test/adeno_fiber/slink.dnd")
    },
)

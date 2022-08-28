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

class GuideTree(Enum):
    sl = 'sl' # Single Linkage Tree
    upgma = 'upgma' # UPGMA
    nj = 'nj' # Neighbor Joining Tree

famsa_exports = '''
GUIDE TREE EXPORTS

export a neighbour joining guide tree to the Newick format
./famsa -gt nj -gt_export ./test/adeno_fiber/adeno_fiber nj.dnd

# export a distance matrix to the CSV format (lower triangular) 
./famsa -dist_export ./test/adeno_fiber/adeno_fiber dist.csv

# export a pairwise identity (PID) matrix to the CSV format (square) 
./famsa -dist_export -pid -square_matrix ./test/adeno_fiber/adeno_fiber pid.csv
'''

@large_task
def famsa_alignment(
    input: LatchFile,
    output: str = 'famsa-alignment',
    guideTree: GuideTree = GuideTree.sl,
    threads: int = 8,
    medoidTree: bool = False,
    medoidThreshold: Optional[int] = None,
    gz: bool = False,
    gzLevel: int = 7
    ) -> LatchFile:

    input_path = Path(input).resolve()
    
    output_path = Path(output).resolve()

    famsa_cmd = [
        './FAMSA/famsa',
        '-gt',
        str(guideTree.value),
        '-t',
        str(threads),
        str(input_path),
        str(output_path)
    ]

    if medoidTree == True: famsa_cmd[1:1] = ['-medoidtree','-medoid_threshold',str(medoidThreshold)]
    if gz == True: famsa_cmd[1:1] = ['-gz','-gz-lev',str(gzLevel)]

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
        "output": LatchParameter(
            display_name="Output",
            description="Name output file (without extension)",
        ),
        "guideTree": LatchParameter(
            display_name="Guide Tree",
            description="Choose between three guide trees, or upload a custom one in Newick format",
        ),
        "threads": LatchParameter(
            display_name="Number of Threads",
            description="Choose number of threads required for operation.  Default is 0, means all available threads.",
        ),
        "medoidTree": LatchParameter(
            display_name="Medoid Tree",
            description="Enable/disable medoid trees for sets with minimum specified sequences",
            section_title="Medoid Tree"
        ),
        "medoidThreshold": LatchParameter(
            display_name="Medoid Threshold",
            description="Define a threshold number of sequence for a set on which medoid trees can be used",
        ),
        'gz': LatchParameter(
            display_name="Gzip Output",
            description="Enable gzipped output",
            section_title="GZip Export"
        ),
        'gzLevel': LatchParameter(
            display_name="Compression Level",
            description="Set a compression level for gzip between 0 to 9. Default is 7",
        ),
    },
)

@workflow(metadata)
def famsa(
    input: LatchFile,
    output: str = 'famsa-alignment',
    guideTree: GuideTree = GuideTree.sl,
    threads: int = 8,
    medoidTree: bool = False,
    medoidThreshold: Optional[int] = None,
    gz: bool = False,
    gzLevel: int = 7,
    ) -> LatchFile:
    """FAMSA Short Desc
    FAMSA Long Desc
    """
    return famsa_alignment(
    input=input,
    output=output,
    guideTree=guideTree,
    threads=threads,
    medoidTree=medoidTree,
    medoidThreshold=medoidThreshold,
    gz=gz,
    gzLevel=gzLevel
    )


"""
Add test data with a LaunchPlan. Provide default values in a dictionary with
the parameter names as the keys. These default values will be available under
the 'Test Data' dropdown at console.latch.bio.
"""
# LaunchPlan(
#     assemble_and_sort,
#     "Test Data",
#     {
#         "read1": LatchFile("s3://latch-public/init/r1.fastq"),
#         "read2": LatchFile("s3://latch-public/init/r2.fastq"),
#     },
# )

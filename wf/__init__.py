"""
Assemble and sort some COVID reads...
"""

import subprocess
from pathlib import Path

from latch import large_task, small_task, workflow
# from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchAuthor, LatchDir, LatchFile, LatchMetadata, LatchParameter
from enum import Enum

class GuideTree(Enum):
    sl = 'sl' # Single Linkage Tree
    upgma = 'upgma' # UPGMA
    nj = 'nj' # Neighbor Joining Tree
    custom  = 'import' # Custom guide tree

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
def famsa_alignment() -> LatchFile:

    bam_file = "hello"

    return LatchFile('/root/{bam_file}', "latch:///covid_sorted.bam")

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
            description="Choose between three guide trees, or upload a custom one in Newick format",
        ),
        "threads": LatchParameter(
            display_name="Number of Threads",
            description="Choose number of threads required for operation.  Default is 0, means all available threads.",
        ),
        "medoidTree": LatchParameter(
            display_name="Mediod Tree",
            description="Enable/disable medoid trees for sets with minimum specified sequences",
            section_title="Medoid Tree"
        ),
        "medoidThreshold": LatchParameter(
            display_name="Mediod Threshold",
            description="Set number of minimum sequences to use medoid trees",
            section_title="Medoid Tree"
        ),
        'gz': LatchParameter(
            display_name="Gzip Output",
            description="Enable gzipped output",
            section_title="GZip export"
        ),
        'gzLevel': LatchParameter(
            display_name="Gzip Compression Level",
            description="Set a compression level for gzip between 0 to 9. Default is 7",
            section_title="GZip export"
        )
    },
)

@workflow(metadata)
def famsa() -> LatchFile:
    """Description...

    markdown header
    ----

    Write some documentation about your workflow in
    markdown here:

    > Regular markdown constructs work as expected.

    # Heading

    * content1
    * content2
    """
    return famsa_alignment()


# @large_task
# def famsa(
#     input: LatchFile,
#     customGuideTree: LatchFile,
#     output: LatchFile,
#     guideTree: GuideTree = GuideTree.sl,
#     threads: int = 8,
#     medoidTree: bool = False,
#     medoidThreshold = int,
#     gz: bool = False,
#     gzLevel: int = 7,
#     ) -> LatchFile:

#     _famsa_cmd = [
#         "./FAMSA/famsa",
#     ]
#     return LatchFile(f"/root/{output}", f"latch:///{output}.txt")


# """The metadata included here will be injected into your interface."""
# @workflow(metadata)
# def famsaTask(
#     input: LatchFile,
#     customGuideTree: LatchFile,
#     output: LatchFile,
#     guideTree: GuideTree = GuideTree.sl,
#     threads: int = 8,
#     medoidTree: bool = False,
#     medoidThreshold = int,
#     gz: bool = False,
#     gzLevel: int = 7
#     ) -> LatchFile:
#     """Description...

#     markdown header
#     ----

#     Write some documentation about your workflow in
#     markdown here:

#     > Regular markdown constructs work as expected.

#     # Heading

#     * content1
#     * content2
#     """
#     return famsa(
#     input=input,
#     customGuideTree=customGuideTree,
#     output=output,
#     guideTree=guideTree,
#     threads=threads,
#     medoidTree=medoidTree,
#     medoidThreshold=medoidThreshold,
#     gz=gz,
#     gzLevel=gzLevel,
#     )




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

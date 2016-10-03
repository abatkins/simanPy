# simanPy
Python Interface for Siman Simulation Lanaguage

This project is still under active development. Please create an issue for bugs.

## Dependencies
* Must have SIMAN installed on the machine.
* Python 3

## Getting Started

The core data structure of SimanPy is a model, which is a way to organize blocks and elements.
<pre>
from model import Model

model = Model()
</pre>

Blocks and elements can be added to the model using .add():
<pre>
from elements import Entity, Project, Replicate

model = Model("Sample1")
model.add(Project(title="Sample Project", analyst_name="Your Name"))
model.add(Replicate(num_replications=1, begin_time=0, replication_len=480))
</pre>

Elements that are passed to blocks will automatically be added to the Model with the block.
<pre>
entity = Entity()
model.add(CreateBlock(entity, interval="EXPO(4.4)"))

queue = Queue(name="Buffer", ranking_criterion="FIFO")
model.add(QueueBlock(queue, capacity=100))
</pre>

Blocks are written to the .mod file in the order they are added to the Model.
The order elements are added to the Model does not matter.

To generate the .mod and .exp files:
<pre>
model.compile()
</pre>

To generate all files and run the simulation, simply use:
<pre>
model.run()
</pre>

## Super Blocks

Super blocks can be used to create block sequences with a reference ID. This is useful for Branch Blocks.
Like other blocks, super blocks will be written to the .mod file in the same order they are added to Model.
<pre>
# Straightener Station
straightenQueueBlock = QueueBlock(straightenQueue)
straightenSeize = SeizeBlock(straightener)
straightenDelay = DelayBlock(duration="EXPO(15)")
straightenRelease = ReleaseBlock(straightener)

straightenerPipeline = [straightenQueueBlock, straightenSeize, straightenDelay, straightenRelease]
straightenStation = SuperBlock("StraightenerStation", straightenerPipeline)

...
...

branch1 = BranchBlock(max_branches=1, branch_type="If", condition="Entity.Type==Part1",
                      destination_label=straightenStation.name)
branch1.add(branch_type="ELSE", destination_label=finishStation.name)
model.add(branch1)

model.add(straightenStation)
</pre>



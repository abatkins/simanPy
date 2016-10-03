from model import Model
from blocks import *
from elements import *

# Initialize model
model = Model("sample2")
model.add(Project(title="Sample2 Project", analyst_name="Your Name"))
model.add(Replicate(num_replications=1, begin_time=0, replication_len=5000, warmup_period=1000))

# Define Resources
drill = Resource(name="Drill", capacity=2)
straightener = Resource(name="Straightener", capacity=1)
finisher = Resource(name="Finisher", capacity=1)

# Define Queues
drillQueue = Queue(name="Drill.Queue")
straightenQueue = Queue(name="Straighten.Queue")
finishQueue = Queue(name="Finish.Queue")

# Define Counters
counter1 = Counter(name="Part1")
counter2 = Counter(name="Part2")
counterTotal = Counter(name="TotalEntities")

# ------- SuperBlocks ------------
# Drill Station
drillQueueBlock = QueueBlock(drillQueue)
drillSeize = SeizeBlock(drill, num_units=1)
drillDelay = DelayBlock(duration="NORM(10,1)")
drillRelease = ReleaseBlock(drill)

drillPipeLine = [drillQueueBlock, drillSeize, drillDelay, drillRelease]
drillStation = SuperBlock("DrillStation", drillPipeLine)

# Straightener Station
straightenQueueBlock = QueueBlock(straightenQueue)
straightenSeize = SeizeBlock(straightener)
straightenDelay = DelayBlock(duration="EXPO(15)")
straightenRelease = ReleaseBlock(straightener)

straightenerPipeline = [straightenQueueBlock, straightenSeize, straightenDelay, straightenRelease]
straightenStation = SuperBlock("StraightenerStation", straightenerPipeline)

# Finish Station
finishQueueBlock = QueueBlock(finishQueue)
finishSeize = SeizeBlock(finisher)
finishDelay = DelayBlock(5)
finishRelease = ReleaseBlock(finisher)

finishPipeline = [finishQueueBlock, finishSeize, finishDelay, finishRelease]
finishStation = SuperBlock("FinishStation", finishPipeline)

# Model Blocks
# todo: Determine how MARK(TimeIn) should be implemented
model.add(CreateBlock(Entity("Part1"), batch_size=1, offset_time=0, interval=30))
model.add(CountBlock(counter1))
delay1 = DelayBlock(duration=2)
delay1.set_next(drillStation)
model.add(delay1)

model.add(CreateBlock(Entity("Part2"), batch_size=1, offset_time=0, interval=20))
model.add(CountBlock(counter2))
model.add(DelayBlock(duration=10))

model.add(drillStation)

branch1 = BranchBlock(max_branches=1, branch_type="If", condition="Entity.Type==Part1",
                      destination_label=straightenStation.name)
branch1.add(branch_type="ELSE", destination_label=finishStation.name)
model.add(branch1)

model.add(straightenStation)

model.add(finishStation)

model.add(CountBlock(counterTotal))
model.add(DisposeBlock())

model.compile()



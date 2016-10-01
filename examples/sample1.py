from elements import *
from blocks import *
from model import Model

model = Model("test")
model.add(Project(title="Simple Project", analyst_name="Your Name"))
model.add(Discrete(max_entities=100))
model.add(Replicate(num_replications=1, begin_time=0, replication_len=480))

entity = Entity()
model.add(CreateBlock(entity, interval="EXPO(4.4)"))

queue = Queue(name="Buffer", ranking_criterion="FIFO")
model.add(QueueBlock(queue, capacity=100))

resource = Resource(name="Machine")
model.add(SeizeBlock(resource))

model.add(DelayBlock("TRIA(3.2,4.2,5.2)"))

model.add(ReleaseBlock(resource))

counter = Counter(name="JobsDone")
model.add(CountBlock(counter))

model.add(DisposeBlock())

model.compile()
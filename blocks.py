class Block:
    def __init__(self, mod):
        self._mod = mod

    def __str__(self):
        return self._mod


class Create(Block):
    def __init__(self, batch_size="", offset_time="", interval="", maximum_batches=""):
        mod = "CREATE, %s, %s: %s, %s;" % (str(batch_size), str(offset_time), str(interval), str(maximum_batches))
        super().__init__(mod)


# todo: implement block label and repeats
# todo: potentially elements should be a whole other abstract class.
# todo: Elements may need to contain specific attributes that can be passed to blocks for initialization. They could also be passed in a list for repeats
class Queue(Block):
    def __init__(self, queue_id="", capacity="", balk_label=""):
        mod = "QUEUE, %s, %s, %s;" % (str(queue_id), str(capacity), str(balk_label))
        super().__init__(mod)


# todo: handle repeates. Either have add_repeats method or alow for adding lists of resource_id and num_units
class Seize(Block):
    def __init__(self, priority="", resource_id="", num_units=""):
        mod = "SEIZE, %s: %s, %s;" % (str(priority), str(resource_id), str(num_units))
        super().__init__(mod)


class Delay(Block):
    def __init__(self, duration="", storage_id=""):
        mod = "DELAY: %s, %s;" % (str(duration), str(storage_id))
        super().__init__(mod)


class Release(Block):
    def __init__(self, resource_id="", quantity_to_release=""):
        mod = "RELEASE: %s, %s;" % (str(resource_id), str(quantity_to_release))
        super().__init__(mod)


class Count(Block):
    def __init__(self, counter_id="", counter_increment=""):
        mod = "COUNT: %s, %s" %(str(counter_id), str(counter_increment))
        super().__init__(mod)


class Dispose(Block):
    def __init__(self):
        mod = "DISPOSE;"
        super().__init__(mod)

c = Create(1)
print(c)
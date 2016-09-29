# TODO: Add param class that simply returns discrete list of params for a given block/elem. Example: param.branchtype.if
class Block:
    def __init__(self, mod):
        self._mod = mod
        self._next = None
        self.ext = "mod"

    def __str__(self):
        if self._next:
            return self._mod + ": %s;" % self._next
        else:
            return self._mod + ";"

    def set_next(self, obj):
        self._next = obj

    def add(self, add_list):
        self._mod += ":\n\t\t%s, %s, %s" % (str(x) for x in add_list)


# todo: determine if element_ids should be passed to block as string or an object
class Create(Block):
    def __init__(self, batch_size="", offset_time="", entity_id="", interval="", maximum_batches=""):
        mod = "CREATE, %s, %s, %s: %s, %s" % (str(batch_size), str(offset_time), str(entity_id), str(interval), str(maximum_batches))
        super().__init__(mod)


# todo: implement balk label
class Queue(Block):
    def __init__(self, queue_id="", capacity="", balk_label=""):
        mod = "QUEUE, %s, %s, %s" % (str(queue_id), str(capacity), str(balk_label))
        super().__init__(mod)


class Seize(Block):
    def __init__(self, priority="", resource_id="", num_units=""):
        mod = "SEIZE, %s: %s, %s" % (str(priority), str(resource_id), str(num_units))
        super().__init__(mod)

    def add(self, resource_id="", num_units=""):
        add_list = [resource_id, num_units]
        super().add(add_list)


class Delay(Block):
    def __init__(self, duration="", storage_id=""):
        mod = "DELAY: %s, %s" % (str(duration), str(storage_id))
        super().__init__(mod)


class Release(Block):
    def __init__(self, resource_id="", quantity_to_release=""):
        mod = "RELEASE: %s, %s" % (str(resource_id), str(quantity_to_release))
        super().__init__(mod)

    def add(self, resource_id="", quantity_to_release=""):
        add_list = [resource_id, quantity_to_release]
        super().add(add_list)


class Count(Block):
    def __init__(self, counter_id="", counter_increment=""):
        mod = "COUNT: %s, %s" %(str(counter_id), str(counter_increment))
        super().__init__(mod)


class Dispose(Block):
    def __init__(self):
        mod = "DISPOSE"
        super().__init__(mod)


# class Assign(Block):

class Branch(Block):
    def __init__(self, max_branches, rand_num_stream, branch_type, condition, destination_label):
        mod = "Branch, %s, %s: %s, %s, %s" % (
            str(x) for x in [max_branches, rand_num_stream, branch_type, condition, destination_label]
        )
        super().__init__(mod)

    def add(self, branch_type, condition, destination_label):
        add_list = [branch_type, condition, destination_label]
        super().add(add_list)


class SuperBlock:
    """Create group of sequential blocks with reference id"""
    def __init__(self, super_id, blocks):
        if not isinstance(blocks, (list, tuple)):
            raise TypeError('argument must be list or tuple')
        if len(blocks) == 0:
            raise ValueError("empty list")

        self.super_id = super_id
        self.blocks = blocks

    def __str__(self):
        return self.super_id + "\t\t" + "\n\t\t\t\t".join(self.blocks)


c = Create(1)
print(c)

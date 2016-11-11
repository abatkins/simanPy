from elements import _Begin, _End, _Queues, _Entities, _Counters, _Resources, _Attributes, _Variables, _Dstats, \
    _Tallies, _Storages, _Outputs, _Stations
import subprocess


class Model:
    def __init__(self, filename, run_controller="No"):
        self.filename = filename
        self.exp = []
        self.mod = []
        self.collections = {}
        self.run_controller = run_controller


    # Allocates block and element data to correct file
    def add(self, obj):
        if obj.type == "mod":
            if hasattr(obj, "blocks") and obj.blocks:  # check if superblock
                for block in obj.blocks:
                    if hasattr(block, "element") and block.element:
                        self._add_element(block.element)
            else:  # normal block
                if hasattr(obj, "element") and obj.element:
                    self._add_element(obj.element)
            self.mod.append(obj)
        elif obj.type == "exp":  # Elements block
            self.exp.append(obj)
        elif obj.type == "element":  # Element blockS
            self._add_element(obj)
        else:
            raise ValueError("Extension type %s is not recognized" % obj.type)

    def _to_collection(self, key, elements_inst, element):
        collection = self.collections.get(key, elements_inst)
        if element.number == "":
            element.number = len(collection.elements) + 1
        collection.add(element)
        self.collections[key] = collection

    # Adds element stored in blocks
    def _add_element(self, element):
        key = element.__class__.__name__
        if key == "Queue":
            self._to_collection(key, _Queues(), element)
        elif key == "Resource":
            self._to_collection(key, _Resources(), element)
        elif key == "Counter":
            self._to_collection(key, _Counters(), element)
        elif key == "Attribute":
            self._to_collection(key, _Attributes(), element)
        elif key == "Variable":
            self._to_collection(key, _Variables(), element)
        elif key == "Dstat":
            self._to_collection(key, _Dstats(), element)
        elif key == "Tally":
            self._to_collection(key, _Tallies(), element)
        elif key == "Storage":
            self._to_collection(key, _Storages(), element)
        elif key == "Entity":
            self._to_collection(key, _Entities(), element)
        elif key == "Output":
            self._to_collection(key, _Outputs(), element)
        elif key == "Station":
            self._to_collection(key, _Stations(), element)
        else:
            raise ValueError("Class name not recognized!")

    # Writes to SIMAN files
    def compile(self):
        exp = list(self.collections.values()) + self.exp
        mod_filename = self.filename + ".mod"
        exp_filename = self.filename + ".exp"
        self._to_file(mod_filename, self.mod)
        self._to_file(exp_filename, exp)

        return mod_filename, exp_filename

    # Run model.exe
    def run_mod(self, input_file, output_file=None):
        if not output_file:
            output_file = input_file.split('.')[0] + '.m'
        subprocess.run('model {} {}'.format(input_file, output_file), shell=True, check=True)
        return output_file

    # Run expmt.exe
    def run_expmt(self, input_file, output_file=None):
        if not output_file:
            output_file = input_file.split('.')[0] + '.e'
        subprocess.run('expmt {} {}'.format(input_file, output_file),shell=True, check=True)
        return output_file

    # Run linker.exe
    def run_link(self, mod_file, exp_file, output_file=None):
        if not output_file:
            output_file = mod_file.split('.')[0] + '.p'
        subprocess.run('linker {} {} {}'.format(mod_file, exp_file, output_file), shell=True, check=True)
        return output_file

    # Run siman.exe
    def run_siman(self, input_file, suppress=False):
        if suppress:
            subprocess.run('siman {} > {}.out'.format(input_file, input_file.split('.')[0]), shell=True, check=True)
        else:
            subprocess.run('siman {}'.format(input_file), shell=True, check=True)

    # Run Simulation
    def run(self, suppress=False):
        mod_filename, exp_filename = self.compile()
        m_filename = self.run_mod(mod_filename)
        e_filename = self.run_expmt(exp_filename)
        p_filename = self.run_link(m_filename, e_filename)
        self.run_siman(p_filename, suppress)

    def _to_file(self,filename, objs):
        file = open(filename, 'w')
        file.write("%s\n" % str(_Begin(run_controller=self.run_controller)))
        for obj in objs:
            file.write("%s\n" % obj)
        file.write(str(_End()))
        file.close()
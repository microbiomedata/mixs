import pprint

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper

mixs_url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/model/schema/mixs.yaml"

mixs_view = SchemaView(mixs_url)

# print(mixs_view.schema.name)

schema_slots = mixs_view.all_slots()

# slow
# ui = mixs_view.usage_index()

schema_slots_names = list(schema_slots.keys())

environment_field_descendants = mixs_view.slot_descendants("environment field")

environment_field_ancestors = mixs_view.slot_ancestors("environment field")

# pprint.pprint(schema_slots_names)

# pprint.pprint(ui.keys())


# pprint.pprint(ui["depth"])

# print(yaml_dumper.dumps(environment_field_descendants))

# print(yaml_dumper.dumps(environment_field_ancestors))


print(yaml_dumper.dumps(mixs_view.get_slot('depth')))


def get_attribute_keys(schema_view, class_name):
    ic = schema_view.induced_class(class_name)
    ic_attributes = ic.attributes
    ic_attribute_keys = list(ic_attributes.keys())
    ic_attribute_keys.sort()
    return ic_attribute_keys


for current_inducable in ["soil", "MIMS", "soil MIMS"]:
    print(current_inducable)
    ic_attrib_names = get_attribute_keys(mixs_view, current_inducable)
    print(ic_attrib_names)


# slow
def all_classes_all_slots(schema_view: SchemaView):
    classes = [str(v.name) for k, v in schema_view.all_classes().items() if v.name]
    classes.sort()
    slot_to_classes = {}
    class_to_slots = {}
    mixin_to_classes = {}
    classes_to_mixins = {}
    checklists = []
    combinations = []
    environments = set()
    environments_to_combos = {}
    for current_class in classes:
        induced = schema_view.induced_class(current_class)
        if schema_view.is_mixin(current_class):
            print(f"    {current_class} is a mixin")
            checklists.append(current_class)
        else:
            print(f"    {current_class} is not a mixin")
        if induced.mixins:
            classes_to_mixins[current_class] = induced.mixins
            for i in induced.mixins:
                # it's an environment
                print(f"    {current_class} uses mixin: {i}")
                environment = induced.is_a
                environments.add(environment)
                combinations.append(current_class)
                if i not in mixin_to_classes:
                    mixin_to_classes[i] = [current_class]
                else:
                    mixin_to_classes[i].append(current_class)
                slot_to_classes[slot].append(current_class)
                if environment not in environments_to_combos:
                    environments_to_combos[environment] = [current_class]
                else:
                    environments_to_combos[environment].append(current_class)
                slot_to_classes[slot].append(current_class)
        else:
            print(f"    {current_class} does not use mixins")
        attributes = list(induced.attributes.keys())
        attributes.sort()
        class_to_slots[current_class] = attributes
        for slot in attributes:
            print(f"{current_class} {slot}")
            if slot not in slot_to_classes:
                slot_to_classes[slot] = [current_class]
            else:
                slot_to_classes[slot].append(current_class)
            slot_to_classes[slot].append(current_class)
    return class_to_slots, slot_to_classes, mixin_to_classes, classes_to_mixins, checklists, combinations, environments, environments_to_combos, abstract_slots


abstract_slots = []
for k, v in mixs_view.all_slots().items():
    if v.abstract:
        abstract_slots.append(k)

mixs_class_to_slots, mixs_slot_to_classes, \
mixs_mixin_to_classes, mixs_classes_to_mixins, \
mixs_checklists, mixs_combinations, mixs_environments, \
mixs_environments_to_combos, mixs_abstracts = all_classes_all_slots(
    mixs_view)

print("mixs_class_to_slots")
pprint.pprint(mixs_class_to_slots)

# todo soil_depth but no soil!
print("mixs_slot_to_classes")
pprint.pprint(mixs_slot_to_classes)

print("mixs_mixin_to_classes")
pprint.pprint(mixs_mixin_to_classes)

print("mixs_classes_to_mixins")
pprint.pprint(mixs_classes_to_mixins)

print("mixs_checklists")
pprint.pprint(mixs_checklists)

print("mixs_combinations")
pprint.pprint(mixs_combinations)

print("mixs_environments")
pprint.pprint(mixs_environments)

print("mixs_environments_to_combos")
pprint.pprint(mixs_environments_to_combos)

non_utility = mixs_checklists + mixs_combinations + list(mixs_environments)
pprint.pprint(non_utility)

all_classes = list(mixs_class_to_slots.keys())

utility = list(set(all_classes) - set(non_utility))
utility.sort()
pprint.pprint(utility)

print(abstract_slots)

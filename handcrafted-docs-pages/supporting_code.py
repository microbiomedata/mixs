import pprint

import yaml
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


# print(yaml_dumper.dumps(mixs_view.get_slot('depth')))


def get_attribute_keys(schema_view, class_name):
    ic = schema_view.induced_class(class_name)
    ic_attributes = ic.attributes
    ic_attribute_keys = list(ic_attributes.keys())
    ic_attribute_keys.sort()
    return ic_attribute_keys


for current_inducable in ["soil", "MIMS", "soil MIMS"]:
    # print(current_inducable)
    ic_attrib_names = get_attribute_keys(mixs_view, current_inducable)
    # print(ic_attrib_names)


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


# abstract_slots = []
# for k, v in mixs_view.all_slots().items():
#     if v.abstract:
#         abstract_slots.append(k)
#
# mixs_class_to_slots, mixs_slot_to_classes, \
# mixs_mixin_to_classes, mixs_classes_to_mixins, \
# mixs_checklists, mixs_combinations, mixs_environments, \
# mixs_environments_to_combos, mixs_abstracts = all_classes_all_slots(
#     mixs_view)
#
#
#
# print("mixs_class_to_slots")
# pprint.pprint(mixs_class_to_slots)
#
# # todo soil_depth but no soil!
# print("mixs_slot_to_classes")
# pprint.pprint(mixs_slot_to_classes)
#
# print("mixs_mixin_to_classes")
# pprint.pprint(mixs_mixin_to_classes)
#
# print("mixs_classes_to_mixins")
# pprint.pprint(mixs_classes_to_mixins)
#
# print("mixs_checklists")
# pprint.pprint(mixs_checklists)
#
# print("mixs_combinations")
# pprint.pprint(mixs_combinations)
#
# print("mixs_environments")
# pprint.pprint(mixs_environments)
#
# print("mixs_environments_to_combos")
# pprint.pprint(mixs_environments_to_combos)
#
# non_utility = mixs_checklists + mixs_combinations + list(mixs_environments)
# pprint.pprint(non_utility)
#
# all_classes = list(mixs_class_to_slots.keys())
#
# utility = list(set(all_classes) - set(non_utility))
# utility.sort()
# pprint.pprint(utility)
#
# print(abstract_slots)

slots_to_classes = {}
slots_to_classes = {}
classes = mixs_view.all_classes()
classes_names = [str(v.name) for k, v in classes.items() if v.name]
classes_names.sort()
slots_names = set()

abstract_classes = []
mixins = []
uses_mixins = []
mixins_to_combinations = {}
envs_to_combinations = {}
slots_to_classes = {}
isa_parents = []
isa_children = []
abstract_slots = []

for current_class_name in classes_names:
    print(f"{current_class_name}")
    induced_class = mixs_view.induced_class(current_class_name)
    if induced_class.abstract:
        # print(f"    {current_class_name} is abstract")
        abstract_classes.append(current_class_name)
    else:
        # print(f"    {current_class_name} is not abstract")
        pass

    if induced_class.mixin:
        # print(f"    {current_class_name} is a mixin")
        mixins.append(current_class_name)
    else:
        # print(f"    {current_class_name} is not a mixin")
        pass

    if induced_class.mixins:
        # print(f"    {current_class_name} uses mixins: {induced_class.mixins}")
        uses_mixins.append(current_class_name)
        # todo assuming one mixin per combination
        if induced_class.mixins[0] not in mixins_to_combinations:
            mixins_to_combinations[induced_class.mixins[0]] = [current_class_name]
        else:
            mixins_to_combinations[induced_class.mixins[0]].append(current_class_name)
    else:
        # print(f"    {current_class_name} does not use mixins")
        pass

    if induced_class.is_a:
        # print(f"    {current_class_name} is a {induced_class.is_a}")
        isa_parents.append(induced_class.is_a)
        isa_children.append(current_class_name)
        if induced_class.is_a not in envs_to_combinations:
            envs_to_combinations[induced_class.is_a] = [current_class_name]
        else:
            envs_to_combinations[induced_class.is_a].append(current_class_name)
    else:
        # print(f"    {current_class_name} doesn't have an is_a parent")
        pass

    class_induced_slots = mixs_view.class_induced_slots(current_class_name)
    class_induced_slots_names = [str(x.name) for x in class_induced_slots if x.name]
    class_induced_slots_names.sort()
    for current_slot_name in class_induced_slots_names:
        slots_names.add(current_slot_name)
        # print(f"{current_class_name}: {current_slot_name}")
        if current_slot_name not in slots_to_classes:
            slots_to_classes[current_slot_name] = [current_class_name]
        else:
            slots_to_classes[current_slot_name].append(current_class_name)

slots = mixs_view.all_slots()
parent_child_slots = {}
slots_names = [str(v.name) for k, v in slots.items() if v.name]
for current_slot_name in slots_names:
    slot_obj = mixs_view.get_slot(current_slot_name)
    if slot_obj.abstract:
        abstract_slots.append(current_slot_name)
    # if slot_obj.is_a:
    #     if current_slot_name not in slots_to_classes:
    #         slots_to_classes[current_slot_name] = [current_class_name]
    #     else:
    #         slots_to_classes[current_slot_name].append(current_class_name)

# pprint.pprint(classes_names)
# slots_names = list(slots_names)
# slots_names.sort()
# pprint.pprint(slots_names)

# pprint.pprint(slots_to_classes)

# print(yaml.dump(slots_to_classes, default_flow_style=False))

print(f"depth classes {slots_to_classes['depth']}")
print(f"geo_loc_name classes {slots_to_classes['geo_loc_name']}")
print(f"ph classes {slots_to_classes['ph']}")

print(f"abstract_classes {abstract_classes}")
print(f"isa_children {isa_children}")
print(f"isa_parents {isa_parents}")
print(f"mixins {mixins}")
print(f"uses_mixins {uses_mixins}")

###

# wishes
# list of classes... are they abstract?
# group into checklists, combinations, environmental packages, other
print(f"classes_names {classes_names}")

# list of checklist classes: declared as a mixin
checklists = list(set(mixins))
checklists.sort()
print(f"checklists {checklists}")

#  details about MIMS
mims_induced = mixs_view.induced_class('MIMS')
mims_induced_attributes_names = [str(v.name) for k, v in mims_induced.attributes.items()]
mims_induced_attributes_names.sort()
print(f"mims_induced_attributes_names {mims_induced_attributes_names}")
# MIMS combinations
pprint.pprint(mixins_to_combinations['MIMS'])

# list of combination classes: mixin and is_a assertions
combinations = list(set(isa_children).intersection(set(uses_mixins)))
combinations.sort()
print(f"combinations {combinations}")

#  details about soil MIMS
soil_mims_induced = mixs_view.induced_class('soil MIMS')
soil_mims_induced_attributes_names = [str(v.name) for k, v in soil_mims_induced.attributes.items()]
soil_mims_induced_attributes_names.sort()
print(f"soil_mims_induced_attributes_names {soil_mims_induced_attributes_names}")
# mixin and is_a parents
print(f"soil_mims is_a {soil_mims_induced.is_a}")
print(f"soil_mims mixin {soil_mims_induced.mixins[0]}")

# list of env pack classes: is_as of combinations
env_packs = list(set(isa_parents))
env_packs.sort()
print(f"env_packs {env_packs}")

#  details about soil
soil_induced = mixs_view.induced_class('soil')
soil_induced_attributes_names = [str(v.name) for k, v in soil_induced.attributes.items()]
soil_induced_attributes_names.sort()
print(f"soil_induced_attributes_names {soil_induced_attributes_names}")
# soil combinations
pprint.pprint(envs_to_combinations['soil'])

# list of other classes
other_classes = list(set(classes_names) - set(combinations) - set(checklists) - set(env_packs))
other_classes.sort()
print(f"other_classes {other_classes}")

#  details about core
core_induced = mixs_view.induced_class('core')
core_induced_attributes_names = [str(v.name) for k, v in core_induced.attributes.items()]
core_induced_attributes_names.sort()
print(f"core_induced_attributes_names {core_induced_attributes_names}")

#  details about quantity value
print(yaml_dumper.dumps(mixs_view.induced_class('quantity value')))

# list of slots
#  details about depth
print(yaml_dumper.dumps(mixs_view.get_slot('depth')))
pprint.pprint(slots_to_classes['depth'])
#  details about geo_loc_name
print(yaml_dumper.dumps(mixs_view.get_slot('geo_loc_name')))
pprint.pprint(slots_to_classes['geo_loc_name'])
#  details about ph
print(yaml_dumper.dumps(mixs_view.get_slot('ph')))
pprint.pprint(slots_to_classes['ph'])
#  details about has unit
print(yaml_dumper.dumps(mixs_view.get_slot('has unit')))
pprint.pprint(slots_to_classes['has unit'])

# list of core slot sections (abstract)
unique_abstract_slots = list(set(abstract_slots))
unique_abstract_slots.sort()
print(f"unique_abstract_slots {unique_abstract_slots}")
#  details about core field
print(yaml_dumper.dumps(mixs_view.get_slot('core field')))
print(yaml_dumper.dumps(mixs_view.slot_descendants('core field', reflexive=False)))
#  details about environment field
print(yaml_dumper.dumps(mixs_view.get_slot('environment field')))
print(yaml_dumper.dumps(mixs_view.slot_descendants('environment field', reflexive=False)))

# schema attributes
# ENUMS and PVs!

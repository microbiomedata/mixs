# geographic location (country and/or sea,region)

## slot name:
- geo_loc_name

## aliases:
- geographic location (country and/or sea,region)

## description (_definition?_)
- The geographical origin of the sample as defined by the country or
      sea name followed by specific region name. Country or sea names should be chosen
      from the INSDC country list (http://insdc.org/country.html), or the GAZ ontology
      (http://purl.bioontology.org/ontology/GAZ)

## examples:
- USA: Maryland, Bethesda

## multivalued:
- False

## parent
- [environment field](environment_field.md)

## range:
- string

## required (_may depend on usage_):
- False

## slot_uri
- MIXS:0000010

## structured pattern: 
_I have pervasively mixed this up with string serialization_
- string_serialization: '{term}: {term}, {text}'

## classes in domain:

## annotations
- expected_value: country or sea name (INSDC or GAZ): region(GAZ), specific location
        name



_show slot usage inline or as links_

## YAML Source

```yaml
  geo_loc_name:
    is_a: environment field
    title: geographic location (country and/or sea,region)
    description: The geographical origin of the sample as defined by the country or
      sea name followed by specific region name. Country or sea names should be chosen
      from the INSDC country list (http://insdc.org/country.html), or the GAZ ontology
      (http://purl.bioontology.org/ontology/GAZ)
    range: string
    multivalued: false
    examples:
    - value: 'USA: Maryland, Bethesda'
    comments: []
    aliases:
    - geographic location (country and/or sea,region)
    annotations:
      expected_value: 'country or sea name (INSDC or GAZ): region(GAZ), specific location
        name'
    string_serialization: '{term}: {term}, {text}'
    slot_uri: MIXS:0000010
```
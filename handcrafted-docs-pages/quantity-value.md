## is_a:
- [class](Classes.md)

## from schema:
- [ranges](../model/schema/ranges.yaml)

```yaml
  quantity value:
    name: quantity value
    description: used to record a measurement
    from_schema: http://w3id.org/mixs
    attributes:
      has unit:
        name: has unit
        description: Example "m"
        from_schema: http://w3id.org/mixs/ranges
        alias: has_unit
        owner: quantity value
      has numeric value:
        name: has numeric value
        from_schema: http://w3id.org/mixs/ranges
        alias: has_numeric_value
        owner: quantity value
        range: double
      has raw value:
        name: has raw value
        from_schema: http://w3id.org/mixs/ranges
        string_serialization: '{has numeric value} {has unit}'
        alias: has_raw_value
        owner: quantity value
```
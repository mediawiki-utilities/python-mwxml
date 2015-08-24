def consume_tags(tag_map, element):
    value_map = {}
    for sub_element in element:
        tag_name = sub_element.tag

        if tag_name in tag_map:
            value_map[tag_name] = tag_map[tag_name](sub_element)

    return value_map

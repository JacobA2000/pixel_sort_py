def sort_array_with_mask(arr, mask, reverse=False):
    sections = []
    current_section = []
    for i, is_sorted in enumerate(mask):
        if is_sorted:
            current_section.append(arr[i])
        else:
            if current_section:
                sections.append(sorted(current_section, reverse=reverse))
                current_section = []
            sections.append(arr[i])

    if current_section:
        sections.append(sorted(current_section, reverse=reverse))

    sorted_array = [item for section in sections for item in (section if isinstance(section, list) else [section])]
    
    return sorted_array

# Example usage:
array_to_sort = [3, 2, 7, 1, 6, 5, 4]
binary_mask = [False, True, True, True, False, True, True]

sorted_array = sort_array_with_mask(array_to_sort, binary_mask)

print("Original array:", array_to_sort)
print("Sorted array:", sorted_array)
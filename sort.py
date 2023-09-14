from PIL import Image, ImageOps

def create_contrast_mask(image, low_threshold, high_threshold):

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(image)

    # Create a binary mask where pixels within the specified range are white and others are black
    mask = gray_image.point(lambda p: 255 if low_threshold <= p <= high_threshold else 0)

    return mask

def pixel_sort(image, mask, sort_param):
    #Get image pixel data
    pixels = list(image.getdata())

    # Get the image size
    width, height = image.size

    sorted_pixels = []
    for y in range(height):
        row = pixels[y * width: (y + 1) * width]
        mask_row = list(mask.getdata())[y * width: (y + 1) * width]
        mask_row_bool = [True if pixel == 255 else False for pixel in mask_row]

        sorted_pixels += sort_array_with_mask(row, mask_row_bool)

    sorted_image = Image.new(image.mode, image.size)
    sorted_image.putdata(sorted_pixels)

    return sorted_image

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

if __name__ == "__main__":
    low_threshold = 100
    high_threshold = 200

    image = Image.open("example.jpg")

    contrast_mask = create_contrast_mask(image, low_threshold, high_threshold)
    contrast_mask.show()
    
    sorted_img = pixel_sort(image, contrast_mask, "h")
    sorted_img.show()

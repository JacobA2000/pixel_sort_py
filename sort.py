from PIL import Image, ImageOps
import colorsys

def create_contrast_mask(image, low_threshold, high_threshold):

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(image)

    # Create a binary mask where pixels within the specified range are white and others are black
    mask = gray_image.point(lambda p: 255 if low_threshold <= p <= high_threshold else 0)

    return mask

def pixel_sort(image, mask, sort_param, sort_dir):
    #Get image pixel data
    pixels = list(image.getdata())

    # Get the image size
    width, height = image.size

    sorted_pixels = []

    if sort_dir == "x":
        for y in range(height):
            row = pixels[y * width: (y + 1) * width]
            mask_row = list(mask.getdata())[y * width: (y + 1) * width]
            mask_row_bool = [True if pixel == 255 else False for pixel in mask_row]

            sorted_pixels += sort_array_with_mask(row, mask_row_bool, sort_param)

    elif sort_dir == "y":
         for x in range(width):
            col = pixels[x * height: (x + 1) * height]
            mask_col = list(mask.getdata())[x * height: (x + 1) * height]
            mask_col_bool = [True if pixel == 255 else False for pixel in mask_col]

            sorted_pixels += sort_array_with_mask(col, mask_col_bool, sort_param)

    sorted_image = Image.new(image.mode, image.size)
    sorted_image.putdata(sorted_pixels)

    return sorted_image

def sort_array_with_mask(arr, mask, sort_param):
    sections = []
    current_section = []
    for i, is_sorted in enumerate(mask):
        if is_sorted:
            current_section.append(arr[i])
        else:
            if current_section:
                sections.append(insertion_sort_hsv(current_section, sort_param))
                current_section = []
            sections.append(arr[i])

    if current_section:
        sections.append(insertion_sort_hsv(current_section, sort_param))

    sorted_array = [item for section in sections for item in (section if isinstance(section, list) else [section])]
    
    return sorted_array

def insertion_sort_hsv(arr, sort_param):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and colorsys.rgb_to_hsv(key[0],key[1],key[2])[sort_param] < colorsys.rgb_to_hsv(arr[j][0],arr[j][1],arr[j][2])[sort_param]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    return arr

if __name__ == "__main__":
    low_threshold = 50
    high_threshold = 200

    sort_param = 0 #0 - hue, 1 - saturation, 2 - brightness
    sort_dir = 'x' #x - row, y - column

    image = Image.open("example.jpeg")

    contrast_mask = create_contrast_mask(image, low_threshold, high_threshold)
    contrast_mask.show()

    sorted_img = pixel_sort(image, contrast_mask, sort_param, sort_dir)
    sorted_img.show()
    sorted_img.save("output.png")

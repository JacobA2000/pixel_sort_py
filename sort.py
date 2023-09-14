from PIL import Image, ImageOps

def create_contrast_mask_pillow(image_path, low_threshold, high_threshold):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(image)

    # Create a binary mask where pixels within the specified range are white and others are black
    mask = gray_image.point(lambda p: 255 if low_threshold <= p <= high_threshold else 0)

    return mask

# Example usage:
if __name__ == "__main__":
    # Set your desired low and high thresholds (adjust these values as needed)
    low_threshold = 50
    high_threshold = 200

    # Create the contrast mask
    contrast_mask = create_contrast_mask_pillow("example2.png", low_threshold, high_threshold)

    # Display the contrast mask
    contrast_mask.show()
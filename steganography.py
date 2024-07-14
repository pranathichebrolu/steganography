from PIL import Image

class Steganography:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        rgb = r1[:4] + r2[:4], g1[:4] + r2[:4], b1[:4] + r2[:4]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb = r[4:] + '0000', g[4:] + '0000', b[4:] + '0000'
        return self._bin_to_int(new_rgb)

    def merge(self, image1, image2):
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')

        map1 = image1.load()
        map2 = image2.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                is_valid = lambda: i < image2.size[0] and j < image2.size[1]
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if is_valid() else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2)

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j] = self._unmerge_rgb(pixel_map[i, j])

        return new_image

# Modify main function to work without argparse
def main():
    # Paths to the images
    image1_path = "image1"  # Replace with the first uploaded image file name
    image2_path = "image2"  # Replace with the second uploaded image file name
    output_path_merge = "merged_output.png"
    output_path_unmerge = "unmerged_output.png"

    image1 = Image.open("/content/a.jpeg")
    image2 = Image.open("/content/a1.jpeg")

    steg = Steganography()

    # Merge the images
    merged_image = steg.merge(image1, image2)
    merged_image.save(output_path_merge)
    print(f"Merged image saved to {output_path_merge}")

    # Unmerge the image
    unmerged_image = steg.unmerge(merged_image)
    unmerged_image.save(output_path_unmerge)
    print(f"Unmerged image saved to {output_path_unmerge}")

# Run the main function
main()

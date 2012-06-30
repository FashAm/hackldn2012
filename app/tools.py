'''
Utilities
'''
import math 

def image_entropy(im):
    """From Reddit: Calculate the entropy of an image"""
    hist = im.histogram()
    hist_size = sum(hist)
    hist = [float(h) / hist_size for h in hist]
    return -sum([p * math.log(p, 2) for p in hist if p != 0])

def square_image(im):
    """From Reddit: if the image is taller than it is wide, square it off. determine
    which pieces to cut off based on the entropy pieces.
    """
    x,y = im.size
    # if the image is taller than it is wide:
    if y > x:
        while y > x:
            #slice 10px at a time until square
            slice_height = min(y - x, 10)

            bottom = im.crop((0, y - slice_height, x, y))
            top = im.crop((0, 0, x, slice_height))

            #remove the slice with the least entropy
            if image_entropy(bottom) < image_entropy(top):
                im = im.crop((0, 0, x, y - slice_height))
            else:
                im = im.crop((0, slice_height, x, y))
            x,y = im.size
    # If the image is wider than it is tall
    else:
        while y < x:
            #slice 10px at a time until square
            slice_width = min(x - y, 10)

            left = im.crop((0, 0, slice_width, y))
            right = im.crop((y - slice_width, 0, x, y))

            #remove the slice with the least entropy
            if image_entropy(left) < image_entropy(right):
                im = im.crop((0, 0, x - slice_width, y))
            else:
                im = im.crop((slice_width, 0, x, y))
            x,y = im.size
    return im

def invalidate_static_url_cache(path):
    """
    Invalidate the entry for this path in the static url global cache (hash). This is done
    *on review* so that the image being reviewed will then be cached properly.
    """
    if path in static_url_hashes:
        del static_url_hashes[path]
"""This module should be imported by the entry-point script.

It implements the functions scan() and assemble(). The former 
is used for detecting features that are suitable for aligning 
two images. The latter proceeds to the alignment and stacking 
steps.
"""

from estare.src.align import align
from estare.src.init import examine, setup

from matplotlib import pyplot as plt
from skimage.io import imsave
from skimage.util import img_as_ubyte, img_as_uint

from pathlib import Path
import numpy as np


def scan(args):
    """Finds features that are suitable for aligning two images.

    This function shows the input image in a graph first. It then 
    goes through every pixel of it and compares its brightness with 
    a given threshold (kapa) specified by the user. If the pixel's 
    brightness is higher than or equal to the threshold, a marker 
    will be shown on that location in the graph and the user can 
    accept it as a feature by pressing any key. The pixel can 
    alternatively be discarded by a left click.

    Args:
        args : user inputs parsed by argparse
    """
    
    # handle input arguments
    image1_path = args.img1
    image2_path = args.img2
    
    info_only = args.info_only   # just check image properties and skip feature detection
    save_pixs = args.save_pxs    # save also the pixel values
    save_gifs = args.save_gif    # save the features as PNG too
    
    if (info_only):   #TODO: this feature should have a separate argument subparser
        img_as_array, x_range, y_range = examine(image1_path, verbose=True, graphics=False)
        img_as_array, x_range, y_range = examine(image2_path, verbose=True, graphics=False)
        return 
    else:
        setup()   # setup the program directory structure
        img1_as_array, x_range, y_range = examine(image1_path, verbose=False, graphics=False)
        img2_as_array, x_range, y_range = examine(image2_path, verbose=False, graphics=False)
    # Replace with:
    # img_as_array = FloatImage(imagePath)
    # img_as_array.print_info()
    # img_as_array.save()
    # x_range, y_range = img_as_array.size()

    img1_gray = img1_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale
    img2_gray = img2_as_array @ [0.2126, 0.7152, 0.0722]  
        
    # Replace with (makes FloatImage redundant):
    # imgGray = GrayImage(imagePath)
    # imgGray.print_info()
    # imgGray.save()
    # x_range, y_range = imgGray.size()

    fig2, (frame1,frame2) = plt.subplots(1, 2)
    image_features = frame1.imshow(img1_gray, cmap='gray')
    image_features = frame2.imshow(img2_gray, cmap='gray')
    selection_guide = '''Please first select two features from the left panel via left-click, and then pick their 
    counterparts (in the same order) from the right panel. Right-click to drop the latest selection. To interrupt 
    feature selection, use the middle mouse button.'''
    selection_warning='''Warning: zooming in can increase the accuracy of selection, but by doing this an 
    unwanted feature may be picked due to the mouse click action. In this case, right-click immediately after 
    zooming in to remove the unwanted selection.'''
    
    frame1.set_title(selection_guide)    
    frame2.set_title(selection_warning)
    
    plt.waitforbuttonpress(-1)
    coordinates = plt.ginput(n=4, timeout=-1, show_clicks=True)
    if len(coordinates) != 4:
        print('Feature detection incomplete. Please retry.')
    else:
        pivot_1 = [coordinates[0], coordinates[1]]
        pivot_2 = [coordinates[2], coordinates[3]]
        piv1_dest = Path.home() / 'estare_data' / 'features' / 'coordinates' / 'pivot_1.npy'
        piv2_dest = Path.home() / 'estare_data' / 'features' / 'coordinates' / 'pivot_2.npy'
        
        np.save(piv1_dest, pivot_1)
        np.save(piv2_dest, pivot_2)
        print('Feature detection completed.')
        if (save_gifs):
            feat_array = np.zeros((7,7))
            feat_gif_dir = Path.home() / 'estare_data' / 'features' / 'gifs'
            num_files = 0
            for child in feat_gif_dir.iterdir():
                num_files += 1
            print(f'Found {num_files} files.')
            suffix = num_files
            for feat_cnt in range(4):
                feat_gif_dest = feat_gif_dir / f'feat_{suffix}.png'
                y_center = int(coordinates[feat_cnt][0])
                x_center = int(coordinates[feat_cnt][1])
                feat_array[:, :] = img1_gray[int(x_center)-3:int(x_center)+4, int(y_center)-3:int(y_center)+4]
                feat_hires = img_as_uint(feat_array)
                imsave(feat_gif_dest, feat_hires)
                suffix += 1                



def assemble(args):
    """unpacks input arguments, then passes them to align() 

    This function prepares the input arguments to be passed to align() 
    for the algorithm to proceed to alignment and then stacking steps.

    Args:
        args : input arguments parsed by argparse
    """

    # TODO: design a stack-only mode that bypasses alignment
    
    # unpack the arguments
    img_1 = args.layer_1
    img_2 = args.layer_2
    skip_alignment = args.no_align
    ###subtract_frame = args.subtract_frame
    
    if not skip_alignment:
        piv1_dir = Path.home() / 'estare_data' / 'features' / 'coordinates' / 'pivot_1.npy'
        piv2_dir = Path.home() / 'estare_data' / 'features' / 'coordinates' / 'pivot_2.npy'
        
        #pivot_1 = np.load(args.anchorb)
        #pivot_2 = np.load(args.anchort)
        pivot_1 = np.load(piv1_dir)
        pivot_2 = np.load(piv2_dir)
        # align and stack the two input frames
        stacked_frame = align(img_1, img_2, pivot_1, pivot_2, save=True)

    else:
        image_1, x_range_1, y_range_1 = examine(img_1)  
        image_2, x_range_2, y_range_2 = examine(img_2)

        # if subtract_frame is None:
        image_1 += image_2
        # else:
        #     image_3, _, _ = examine(subtract_frame)
        #     image_1 += (image_2 - image_3)
            
        #TODO: accept fraction as input image_1 *= 0.5

        result_dest = Path.home() / 'estare_data' / 'stacked_images' / 'estare_overlay.jpeg'
        imsave(result_dest, image_1)
        
    print('Done')

    

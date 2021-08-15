import numpy as np
import estare.scan.feature as feature

def find_threshold(image, x_range, y_range, initial=0.5):

    threshold = initial
    numFeatures, indices, markers = feature.extract(image, xRng=[0, x_range], yRng=[0, y_range],
                                                    kapa=threshold)
    while numFeatures > 10 and threshold < 1.0:
        threshold = threshold*1.01
        numFeatures, indices, markers = feature.extract(image, xRng=[0, x_range], yRng=[0, y_range],
                                                        kapa=threshold)
    # Remove the last multiplication
    if threshold > 1.0:
        threshold = threshold / 1.01
        
    return threshold

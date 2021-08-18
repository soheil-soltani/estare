def count():
    xy_FeatureCount = 0   # number of already-saved feature coordinates initialized to zero
    binFeatureCount = 0   # number of already-saves feature images in binary format initialized to zero
    imgFeatureCount = 0   # number of already-saves feature images in .png format initialized to zero

    xy_RefusedCount = 0   # number of already-saved refused coordinates initialized to zero
    binRefusedCount = 0   # number of already-saves refused images in binary format initialized to zero
    imgRefusedCount = 0   # number of already-saves refused images in .png format initialized to zero  

    for files in os.listdir('./data/features'):
        if files.endswith('.png'):
            imgFeatureCount += 1

    for files in os.listdir('./data/features/pixels'):
        if files.endswith('.npy'):
            binFeatureCount += 1

    for files in os.listdir('./data/features/coordinates'):
        if files.endswith('.npy'):
            xy_FeatureCount += 1


    for files in os.listdir('./data/refuse'):
        if files.endswith('.png'):
            imgRefusedCount += 1

    for files in os.listdir('./data/refuse/pixels'):
        if files.endswith('.npy'):
            binRefusedCount += 1

    for files in os.listdir('./data/refuse/coordinates'):
        if files.endswith('.npy'):
            xy_RefusedCount += 1    

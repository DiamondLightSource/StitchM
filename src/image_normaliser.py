import numpy as np
import logging


def normalise_images(images, exposure_minmax, good_image_list):
    normalised_imgs = _rescale_corrected_imgs(
        _exposure_correction(images, exposure_minmax, good_image_list)
        )
    return normalised_imgs


def _image_value_trimmer(image_stack):
    new_stack = image_stack[:, :, :]
    median_std = np.median([np.std(image) for image in image_stack])
    median_median = np.median(image_stack)
    new_max = median_median + 2.5 * median_std
    return np.clip(new_stack, 0, new_max)


def _exposure_correction(images, exposure_minmax, good_image_list):
    """
    Cockpit saves some exposure min/max data which they use to
    correct exposure when displaying it. This function uses this
    to correct for the exposure.
    """
    images_min = images[good_image_list].min()
    images_max = images[good_image_list].max()
    images_range = images_max - images_min
    corrected_images = []
    for i in good_image_list:
        exp_min = exposure_minmax[i, 0]
        exp_max = exposure_minmax[i, 1]
        exp_range = exp_max - exp_min

        normalisation_coefficient = images_range / exp_range

        unbiased_img = (images[i, :, :] - exp_min) * normalisation_coefficient
        corrected_images.append(unbiased_img)
    return np.asarray(corrected_images)


def _rescale_corrected_imgs(corrected_images):
    # Trim images before correction to avoid any speckles
    # leading to the entire image to be quite dark:
    corrected_images = np.asarray(
        _image_value_trimmer(corrected_images)
        ).astype('f')  # Convert to float for rescaling
    # Move minimum value of all corrected images to 0:
    corrected_min = corrected_images.min()
    corrected_images -= corrected_min
    # Convert values to float and rescale so the maximum
    # is set by dtype (uint8):
    corrected_max = corrected_images.max()
    rescaled_images = corrected_images * (np.iinfo("uint8").max / corrected_max)

    return rescaled_images.astype("uint8")

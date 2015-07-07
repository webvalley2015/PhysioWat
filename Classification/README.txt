July 5th, 2015, 22:21

The code in this folder currently represents a combination of original and repurposed code to achieve a classification accuracy for ASD flapping motion (using decision tree on mean and variance features) of 56%. Over the next few days, we hope to refine this model by introducing new features from Riccardo in the feature extraction team.

July 8th, 2015, 10:07

The new claire_HandFlappingModes.txt is a file that contains data collected from sensor 174 (at 100Hz?) of two minutes of handflapping. The mode of movement was changed every ten seconds, with some noise at the beginning, as follows:

standing still
walking
mirrored hand flapping standing
mirrored hand flapping w/ walking
winged hand flapping standing still
winged hand flapping w/ walking
asymmetrical antidirectional hand flapping standing still
asymmetrical antidirectional hand flapping w/ walking
downward hand flapping standing still
downward hand flapping w/ walking
upward hand flapping standing still
upward hand flapping w/ walking


July 8th, 2015, 11:31

Valerie discussed with Andrea the meaning of the data in this folder. To recap, ASD.txt is data from the PhysioWAT app interface of 30 seconds of Valerie simulating hand-flapping behavior. Claire's txt file is described below. standing.txt is control data from Task 1, just for testing. 

July 8th, 2015, 10:18

Claire added a list of relevantPublications.txt, all of which are available through the ACM Digital Library. (You have to pay to get to them.) There are probably other relevant papers, but these are the ones I feel best represent what we need.

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

July 5th, 2015, 22:21

The code in this folder currently represents a combination of original and repurposed code to achieve a classification accuracy for ASD flapping motion (using decision tree on mean and variance features) of 56%. Over the next few days, we hope to refine this model by introducing new features from Riccardo in the feature extraction team.


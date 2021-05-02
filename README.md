Calculates and visualizes Neyman-Pearson tests.

An example. A florist ordered a large box of tulip bulbs. The box contains either 75% red-flowering and 25% yellow-flowering tulips, or 30% red-flowering and 25% yellow-flowering tulips. But he can't remember which. To find out, he plants 5 bulbs at random and counts how many produce red flowers. (Adapted from Howson and Urbach 2006, who cite Kyburg 1974.)

Here are the probabilities under the two hypotheses:


|         | 0    | 1    | 2    | 3    | 4    | 5    |
|---------|------|------|------|------|------|------|
| 75% red | .001 | .015 | .088 | .264 | .396 | .237 |
| 30% red | .168 | .360 | .309 | .132 | .028 | .002 |


What should the florist do after he observes the result? Neyman and Pearson answer as follows.

Before the experiment, the florist should choose a *rejection region*: a set of outcomes. If, after the experiment, the outcome is in the rejection region, the florist should reject the first hypothesis (75% red) and accept the second (30% red); else, he should reject the second and accept the first.

But which rejection region to pick? A rejection region's *size* is the probability of getting an outcome in the region, assuming the first hypothesis is true, and its *power* is the probability of getting an outcome in the region, assuming the second hypothesis is true. So our first proposal is: choose a region with low size and high power.

The function **plot_discrete_regions** plots the size and power of every rejection region:

<img src="plot_0.png">

Low size and high power pull in opposite directions. So the florist needs to trade them off. How? Region 1 dominates Region 2 if it has lower size and higher power (with at least one inequality strict). This much is clear: the florist should choose an undominated region. The Neyman-Pearson Lemma says that rejection regions which take a special form---*likelihood ratio tests*---are undominated. So our second proposal is: choose a likelihood ratio test.

The function **plot_discrete_regions_plus** shows which regions are undominated (blue blobs) and which regions are likelihood ratio tests (big blobs). (Note that all big blobs are blue, by the Neyman-Pearson Lemma, but the converse is false.)

<img src="plot_1.png">

Still, there are multiple likelihood ratio tests. Can we give the florist more specific advice? This leads to the third proposal: Choose a maximum acceptable size. Among likelihood ratio tests of at most that size, choose the one with the highest power.

The function **which_region** shows this proposal in action:

<img src="plot_2.png">

The red line is the maximum acceptable size. The black blob is the region selected according to our third proposal.

The functions **print_discrete_regions** and **print_discrete_regions_plus** print the data instead of plotting it.
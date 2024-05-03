# laser beam properties



1. Project Overview

In this project, I will process an image of a laser beam to measure the size and position of the beam. In laser labs, we often need to know in detail the laser beam characteristics (think of the shape of the beam of a laser pointer on a screen): what is the beam size? Is it nice and round, or elongated? Has it moved? All of these properties can have strong effects on our experiments, and also tell us whether there are problems with the laser. In order to track all of these, it is common to directly image the laser beam – send a small portion of the beam to a camera, so that the image taken shows the laser beam shape. Where there is more light the image will be brighter etc. But since we care about changes of the beam that are hard to track by eye, we need to characterize the beam shape (called “beam profile”) in a quantitative way; We do that by fitting a known function – a 2D Gaussian – to the imaged beam shape, and tracking the relevant quantities resulting from the fit. In this project, I will process real data taken from my a lab and use code as a tool in the same manner that researchers do on a daily basis . 
The code is going to take an image file and the optical system parameters as an input, and output to a .txt file a measurement of the beam size, as well as various plots related to the measurement.

2. Background

2.1 Laser beam shape

Real laser beams tend to have a Gaussian shape in space, i.e. if you project the beam onto a screen or into a camera, the amount of light that reaches each point in space will form a two-dimensional Gaussian.

I(x, y) = C * e^(-((x-x_0)^2 / (2*sigma_x^2))) * e^(-((y-y_0)^2 / (2*sigma_y^2))) + B

Here 'x' and 'y' mark the position in space on a plane the laser hits, like a screen or a camera sensor. 'x_0' and 'y_0' are the positions of the center of the beam, 'sigma_x' and 'sigma_y' are the widths of the Gaussians in their respective axes. 'C' is a constant that is proportional to the total amount of light. 'B' is a background level, and in general is a positive shift above the zero line.

The Gaussian shape is maintained over each axis independently:

I(x) = ∫ dy I(x, y) = C' * e^(-((x-x_0)^2 / (2*sigma_x^2))) + B'

and the same for I(y).

2.2 The data

In this project I work with an image of the laser beam - it will contain a measurement of the amount of light that reaches each point on the camera sensor.

counts[n, m] = I(x = (n / Pixels in x) * L_x, y = (m / Pixels in y) * L_y)

Where 'n' and 'm' are the pixel indices, 'Pixels in x/y' are the number of pixels in each axis, and 'L_x' and 'L_y' are the dimensions of the sensor. Each pixel will only contain a single number, the count, proportional to the amount of light, without any color information. Below you can see an example of such an image of a laser beam cross-section.

As you can maybe already see in this image, real data is dirty. The beam is not a perfect 2D Gaussian. This becomes clearer when looking at a one-dimensional plot of counts vs. x position. Here, in order to get a 1-D graph from the 2-D image, we summed over the y-axis:

counts_x[n] = ∑_{m=0}^{NyPixels} counts[n, m]

2.3 Fitting a function to data

There are various mathematical approaches to fit a function to data. The basic concept is to start with a function that should match the data (based on some prior knowledge, such as a theoretical explanation) and adjust some free parameters of the function until the “distance” between the data and the calculation according to the function is minimized. In this project you will use a fitting procedure that is already implemented in Python (you do not need to write it yourself).

In our case, the function is a 1-D Gaussian, the parameters are the amplitude 'C'', the position 'x_0', and the width 'sigma_x'. In principle, one could fit directly the 2D Gaussian. But fitting over a one-dimensional Gaussian is easier and more reliable. In addition, summing over the other axis reduces the noise in the data.

2.4 Pointing stability

The position of the beam moves over time due to a variety of reasons such as effects of temperature change, vibrations, air currents, and construction work on a floor above the lab while we are trying to take very precise measurements. The name for this property is Pointing Stability. To quantify it we take a series of images over time, measure the position of the beam in each image using a fit and then calculate the root mean square (RMS) of the results we have obtained. The RMS of the position is defined below:

x_RMS = sqrt((1/N) * Σ(i=0 to N)((x_i - x̅)^2))

Here 'N' is the number of measurements, 'x_i' is the position of the 'i'th measurement, and 'x̅' is the average of the 'x' position in all measurements. Similarly, you can calculate the RMS for the movement in the y-axis by replacing 'x' with 'y'.

This can be calculated also for the radial distance, i.e., the distance of each measurement from the average position defined by:

r_i = sqrt((x_i - x̅)^2 + (y_i - y̅)^2)

Giving us the RMS in 'r':

r_RMS = sqrt((1/N) * Σ(i=0 to N)(r_i^2))

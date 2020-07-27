GUI looks great! a few issues below to iron out, but really exciting to see 
it in such good shape - a real program!

**1. Error message when running with filter**

When using the following parameters: Filtering = Gausian blur sigma 3px, everything
ran as expected and produced .csv files as an output. 

The following error message was thrown however: 

> C:\Users\jdeed\Desktop\2020-07-27 unzip three-d-distance-analyser-master\pydist3d\main.py:221: 
> 
> UserWarning: Values in mask2[slices]: [False  True] warnings.warn(f"Values in mask2[slices]: {np.unique(mask2[slices])}")

What does this message mean/is it possible for us to supress it if it is not 
providing anything informatitve?

**2.  'None' as Filtering option does not run**

When selecting 'None' as the 'Filtering' option (alongside 'otsu' as the thresholding
method, the program did not run and the following error message was thrown. 

> Traceback (most recent call last):
>   File "C:\Users\jdeed\Desktop\2020-07-27 unzip three-d-distance-analyser-master\scripts\run_gui.py", line 219, in <module>
>     main()
>     
>   File "C:\Users\jdeed\Desktop\2020-07-27 unzip three-d-distance-analyser-master\scripts\run_gui.py", line 214, in main
>     threshold_method=settings["threshold_method"],
>     
>   File "C:\Users\jdeed\Desktop\2020-07-27 unzip three-d-distance-analyser-master\pydist3d\main.py", line 278, in main
>     threshold_method=threshold_method,
>     
>   File "C:\Users\jdeed\Desktop\2020-07-27 unzip three-d-distance-analyser-master\pydist3d\main.py", line 255, in batch
>     threshold_method=threshold_method,
>     
>   File "C:\Users\jdeed\Desktop\2020-07-27 unzip three-d-distance-analyser-master\pydist3d\main.py", line 113, in process_file
>     filtered1 = perform_filter_using_method(channel1, filter_method)
>     
>   File "C:\Users\jdeed\Desktop\2020-07-27 unzip three-d-distance-analyser-master\pydist3d\main.py", line 48, in perform_filter_using_method
>     raise ValueError(f"Filter method [{method}] not supported")
>     
> ValueError: Filter method [none] not supported

**3. Slice selection for object detection check** 

I noted that you added a parameter in the python module to specify the slice that
to show the overlay of object detection against the original image for the user
to check the effectiveness of the object detection. I think this should be added
to the GUI as well. 

**4. Channel numbering**

This is a minor point, but as the GUI is geared towards the non-pythonic analyist,
it might be worth changing the channel selection so that the first channel selected
with the number '1' as opposed to '0' (and so on). 

Currently the selection goes up to 2 (allowing for images with 3 channels to be
analysed with the GUI), while this will work for most immunofluoresence images,
I think we should either increase the number of possible channels to '6' (overkill)
or perhaps simply require the analyist to enter their channel number without 
selecting from a list - whichever is easiest. 

**5. Distance descriptions**

This is another minor point that applies to both the GUI and the python module,
in the stats_table output, the names should be changed to match the descriptiosn
we are using in the upcoming paper. 

'min Distance' -> 'Edge to Edge'
'max Distance' -> 'Hausdorff Distance'
'mean Distance' -> 'PD<sub>mean</sub>'

A median ('median distance' -> 'PD<sub>median</sub>') and sum ('sum distance' -> PD<sub>sum</sum>))
of the PD measurements is 
also currently included, I personally do not see much value in these measurements:

The median measurement (PD<sub>median</sub>) is much the same as the mean measurement 
but doesn't pay as much attention to pixels in the perimeter of the object
with large distances to the nearest signal in neighbouring channel - this I argue
makes it a less effective measurement. 

The sum measurment is almost entirely uninformative as it depends largely on the
size of the object being measured. 

Finally, the 'total number of bacterial perimeter pixels' measurement should
be renamed to 'Number of Perimeter Pixels in Object' to make it more widely applicable
to all users. 


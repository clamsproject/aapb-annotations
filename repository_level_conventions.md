# Repository-level Conventions
> TL;DR  
> Media Time = `hh:mm:ss.mmm` with a **DOT**   
> Annotations are usually a little imprecise because audiovisual phenomena are, or visualizing/labelling of such is. 
> Some estimates of imprecision are given by Margin of Error.
> Directionality definitions help frame the boundaries meant by annotated times.

### Time Point Notation
> [!IMPORTANT]
> `hh:mm:ss.mmm` with a **DOT**  

The time format for all (gold) datasets in this repository is [ISO 8601 Time Format](https://en.wikipedia.org/wiki/ISO_8601#Times). 
Specifically, with time precision of up to hours and down to milliseconds placed after seconds with a **DOT**, where `00:00:00.000` means the very beginning of a time-based media (not midnight real-time).  
This instruction is specifically to be  required for the "gold" data formats throughout this repository, except where exceptions are required and documented.  
(_TODO: Current/Old gold datasets and tools have yet to be converted._)  
During raw annotation however, the tool environments may use different time formats because of non-in-house authors. 
Moving forward, the expectation for any in-house tools and apps are to use this standard. 
If configurable, the annotation tool should be configured to use this format. If possible, the annotator should also be instructed to use this format.  
For MPEG-based video files, frame numbers are converted to milliseconds with loss of precision past 3-digits. 
However, due to exact time -> still-image-fetching being dependent on the video compression/codec/player, there is no expected need for precision past 3-digits. 
It is assumed that different video players will regenerate images on screen slightly differently based on the decompression algorithms. 
To that end, it is unlikely that even given a specific time moment that a person in one place would be able to extract exactly the same pixels 
in a frame as another person doing it somewhere else.  
The other reason frames was not chosen to divide seconds is that the collection also contains radio assets with audio only. Audio does not have frames.  
### Imprecision in Annotation in General
Data Quality processes are currently still being built. Currently, datasets do not have a data quality checklist applied to them. 
This means there are possible typos in anything that must be typed. Other general data messiness is also possible. 
Two semi-preventative measures are: 
1. If only a few value options are expected in one column, using a pie chart/counter in Excel to search/count for typos to manually correct is possible. 
2. Annotators should use copy-paste wherever possible instead of typing, and annotation tools should have buttons to add items, 
reducing typos during typing.  

The current convention is that annotators are asked to be as careful as meaningfully possible, and some datasets are "quality-assumed" upon 
faith in annotators/environment until such time a quantitative analysis of errors is done.  

### Imprecision in Time-based Annotation
Time-based annotations are almost inherently imprecise. This is due usually to either perception or manipulation of the tool within the limits of meaningful
task-speed constraints are at hand. 
Furthermore, the features of audiovisual materials do not always have clear-cut beginning and end points.    
The conventions in place attempt to provide clarity for when generally the annotations can be considered precise or not. 

1. **MARGIN OF ERROR** _(+/- in both directions)_- 
The margin of error depends on the process of how an annotation project was conducted and the tool used. 
For instance, 
if the annotator is playing a video at half speed (audio listenable) and pressing a button when a chyron appears (and not stopping to correct or precisely verify), we can assume:
   1. Precision is limited by on-screen-and-discern-to-press [reaction time](https://www.reddit.com/r/truegaming/comments/hu0p3a/comment/fylge12/?utm_source=reddit&utm_medium=web2x&context=3),
which is approximately .200 to .250 seconds. This time amount is somewhat similarly shown in feedback from musicians using digital keyboards and video gamers complaining about [ping or framerate](https://www.pcgamer.com/how-many-frames-per-second-can-the-human-eye-really-see/).
   2. As an assumption, if the video is playing at half speed, we can then assume the margin of error from this factor is approximately 0.100-0.200 seconds. 
   3. Being able to pause and visually move a time slider with high precision would increase the precision but likely lead to excessive annotation labor cost. 
   4. It is highly likely there will be cases where margin of error will pass over the Directionality limit given below. 
However, the convention requested during annotation is to attempt to preserve **Directionality** instructions over reducing **Margin of Error**.   
  
2. **DIRECTIONALITY** _(as close to a certain boundary but not past it)_ - We attempt to give instructions and explanation for when we want 
an annotation to be up to the limit of something as close as possible. 
There are times when a project requires one thing to be the superinterval and times when other projects require the other way around. (See 3rd point.)   
   1. E.g. Let's say we are annotating a fading-in-and-out chyron. 
   We want the start time of the chyron to be "as close as possible but after" the moment when the chyron is fully solid and no longer transparent.
   And we want the end time of the chyron to be "as close as possible but before" the moment when the chyron begins to start fading-out. 
   Here are two ways to describe one Directionality convention: 
      1. **Instructions for human annotators** - For time-based media, annotated times are to be labeled as within the duration of the phenomenon.
   Eg. if a text-based label fades on-and-off screen, 
   the annotated start time should be the moment it has become fully solid and the end time should be the moment just before it begins to fade.  
      2. **Interpreting [MMIF](https://github.com/clamsproject/mmif) or annotations** - For time-based media, assume that the interval defined in the MMIF annotation is contained within the relevant interval in the actual media.  
3. **SUPERINTERVAL/SUBINTERVAL/SUPERSET** - Another way to explain Directionality -  
This explanation originates from the mathematical terms "superset" and "subset", where if groupA is a "superset" containing groupB,
then that means that groupA wholly contains the bounds of groupB.  
So, if an annotated time interval label with a start and end time (as is above) is wholly within the time where 
a phenomenon (e.g. a chyron) appears, then the annotation is considered a subinterval of the phenomenon.  
i.e. The phenomenon is a superinterval to the labeled time.  
i.e. Any time given by the annotated time interval of the chyron should return an image of the chyron being present in the media at that time.   

Finally, a reminder that at 30 frames per second, each frame is 0.033_ seconds long - meaning a tenth of a second has 3 frames within it.
Practically speaking, there is only a small percentage of cases where the variation between one frame to its neighbor is relevant,
especially in cases of human perception.
The conventions for precision hold until new needs of the project are required. 
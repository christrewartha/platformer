# PyGame Platformer

Followed the tutorial from "Clear Code" on YouTube: https://www.youtube.com/playlist?list=PL8ui5HK3oSiGXM2Pc2DahNu1xXBf7WQh-

Some of the code seemed a bit messy to me so started tidying up.
- Moved the tiles into their own files
- Standardised the code for creating/updating tiles and simplified the "level" class
- Added some easing functions and simplified the "overworld" class

Looking at the code a bit more, I don't love the way the scrolling is done. The player movement is also a bit basic, and the two are tied together in a strange way (when the player reaches the edge of the screen, their speed is set to zero and the scrolling speed is set to 8 - the max player speed).

I think I'll implement some motion which has a bit more intertia/momentum, then look at splitting out the movement and scrolling logic. I don't think game objects should care what the camera is looking at.

Nice to discover "Tiled" by following this tutorial!
 

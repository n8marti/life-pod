## Emulate other screens

model | size | resolution | dpi | density | -m screen: 
:-- | --: | --: | --: | --: | :--
laptop | 14in | 1920x1080 | 157 | 1.0 (157/160)
Samsung Galaxy A13 | 7in | 2408x1080 | 377 | 2.35
Samsung Galaxy Tab A10 | 8in | 1280x800 | 148 | 1.0 | tablet_samsung_galaxy_tab_10
Samsung Galaxy Tab A10.1 | 8in | 1920x1200 | 241 | 1.5
Samsung Galaxy Tab A7 Lite | 8.75in | 1340x800 | 178 | 1.0

# using `screen` module (emulates pre-defined devices)
```shell
python -m src.life_pod -m screen:tablet_samsung_galaxy_tab_10[,scale=1]
```
However, this module automatically reduces the height for the android bar,
which is not necessarily helpful:
```python
# kivy/modules/screen.py L136-139
# ...
    Config.set('graphics', 'width', str(int(width * scale)))
    # simulate with the android bar
    # FIXME should be configurable
    Config.set('graphics', 'height', str(int(height * scale - 25 * density)))
# ...
```

# using environment variables
```shell
KIVY_DPI=NNN KIVY_METRICS_DENSITY=N.N python -m src.life_pod --size=NNNNxNNNN
```
To scale output the env variables must be scaled together.

## Kivy metrics
https://kivy.org/doc/stable/api-kivy.metrics.html
We provide some environment variables to control metrics:

- `KIVY_METRICS_DENSITY`: if set, this value will be used for density instead of the systems one. On android, the value varies between 0.75, 1, 1.5 and 2.
- `KIVY_METRICS_FONTSCALE`: if set, this value will be used for fontscale instead of the systems one. On android, the value varies between 0.8 and 1.2.
- `KIVY_DPI`: if set, this value will be used for dpi. Please note that setting the DPI will not impact the dp/sp notation because these are based on the screen density.

## Kivy density
https://kivy.org/doc/stable/api-kivy.metrics.html#kivy.metrics.MetricsBase.density
density: float
- The density of the screen.
- This value is 1 by default on desktops but varies on android depending on the screen.

## Android "logical DPI factors"
https://en.wikipedia.org/wiki/Pixel_density > Logical DPI Values on Android
> These seem to be what Kivy is referring to as "density".

# Logical DPI values on Android
Android supports the following logical DPI values for controlling how large content is displayed:
Name | Full name | Scale factor | DPI
:-- | :-- | --: | --:
ldpi | Low DPI | 0.75x | ~120
mdpi | Medium DPI | 1x | ~160
tvdpi | TV DPI | 1.33x | ~213
hdpi | High DPI | 1.5x | ~240
xhdpi | Extreme high DPI | 2x | ~320
xxhdpi | Extreme x2 high DPI | 3x | ~480
xxxhdpi | Extreme x3 high DPI | 4x | ~640

# Designing for different pixel densities
https://developer.android.com/training/multiscreen/screendensities

To preserve the visible size of your UI on screens with different densities, design your UI using density-independent pixels (dp) as your unit of measurement. One dp is a virtual pixel unit that's roughly equal to one pixel on a medium-density screen (160 dpi, or the "baseline" density). Android translates this value to the appropriate number of real pixels for each other density.

Convert dp units to pixel units
In some cases, you need to express dimensions in dp and then convert them to pixels. The conversion of dp units to screen pixels is as follows:
```
px = dp * (dpi / 160)
```
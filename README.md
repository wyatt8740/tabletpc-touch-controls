# Tablet PC Touch/Stylus Controls

This is an applet I made to house functions I regularly use with my ThinkPad
X201 when it is switched into it's tablet orientation.

## Why?

Since Lenovo unfortunately deemed it prudent to axe the four directional
buttons seen on the bezel of the X61 and X60 tablet models, I only have four
buttons usable (plus the power button, I suppose, if I wanted to remap it)
when my tablet is being used as a tablet instead of as a laptop.

Unfortunately, I already had more than four functions I wished to use in tablet
mode on day one! These include:

1. Toggling the touch screen digitizer portion on and off (so I can rest my
palm, hand, and/or wrist on the screen while using the stylus)
2. Flipping the screen upside down
3. Alternating between portrait and landscape modes
4. Making an on-screen keyboard appear/disappear
5. Adjusting display brightness up
6. Adjusting display brightness down
7. Switching between windows in FVWM without having a window list bar
constantly take up precious space

Some of these are mapped directly to the keys on the bezel; however, I reserved
one so that I could make a software menu to supplement the list of actions.

After not finding much in the way of tools that can do this for unix systems
(possibly because I don't know what to search for?), I rolled my own ugly
python thing. I am not really a Python programmer at heart, but it seemed
the easiest way to get a somewhat cross-platform UI going (something that
doesn't require FVWM to be in use).

## Problems
...Oh, so many problems. Where to start?

* It currently doesn't float on top unless your window manager is configured
so that it stays on top.
   * This might be something I can fix with a WM hint, but I've not read
   through the documentation enough to find out how (or if) I can do that via
   Python 3's GTK3 library, or if I'll need to use XCB stuff. Since I can do
   this via fvwm's config file on my system, it wasn't necessary for my
   initial prototype, which is what this code drop represents as of now.
   * If using FVWM, my config contains the following rules:

```
Style TabletPC_Applet_Menu NeverFocus, StaysOnTop, Sticky, !Button 4, !Button 2, !Button 1, !Borders
```

* Not every action has an icon
   * Since I am drawing all of the icons myself, and that takes time, I haven't
   drawn all of the icons for all of the actions yet. It's especially time
   consuming since I decided (for some reason I'm not even sure of) to manually
   redraw all the icons at 16x16 px, like how Microsoft did in the old days for
   it's operating systems. I really don't know if there are any tablets with
   DPI low enough for 16x16 px to make sense, even, but some of the icons
   themselves might be re-usable in other places or projects.
* Hardcoded stuff all over the scripts that I run
   * I've included the scripts in this code drop that I use, but they are all
     pretty much hardwired for my system. No attempt has yet been made to
     make them more portable. There may be hardcoded paths and other
     assumptions made. In fact, some of the scripts might even use Korn Shell
     instead of bash. I've not checked recently, and I do enjoy using ksh
     sometimes.
* Just generally not ready for production
   * I'm mainly putting it online so I don't lose it and have to recreate it.

If you find a use for it or want to fix it up, go right ahead. I might do that,
too, if time allows, but right now I'm pretty swamped with school work.

## Licensing

All images are currently my own work, and are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)
(Creative Commons Attribution-ShareAlike).

I have decided to license this software under the terms of the commonly used
MIT license, which I have reproduced below:

> Copyright 2019 Wyatt Ward.
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

# Ninja-Run
**Ninja Run 🥷🏃🏻‍♂️‍➡️ game using Kivy - Python**

This is an implementation for Ninja Run(like Dinosaur offline game on chrome) for a ninja running and avoiding obsacles 𖣘 as my third project in my "How many projects you can do in your last semster" challenge

# Make APK for Kivy

Follow this tutorial : https://www.youtube.com/watch?v=WQ0oNpsTJus&t=223s

with this notebook: https://colab.research.google.com/gist/kaustubhgupta/0d06ea84760f65888a2488bac9922c25/kivyapp-to-apk.ipynb

and here is a template for the spec file so you don't search alot as it takes alot to give you an output so you won't like to restart it alot (like i did🫣):
```
[app]
title = Appname
package.name = appname
package.domain = org.kivy
source.dir = .
source.include_exts = py, kv, png, jpg
version = 1.0
requirements = python3, kivy, #(all modules need to install)
android.permissions = INTERNET #optional
android.api = 33
android.minapi = 21
android.fileprovider = True
orientation = landscape #according to your app

[buildozer]
log_level = 2
warn_on_root = 1
```

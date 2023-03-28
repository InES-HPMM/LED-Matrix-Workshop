# Anleitung für das Erstellen von Pixel-Art

Mir dem Pixel-Art Modul können 8x8 Pixel grosse Bilder auf der LED-Matrix angezeigt werden. Die Bilder
können als Bitmap-Datei (.bmp) auf den Pi-Pico geladen werden. Die Bitmaps können ganz einfach mit einem
Online-Tool erstellt werden. Folgend findest du eine kurze Anleitung, wie du Bilder für die LED-Matrix 
zeichnen und auf den Pi-Pico laden kannst:

1. Gehe auf die Website JS Paint. Dies ist ein einfaches Online-Tool um Bilder zu zeichnen. (https://jspaint.app/)
2. Die Sprache kann unter "Extras" -> "Language" geändert werden.
3. Klicke oben auf "Images" und dann auf "Attributes". Du kannst hier die Grösse des Bildes auf 8 x 8 Pixel ändern.
![image_attributes](https://github.zhaw.ch/storage/user/5715/files/eaee0a74-066f-4564-b8f3-237429afb343)
![image_size_pixel](https://github.zhaw.ch/storage/user/5715/files/b226527c-4c51-4e76-bf92-03c85686b4b2)

4. Das Bild ist nun sehr klein. Klicke oben auf "View" dann auf "Zoom" und dann auf "Zoom to window".

![image_zoom](https://github.zhaw.ch/storage/user/5715/files/5d84edf9-6035-4001-8a59-2fcb023d6a52)


5. Nun sollte das Bild wieder gross sein. Du kannst nun dein Bitmap zeichnen. Die Farbpalette ist unten Links.

![Farbpalette](https://github.zhaw.ch/storage/user/5715/files/a7e71bb2-9f55-4824-bb66-7e1eeb65cbd3)


6. Um selber eine Farbe zu erstellen, mache einen Doppelklick auf die Farbpalette und wähle "Define Custom Colors".

![custom_color](https://github.zhaw.ch/storage/user/5715/files/3d1319ff-d2a8-40e0-8008-0d56f311cb3b)


7. Wenn du die Farbe erstellt hast, klicke auf "Add To Custom Colors".

![add_custom_color](https://github.zhaw.ch/storage/user/5715/files/c01f15b4-a792-40fa-a47b-69bf3ed94c74)


8. Wenn du mit dem Bild fertig bist, Klicke oben auf "File" und dann auf "Save As".

![save_as](https://github.zhaw.ch/storage/user/5715/files/0e700054-005a-4467-8edc-875c72c71351)


9. Speichere das Bild als 24-Bit Bitmap.

![24_bitmap](https://github.zhaw.ch/storage/user/5715/files/113b9cf3-717e-4f50-b845-838f68744c72)


10. Dieses Bild kannst du so nun auf dem Raspberri Pi Pico abspeichern und verwenden. 

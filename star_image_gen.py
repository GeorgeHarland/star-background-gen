from zipapp import ZipAppError
import PIL
from PIL import Image
from random import randint
import pandas as pd
from io import BytesIO
import zipfile

# stars
INDEX_START = 1 
COUNT = 50 

print("Generating " + str(COUNT) + " stars.")

# load images
bg_img = Image.open("dark_blue_bg_1024.png").convert("RGBA")
star_img = Image.open("star_104.png").convert("RGBA")

# other vars
star_count = []
zipa = zipfile.ZipFile('stars.zip', 'w', zipfile.ZIP_DEFLATED)

for c in range(COUNT):
    render_img = bg_img.copy()
    stars_in_file = randint(0,50)
    star_count.append(stars_in_file)
    for i in range(stars_in_file):
        angle = randint(0,360)
        star_size = randint(30,100)
        temp_star = star_img.resize((star_size, star_size), resample=PIL.Image.Resampling.LANCZOS)
        temp_star = Image.Image.rotate(temp_star, angle, expand=True) # ,resample=PIL.Image.BICUBIC,expand=True

        x = randint(-int(temp_star.width/2),bg_img.width - int(temp_star.width/2))
        y = randint(-int(temp_star.height/2),bg_img.height - int(temp_star.height/2))

        render_img.paste(temp_star, (x, y), temp_star)

    image_file = BytesIO()
    render_img.save(image_file, 'PNG')
    zipa.writestr(f'stars-{c+INDEX_START}.png', image_file.getvalue())

df = pd.DataFrame( {'id':range(INDEX_START,len(star_count)+INDEX_START),'clip_count':star_count})
zipa.writestr('master.csv', df.to_csv(index=False))
zipa.close()
print("done")

df

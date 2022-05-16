# APOD Viewer
import tkinter
import requests
import webbrowser
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from io import BytesIO
from constants import API_KEY

# define window
root = tkinter.Tk()
root.title('APOD Viewer')
root.iconbitmap('rocket.ico')

# define fonts n colors
text_font = ('Time New Roman', 14)
nasa_win = '#758BFD'
nasa_btn = '#AEB8FE'
nasa_exit = '#FF8600'
nasa_bg = '#ffffff'
root.config(bg=nasa_win)

# define functions


def get_request():
    '''get request data from NASA APOD API'''
    global response

    # set the parameter for the request
    url = 'https://api.nasa.gov/planetary/apod'
    api_key = API_KEY  # use your own api key
    date = calendar.get_date()
    querry_string = {'api_key': api_key,  'date': date}

    # call the request n turn it into a python usable format
    response = requests.request('GET', url, params=querry_string)
    response = response.json()

    # update output labels
    set_info()


def set_info():
    '''update output labels based on API call'''

    # example response
    '''{'copyright': 'U. Mishra', 'date': '2021-03-01', 'explanation': 'The Pelican Nebula is changing.   The entire nebula, officially designated IC 5070, is divided from the larger North America Nebula by a molecular cloud filled with dark dust.  The Pelican, however, is particularly interesting because it is an unusually active mix of star formation and evolving gas clouds.  The featured picture was processed to bring out two main colors, red and blue, with the red dominated by light emitted by interstellar hydrogen. Ultraviolet light emitted by young energetic stars is slowly transforming cold gas in the nebula to hot gas, with the advancing boundary between the two, known as an ionization front, visible in bright red across the image center. Particularly dense tentacles of cold gas remain.  Millions of years from now this nebula might no longer be known as the Pelican, as the balance and placement of stars and gas will surely leave something that appears completely different.   APOD in world languages: Arabic, Bulgarian, Catalan, Chinese (Beijing), Chinese (Taiwan), Croatian, Czech, Dutch, Farsi, French, German, Hebrew, Indonesian, Korean, Montenegrin, Polish, Russian, Serbian, Slovenian,  Spanish, Taiwanese, Turkish, Turkish, and  Ukrainian', 'hdurl': 'https://apod.nasa.gov/apod/image/2102/Pelican_PetraskoEtAl_3555.jpg', 'media_type': 'image', 'service_version': 'v1', 'title': 'The Pelican Nebula in Red and Blue', 'url': 'https://apod.nasa.gov/apod/image/2102/Pelican_PetraskoEtAl_960.jpg'}'''

    # update the picture date n explanation
    picture_date.config(text=response['date'])
    picture_exp.config(text=response['explanation'])
    picture_title.config(text=response['title'])

    # we need to use 3 images in other functions, an image(img), a thumbnail(thumb) and a full image(full_img)
    global img
    global thumb
    global full_img
    url = response['url']

    if response['media_type'] == 'image':
        # grab the photo that is in our response
        img_response = requests.get(url, stream=True)

        # get the content of the response n use BytesIO to open it as an Image
        # keep a reference to this img as this is what we can use to save the image (Image not PhotoImage)
        # create the full screen image for a second window
        img_data = img_response.content
        img = Image.open(BytesIO(img_data))
        full_img = ImageTk.PhotoImage(img)

        # create the thumbnail for the main screen
        thumb_data = img_response.content
        thumb = Image.open(BytesIO(thumb_data))
        thumb.thumbnail((200, 200))
        thumb = ImageTk.PhotoImage(thumb)

        # set the thumbnail image
        picture_label.config(image=thumb)

    elif response['media_type'] == 'video':
        picture_label.config(text=url, image='')
        webbrowser.open(url)


def full_photo():
    '''open the full size photo in a new window'''
    top = tkinter.Toplevel()
    top.title('Full APOD Photo')
    top.iconbitmap('rocket.ico')

    # load the full image to the top window
    img_label = tkinter.Label(top, image=full_img)
    img_label.pack()


def save_photo():
    '''save the desired photo'''
    save_name = filedialog.asksaveasfilename(
        initialdir='./', title='Save Image', filetypes=(('JPEG', '*.jpg'), ('All Files', '*.*')))
    img.save(save_name + '.jpg')


# define layouts
# create frames
input_frame = tkinter.Frame(root, bg=nasa_win)
output_frame = tkinter.Frame(root, bg=nasa_bg)
input_frame.pack()
output_frame.pack(padx=50, pady=(0, 25))

# layout for the input_frame
calendar = DateEntry(input_frame, width=10, font=text_font,
                     background=nasa_win, foreground=nasa_bg)
submit_button = tkinter.Button(
    input_frame, text='Submit', font=text_font, bg=nasa_btn, command=get_request)
full_button = tkinter.Button(
    input_frame, text='Full Photo', font=text_font, bg=nasa_btn, command=full_photo)
save_button = tkinter.Button(
    input_frame, text='Save Photo', font=text_font, bg=nasa_btn, command=save_photo)
quit_button = tkinter.Button(
    input_frame, text='Exit', font=text_font, bg=nasa_exit, command=root.destroy)

calendar.grid(row=0, column=0, padx=5, pady=10)
submit_button.grid(row=0, column=1, padx=5, pady=10, ipadx=35)
full_button.grid(row=0, column=2, padx=5, pady=10, ipadx=25)
save_button.grid(row=0, column=3, padx=5, pady=10, ipadx=25)
quit_button.grid(row=0, column=4, padx=5, pady=10, ipadx=50)

# layout for output_frame
picture_title = tkinter.Label(output_frame, font=text_font, bg=nasa_bg)
picture_date = tkinter.Label(
    output_frame, font=text_font, bg=nasa_bg)
picture_exp = tkinter.Label(
    output_frame, font=text_font, bg=nasa_bg, wraplength=600)
picture_label = tkinter.Label(output_frame)

picture_title.grid(row=0)
picture_exp.grid(row=1, column=0, padx=10, pady=10, rowspan=2)
picture_date.grid(row=2, column=1, padx=10, pady=10)
picture_label.grid(row=1, column=1, padx=10, pady=10)

# load the info of current day at start
# get_request()

# run the root windows main loop
root.mainloop()

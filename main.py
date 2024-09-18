import discord
import random
from discord.ext import commands
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def snaky(path):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r", encoding="UTF-8").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]
    print(class_name)
    if class_name == "0 Главная дорога":
        return("это дорога с преимущественным (приоритетным) правом проезда по отношению ко второстепенным дорогам, пересекающим главную дорогу или примыкающим к ней.")
    elif class_name == "1 кирпич":
        return("Это Въезд запрещен")
    elif class_name == "2 стоп":
        return("Знак «Движение без остановки запрещено» (СТОП, STOP) — это дорожный знак приоритета, предписывающий водителям совершить обязательную кратковременную остановку перед стоп-линией, а если её нет — перед краем пересекаемой проезжей части.")
    elif class_name == "3 скорость":
        return("это установление допустимой максимальной скорости, с которой транспортные средства могут двигаться по данному участку дороги.")
    else:
        return("это участок проезжей части или трамвайных путей, обозначенный дорожными знаками «Пешеходный переход» и (или) дорожной разметкой («зебра») и выделенный для движения пешеходов через дорогу.")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    for img in ctx.message.attachments:
        number = random.randint(0, 100000000000000)
        await img.save (f'foto{number}.jpg')
        await ctx.send(snaky(f'foto{number}.jpg'))
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

bot.run("Token")
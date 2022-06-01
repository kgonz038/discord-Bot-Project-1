import os
import discord
from discord.ext import commands
from discord.ext.commands import bot
import requests

# bot = discord.Client()

# commands are executed if there's a ! in front
bot = commands.Bot(command_prefix='!')

# api key from openweathermap.org
api_key = os.environ['api']
base_url = "http://api.openweathermap.org/data/2.5/weather?"


# confirmation that the bot is running
@bot.event
async def on_ready():
    print('We have connected as {0.user}'.format(bot))


# this command function displays the pdf version of the discounted days to be downloaded
@bot.command(pass_context=True)
async def PDF(ctx):
    await ctx.send(file=discord.File('SATX-WEEK-BOT.pdf'))


# This weather command displays the current weather, temp, humidty and wind speed in San Antonio only
@bot.command(pass_context=True)
async def weather(ctx):
    city = str("San Antonio")
    city_name = city

    # different weather description cases to display corresponding current images
    rain_string = "rain"
    thunder_string = "thunder"
    cloudy_string = "cloud"
    snow_string = "snow" or "hail"
    clear_string = "clear" or "sun"

    # uses the weather website url and the api key while also appending the city name (san antonio) in order to receive the weather data
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)
    x = response.json()

    channel = ctx.message.channel

    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            w = x["wind"]
            current_temperature = y["temp"]  # in kelvin
            current_temp_cel = str(round(current_temperature - 273.15))
            current_temperature_fahrenheit = str(round((current_temperature - 273.15) * 1.8000 + 32.00))
            # wind speed data
            wind_speed = w["speed"]
            curr_wind_speed = str(round(wind_speed * 2.23694))

            # humidity data
            current_humidity = y["humidity"]

            # current weather data description
            z = x["weather"]
            weather_description = z[0]["description"]

            # the bot responds with the weather description and data as an embedded message
            embed = discord.Embed(title=f"Current Weather In {city_name}",
                                  color=ctx.guild.me.top_role.color, timestamp=ctx.message.created_at)

            embed.add_field(name="Description:", value=f"**{weather_description.title()}**", inline=False)

            embed.add_field(name="Temperature (F)  |  (C):",
                            value=f"**{current_temperature_fahrenheit}°F**  |  **{current_temp_cel}°C**", inline=False)

            embed.add_field(name="Humidity(%):", value=f"**{current_humidity}%**", inline=False)

            embed.add_field(name="Wind Speed (mph)  |  (m/s):",
                            value=f"**{curr_wind_speed} mph**  |  **{wind_speed} m/s**", inline=False)

            # Different cases to send the corresponding image of current weather
            if rain_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/RAIN-512.png")

            elif thunder_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/THUNDERSTORM-512.png")

            elif cloudy_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/CLOUDS-512.png")

            elif snow_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/SNOWY-512.png")

            elif clear_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/SUN-512.png")

            else:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/CLOUDYDAY-512.png")

            # displays who asked for the weather in the footer of the embedded message
            embed.set_footer(text=f"Inquired by {ctx.author.name}")

        await channel.send(embed=embed)
    else:
        await channel.send("This is not a valid city! Please try again.")


# Weather command in a chosen city---------------------
@bot.command(pass_context=True)
async def weatherIn(ctx, *, city: str):
    city_name = city

    rain_string = "rain"
    thunder_string = "thunder"
    cloudy_string = "cloud"
    snow_string = "snow" or "hail"
    clear_string = "clear" or "sun"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)
    x = response.json()

    channel = ctx.message.channel

    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            w = x["wind"]
            current_temperature = y["temp"]  # in kelvin
            current_temp_cel = str(round(current_temperature - 273.15))
            current_temperature_fahrenheit = str(round((current_temperature - 273.15) * 1.8000 + 32.00))
            # current wind speed
            wind_speed = w["speed"]
            curr_wind_speed = str(round(wind_speed * 2.23694))

            # current humidity
            current_humidity = y["humidity"]

            # current weather data description
            z = x["weather"]
            weather_description = z[0]["description"]

            # the bot responds with the weather description and data as an embedded message
            embed = discord.Embed(title=f"Current Weather In {city_name}",
                                  color=ctx.guild.me.top_role.color, timestamp=ctx.message.created_at)

            embed.add_field(name="Description:", value=f"**{weather_description.title()}**", inline=False)

            embed.add_field(name="Temperature (F)  |  (C):",
                            value=f"**{current_temperature_fahrenheit}°F**   |   **{current_temp_cel}°C**",
                            inline=False)

            embed.add_field(name="Humidity(%):", value=f"**{current_humidity}%**", inline=False)

            embed.add_field(name="Wind Speed (mph)  |  (m/s):",
                            value=f"**{curr_wind_speed} mph**    |    **{wind_speed} m/s**", inline=False)

            # Different cases to send the corresponding image of current weather
            if rain_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/RAIN-512.png")

            elif thunder_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/THUNDERSTORM-512.png")

            elif cloudy_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/CLOUDS-512.png")

            elif snow_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/SNOWY-512.png")

            elif clear_string in weather_description:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/SUN-512.png")

            else:
                embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-471/128/CLOUDYDAY-512.png")

            # displays who asked for the weather in the footer of the embedded message
            embed.set_footer(text=f"Inquired by {ctx.author.name}")

        await channel.send(embed=embed)
    else:
        await channel.send("This is not a valid city! Please try again.")


# Displays the discounted day event/activities as an image
@bot.command(pass_context=True)
async def Week(ctx):
    embed = discord.Embed(
        title='Weekly Discount View',
        description='Displaying the discounted weekly event/activities as an image',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='The PDF or specific chosen day has links to the websites/ticket purchasing page')
    embed.set_image(url='https://imgur.com/pGRpiYP.jpg')

    await ctx.send(embed=embed)


# Displays the discounts aviable for this requested inquired day
@bot.command(pass_context=True)
async def Mon(ctx):
    embed = discord.Embed(
        title='Monday Discount View',
        description='○ Sea Life Aquarium: 24HR Advanced Booking -$3 Off https://www.visitsealife.com/san-antonio/tickets-passes/ \n\n○ The Japanese Tea Garden: FREE Admission 7AM-5PM https://saparksfoundation.org/japanese-tea-garden/ \n\n○ The Alamo: FREE Admissions (with Reservations) 9AM-5PM https://tickets.thealamo.org/events/10788a82-3771-721c-761d-6a8dc3970f30',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='This is the available discounted events for Monday!')
    embed.set_image(url='https://i.imgur.com/Ipsd9RP.png')

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def Tue(ctx):
    embed = discord.Embed(
        title='Tuesday Discount View',
        description='○ Sea Life Aquarium: 24HR Advanced Booking -$3 Off https://www.visitsealife.com/san-antonio/tickets-passes/   \n\n○ SA Museum of Art: Bexar County Residents get FREE admission 4PM-7PM https://www.samuseum.org/?_ga=2.65562414.182967042.1653544177-2048089792.1653544177 \n\n○ The Japanese Tea Garden: FREE Admission 7AM-5PM https://saparksfoundation.org/japanese-tea-garden/ \n\n○ The Alamo: FREE Admissions (with Reservations) 9AM-5PM https://tickets.thealamo.org/events/10788a82-3771-721c-761d-6a8dc3970f30 \n\n○ The Witte Museum: FREE Admission 3PM-6PM https://www.wittemuseum.org/',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='This is the available discounted events for Tuesday!')
    embed.set_image(url='https://i.imgur.com/1u2se0j.jpg')

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def Wed(ctx):
    embed = discord.Embed(
        title='Wednesday Discount View',
        description='○ Sea Life Aquarium: 24HR Advanced Booking -$3 Off https://www.visitsealife.com/san-antonio/tickets-passes/ \n\n○ The Japanese Tea Garden: FREE Admission 7AM-5PM https://saparksfoundation.org/japanese-tea-garden/ \n\n○ The Alamo: FREE Admissions (with Reservations) 9AM-5PM https://tickets.thealamo.org/events/10788a82-3771-721c-761d-6a8dc3970f30',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='This is the available discounted events for Wednesday!')
    embed.set_image(url='https://i.imgur.com/JHgY6Ob.jpg')

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def Thu(ctx):
    embed = discord.Embed(
        title='Thursday Discount View',
        description='○ Sea Life Aquarium: 24HR Advanced Booking -$3 Off https://www.visitsealife.com/san-antonio/tickets-passes/ \n\n○ The Japanese Tea Garden: FREE Admission 7AM-5PM https://saparksfoundation.org/japanese-tea-garden/ \n\n○ The Alamo: FREE Admissions (with Reservations) 9AM-5PM https://tickets.thealamo.org/events/10788a82-3771-721c-761d-6a8dc3970f30',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='This is the available discounted events for Thursday!')
    embed.set_image(url='https://i.imgur.com/i2A8v0X.jpg')

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def Fri(ctx):
    embed = discord.Embed(
        title='Friday Discount View',
        description='○ The Japanese Tea Garden: FREE Admission 7AM-5PM https://saparksfoundation.org/japanese-tea-garden/ \n\n○ The Alamo: FREE Admissions (with Reservations) 9AM-5PM https://tickets.thealamo.org/events/10788a82-3771-721c-761d-6a8dc3970f30',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='This is the available discounted events for Friday!')
    embed.set_image(url='https://i.imgur.com/RnkQu2Y.jpg')

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def Sat(ctx):
    embed = discord.Embed(
        title='Saturday Discount View',
        description='○ The Japanese Tea Garden: FREE Admission 7AM-5PM https://saparksfoundation.org/japanese-tea-garden/ \n\n○ The Alamo: FREE Admissions (with Reservations) 9AM-5PM https://tickets.thealamo.org/events/10788a82-3771-721c-761d-6a8dc3970f30',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='This is the available discounted events for Saturday!')
    embed.set_image(url='https://i.imgur.com/qxnZC5R.jpg')

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def Sun(ctx):
    embed = discord.Embed(
        title='Sunday Discount View',
        description='○ The Japanese Tea Garden: FREE Admission 7AM-5PM https://saparksfoundation.org/japanese-tea-garden/ \n\n○ SA Museum of Art: Bexar County Residents get FREE admission 4PM-7PM https://www.samuseum.org/?_ga=2.65562414.182967042.1653544177-2048089792.1653544177 \n\n○ The Alamo: FREE Admissions (with Reservations) 9AM-5PM https://tickets.thealamo.org/events/10788a82-3771-721c-761d-6a8dc3970f30',
        colour=discord.Colour.blue()
    )

    embed.set_footer(text='This is the available discounted events for Sunday!')
    embed.set_image(url='https://i.imgur.com/K6B8oa6.jpg')

    await ctx.send(embed=embed)


my_secret = os.environ['TOKEN']
bot.run(my_secret)
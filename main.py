import discord
from discord.ext import commands
import ccxt
import os
from dotenv import load_dotenv

# 1. Setup & Config
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to Binance (or any other exchange supported by CCXT)
exchange = ccxt.binance()

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')

@bot.command()
async def range(ctx, ticker: str, timeframe: str = '1d'):
    """Usage: !range BTC/USDT 1w (Options: 1d, 1w, 1M)"""
    try:
        # Fetch the last 2 candles (current and previous)
        symbol = ticker.upper()
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=2)
        
        # Data structure: [timestamp, open, high, low, close, volume]
        current_candle = ohlcv[-1]
        high, low, close = current_candle[2], current_candle[3], current_candle[4]
        price_range = high - low

        # Format Discord Embed
        embed = discord.Embed(
            title=f"📊 {symbol} {timeframe.upper()} Range",
            color=discord.Color.blue(),
            description=f"Market data retrieved from {exchange.name}"
        )
        embed.add_field(name="Current Price", value=f"${close:,.2f}", inline=False)
        embed.add_field(name="High", value=f"${high:,.2f}", inline=True)
        embed.add_field(name="Low", value=f"${low:,.2f}", inline=True)
        embed.add_field(name="Range Size", value=f"${price_range:,.2f}", inline=False)
        embed.set_footer(text="Requested by " + ctx.author.name)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}. Usage: `!range BTC/USDT 1d`")

if __name__ == "__main__":
    bot.run(TOKEN)



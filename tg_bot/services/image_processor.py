from datetime import datetime
from typing import Optional, Tuple, Type

from PIL import Image, ImageDraw
from tg_bot.models.image import BaseTemplateImage, Colors, Fonts
from tg_bot.models.stocks import TickersList
import tg_bot.services.stock_obtainer as stock


def create_image(tickers: TickersList, image_config: Type[BaseTemplateImage]) -> str:
    """Создание изображения

    создает и сохраняет изображение
    """
    current_date = datetime.now()
    with Image.open(image_config.template_path, "r") as img:
        draw = ImageDraw.Draw(img)

        draw.text(xy=image_config.date_coord,
                  text=current_date.strftime("%d.%m.%Y"),
                  fill=Colors.text,
                  font=Fonts.date_font,
                  anchor="rs")

        draw_prices(draw=draw, tickers=tickers,
                    x_coord=image_config.x_coord,
                    price_coords=image_config.prices_y_coords,
                    diff_coords=image_config.diff_y_coords)

        img.save(image_config.result_path)

    return image_config.result_path


def draw_prices(draw: ImageDraw,
                tickers: TickersList,
                x_coord: int,
                price_coords: Tuple[int, ...],
                diff_coords: Tuple[int, ...]) -> None:
    """Добавление на шаблон информации

    Вычисляет и наносит на шаблонное изображение информацию по
    переданным тикерам
    """
    for tick, price_coord, diff_coord in zip(tickers.tickers, price_coords, diff_coords):
        symbol = _pick_currency_symbol(ticker=tick)
        price = _round_price(ticker=tick)
        draw.text(
            xy=(x_coord, price_coord),
            text=f"{symbol}{price}",
            fill=Colors.text,
            font=Fonts.rate_font,
            anchor="rs",
        )

        price_diff = _calc_price_diff(ticker=tick)
        color = _pick_price_color(ticker=tick)
        draw.text(
            xy=(x_coord, diff_coord),
            text=price_diff,
            fill=color,
            font=Fonts.diff_font,
            anchor="rs",
        )


def _pick_price_color(ticker: stock.TickerBase) -> Tuple[int, int, int]:
    """Определение цвета для отображения"""
    if ticker.current_price < ticker.previous_close:
        return Colors.red
    elif ticker.current_price == ticker.previous_close:
        return Colors.text
    else:
        return Colors.green


def _pick_currency_symbol(ticker: stock.TickerBase) -> Optional[str]:
    """Определение символа для отображения"""
    symbols = {"RUB": "RUB ", "USD": "$"}

    return symbols.get(ticker.currency, "")


def _calc_price_diff(ticker: stock.TickerBase) -> str:
    """Вычисление разницы цен"""
    sub_diff = _calc_subtracting_diff(ticker)
    percentage_diff = _calc_percentage_diff(ticker)

    diff_sign = "+" if sub_diff > 0 else ""
    result_string = \
        f"{diff_sign}{round(percentage_diff, 2)}% ({diff_sign}{round(sub_diff,2)})"

    return result_string


def _calc_percentage_diff(ticker: stock.TickerBase) -> float:
    """Вычисление измениния цены в процентах"""
    percentage_diff = (ticker.current_price / ticker.previous_close - 1) * 100
    return percentage_diff


def _calc_subtracting_diff(ticker: stock.TickerBase) -> float:
    """Вычисление изменения цены"""
    return ticker.current_price - ticker.previous_close


def _round_price(ticker: stock.TickerBase) -> float:
    """Правила округления для цены"""
    if ticker.current_price > 1:
        return round(ticker.current_price, 2)
    else:
        return round(ticker.current_price, 4)

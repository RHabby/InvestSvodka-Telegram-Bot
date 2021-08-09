from dataclasses import dataclass
from typing import Tuple

from PIL import ImageFont


@dataclass
class BaseTemplateImage:
    """Информация для базового шаблона изображения"""

    redis_key: str
    template_path: str
    result_path: str
    tickers: Tuple[str]

    date_coord: Tuple[int, int] = (454, 214)
    x_coord: int = 690
    prices_y_coords: Tuple[int, ...] = \
        tuple(i for i in range(342, 1430 + 1, 136))
    diff_y_coords: Tuple[int, ...] = \
        tuple(i for i in range(378, 1466 + 1, 136))


@dataclass
class IndexesImage(BaseTemplateImage):
    """Информация для подборке индексов"""

    redis_key: str = "indexes"
    template_path: str = "tg_bot/assets/images/templates/base_indexes_template.png"
    result_path: str = "tg_bot/assets/images/ready/base_indexes_ready.png"
    tickers: Tuple[str] = (
        "^GSPC", "^IXIC", "^DJI",
        "IMOEX.ME", "RTSI.ME", "^VIX",
        "RUB=X", "EURRUB=X", "BTC-USD",
    )


@dataclass
class CryptoImage(BaseTemplateImage):
    """Информация для крипто подборке"""

    redis_key: str = "crypto"
    template_path: str = "tg_bot/assets/images/templates/base_crypto_template.png"
    result_path: str = "tg_bot/assets/images/ready/base_crypto_ready.png"
    tickers: Tuple[str] = (
        "BTC-USD", "ETH-USD", "BNB-USD",
        "DOGE-USD", "XRP-USD", "DOT1-USD",
        "ADA-USD", "LTC-USD", "UNI3-USD",
    )


@dataclass
class TinkoffETFImage(BaseTemplateImage):
    """Информация для подборке индексов от Тиньков"""

    redis_key: str = "tinkoff_etf"
    template_path: str = "tg_bot/assets/images/templates/base_tinkoff_etf_template.png"
    result_path: str = "tg_bot/assets/images/ready/base_tinkoff_etf_ready.png"
    tickers: Tuple[str] = (
        "TIPOA.ME", "TGLDA.ME", "TSPXA.ME",
        "TECHA.ME", "TBIOA.ME", "TMOSA.ME",
        "TSPVA.ME", "TGRNA.ME", "TBRUA.ME",
    )


@dataclass(frozen=True)
class Colors:
    """Базовые цвета для изображений"""

    green: Tuple[int, int, int] = (3, 196, 161)
    red: Tuple[int, int, int] = (238, 69, 68)
    text: Tuple[int, int, int] = (255, 255, 255)


@dataclass(frozen=True)
class Fonts:
    """Базовые шрифты для изображений"""

    font_path = "tg_bot/assets/fonts/Lato-Black.ttf"
    date_font = ImageFont.truetype(font=font_path, size=32)
    rate_font = ImageFont.truetype(font=font_path, size=48)
    diff_font = ImageFont.truetype(font=font_path, size=28)

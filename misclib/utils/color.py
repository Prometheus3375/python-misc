from typing import Any, Self, TypedDict

from misclib.functions.comparators import max_with_index

int_float = int, float


def _hsl2rgb_helper(n: int, h_div_30: float, a: float, l_: float, /) -> int:
    k = (n + h_div_30) % 12
    return round((l_ - a * max(-1., min(k - 3., 9. - k, 1.))) * 255.)


def _hsv2rgb_helper(n: int, h_div_60: float, v_times_s: float, v: float, /) -> int:
    k = (n + h_div_60) % 6
    return round((v - v_times_s * max(0., min(k, 4. - k, 1.))) * 255.)


class ColorMap(TypedDict):
    """
    Mapping with color information.
    """
    red: int
    green: int
    blue: int
    alpha: int


class Color:
    """
    Structure for holding color information in RGBA format.
    """

    # It is required to add __weakref__ to slots
    # in order to cache Color using WeakValueDictionary.
    # This increases size of each color object by 8 bytes.
    # The decision was made not to cache colors through WeakValueDictionary.
    # It also not good to use common dict for caching.
    # There are 4,294,967,296 possible colors,
    # one dictionary unable to store them all.
    __slots__ = '_argb',

    def __init__(self, /, red: int, green: int, blue: int, alpha: int = 255) -> None:
        """
        Initializes this structure with the given values of color components.
        All of them must be integers in range [0, 255].
        """
        if not (
                isinstance(red, int)
                and isinstance(green, int)
                and isinstance(blue, int)
                and isinstance(alpha, int)
        ):
            raise ValueError(
                f'values of color components must be integers in range [0, 255], '
                f'got {type(red)=}, {type(green)=}, {type(blue)=}, {type(alpha)=}'
                )
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255 and 0 <= alpha <= 255):
            raise ValueError(
                f'values of color components must be integers in range [0, 255], '
                f'got {red=}, {green=}, {blue=}, {alpha=}'
                )

        # Invert alpha to save 4 bytes of space
        # at a cost of doing subtraction every time to get alpha.
        # It is assumed that most colors in use are completely opaque,
        # making them have alpha at 255, the default value.
        # Numbers less than 2^30 take 28 bytes,
        # but since 2^30 they occupy 32 bytes.
        # Thus, argb number occupies 32 bytes every time alpha is greater than 63,
        # forcing the whole object to weigh more with the most common alpha.
        # Subtracting from 255 resolves this issue.
        # With values of alpha in range [192, 255],
        # argb number still weighs 28 bytes.
        self._argb = (255 - alpha << 24) + (red << 16) + (green << 8) + blue

    @property
    def alpha(self, /) -> int:
        """
        Alpha in range [0, 255] as an integer.
        """
        return 255 - (self._argb >> 24)

    @property
    def red(self, /) -> int:
        """
        Red in range [0, 255] as an integer.
        """
        return self._argb >> 16 & 255

    @property
    def green(self, /) -> int:
        """
        Green in range [0, 255] as an integer.
        """
        return self._argb >> 8 & 255

    @property
    def blue(self, /) -> int:
        """
        Blue in range [0, 255] as an integer.
        """
        return self._argb & 255

    def __str__(self, /) -> str:
        return f'#{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}'

    def __repr__(self, /) -> str:
        return (
            f'{self.__class__.__name__}('
            f'red={self.red}, '
            f'green={self.green}, '
            f'blue={self.blue}, '
            f'alpha={self.alpha}'
            f')'
        )

    def __eq__(self, other: Any, /) -> bool:
        if isinstance(other, Color):
            return self._argb == other._argb

        return NotImplemented

    def __ne__(self, other: Any, /) -> bool:
        if isinstance(other, Color):
            return self._argb != other._argb

        return NotImplemented

    def __hash__(self, /) -> int:
        return self._argb

    def __lt__(self, other: Self, /) -> bool:
        if isinstance(other, Color):
            return self._argb < other._argb

        return NotImplemented

    def __le__(self, other: Self, /) -> bool:
        if isinstance(other, Color):
            return self._argb <= other._argb

        return NotImplemented

    def __gt__(self, other: Self, /) -> bool:
        if isinstance(other, Color):
            return self._argb > other._argb

        return NotImplemented

    def __ge__(self, other: Self, /) -> bool:
        if isinstance(other, Color):
            return self._argb >= other._argb

        return NotImplemented

    def __sizeof__(self, /) -> int:
        return object.__sizeof__(self) + self._argb.__sizeof__()

    @property
    def alpha_f(self, /) -> float:
        """
        Alpha in range [0, 1] as a real number.
        """
        return self.alpha / 255.

    @property
    def red_f(self, /) -> float:
        """
        Red in range [0, 1] as a real number.
        """
        return self.red / 255.

    @property
    def green_f(self, /) -> float:
        """
        Green in range [0, 1] as a real number.
        """
        return self.green / 255.

    @property
    def blue_f(self, /) -> float:
        """
        Blue in range [0, 1] as a real number.
        """
        return self.blue / 255.

    @property
    def alpha_p(self, /) -> float:
        """
        Alpha in range [0, 100] as a percentage.
        """
        return self.alpha * 100 / 255.

    @property
    def red_p(self, /) -> float:
        """
        Red in range [0, 100] as a percentage.
        """
        return self.red * 100 / 255.

    @property
    def green_p(self, /) -> float:
        """
        Green in range [0, 100] as a percentage.
        """
        return self.green * 100 / 255.

    @property
    def blue_p(self, /) -> float:
        """
        Blue in range [0, 100] as a percentage.
        """
        return self.blue * 100 / 255.

    def to_tuple(self, /) -> tuple[int, int, int, int]:
        """
        Converts this structure to a tuple of 4 numbers
        representing color components in the following order:
        red, green, blue, alpha.

        The resulting tuple can be unpacked to the constructor
        to get the same structure back.
        """
        return self.red, self.green, self.blue, self.alpha

    def to_dict(self, /) -> ColorMap:
        """
        Converts this structure to a mapping from color component to its value.

        The resulting tuple can be unpacked to the constructor
        to get the same structure back.
        """
        return {'red': self.red, 'green': self.green, 'blue': self.blue, 'alpha': self.alpha}

    @classmethod
    def from_hex(cls, hex_: str, /, alpha: int = 255) -> Self:
        """
        Creates a color structure from a hex string.
        Information about alpha must at the end of this string,
        or not present at all and passed via parameter ``alpha``.
        """
        if len(str) == 8:
            alpha = int(hex_[6:8], 16)
        elif len(str) != 6:
            raise ValueError(f'length of a hex string must be 6 or 8, got {len(str)}')

        return cls(int(hex_[0:2], 16), int(hex_[2:4], 16), int(hex_[4:6], 16), alpha)

    @property
    def hex(self, /) -> str:
        """
        Converts this structure to a hex string, with alpha at the end.

        The resulting string can be passed to the class method ``from_hex``
        to get the same structure back.
        """
        return f'{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}'

    @classmethod
    def from_hsl(cls, /, hue: float, saturation: float, lightness: float, alpha: int = 255) -> Self:
        """
        Creates a color structure from the given hue, saturation, lightness and alpha.

        Hue must be a real number in range [0, 360],
        saturation and lightness must be real numbers in range [0, 1],
        alpha must be an integer in range [0, 255].
        """
        if not (isinstance(hue, int_float) and 0. <= hue <= 360.):
            raise ValueError(
                f'hue must be a real number in range [0, 360], '
                f'got {hue!r} of type {type(hue)}'
                )
        if not (isinstance(saturation, int_float) and 0. <= saturation <= 1.):
            raise ValueError(
                f'saturation must be a real number in range [0, 1], '
                f'got {saturation!r} of type {type(saturation)}'
                )
        if not (isinstance(lightness, int_float) and 0. <= lightness <= 1.):
            raise ValueError(
                f'lightness must be a real number in range [0, 1], '
                f'got {lightness!r} of type {type(lightness)}'
                )

        # Algorithm: https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB_alternative
        saturation *= min(lightness, 1. - lightness)
        hue /= 30.
        return cls(
            _hsl2rgb_helper(0, hue, saturation, lightness),
            _hsl2rgb_helper(8, hue, saturation, lightness),
            _hsl2rgb_helper(4, hue, saturation, lightness),
            alpha,
            )

    @property
    def hsl(self, /) -> tuple[float, float, float, int]:
        """
        Converts this structure to a tuple of 4 numbers
        representing color components in the following order:
        hue, saturation, lightness, alpha.

        The resulting tuple can be unpacked to the class method ``from_hsl``
        to get the same structure back.
        """
        # Algorithm: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
        comp = self.red_f, self.green_f, self.blue_f
        max_idx, v = max_with_index(comp)
        c = v - min(comp)
        l_ = v - c / 2.
        s = 0. if l_ == 0. or l_ == 1. else (v - l_) / min(l_, 1. - l_)
        h = 0. if c == 0. else \
            (max_idx * 2. + (comp[(max_idx + 1) % 3] - comp[(max_idx + 2) % 3]) / c) % 6 * 60.

        # If red == max, H / 60 = 0 + (green - blue) / C, in [-1, 1].
        # If green == max, H / 60 = 2 + (blue - red) / C, in [1, 3].
        # If blue == max, H / 60 = 4 + (red - green) / C, in [3, 5].
        # Every difference uses next two colors (red -> green -> blue -> red -> green),
        # so we can replace colors in difference with
        # (max_idx + 1) % 3 and (max_idx + 2) % 3 respectively.
        # Shift added to the ratio with C can be replaced with max_idx * 2.
        # Modulo 6 is used for the case with red to remap its result
        # from [-1, 1] to [0, 1] | [5, 6);
        # applying modulo for other cases does nothing.

        return h, s, l_, self.alpha

    @classmethod
    def from_hsv(cls, /, hue: float, saturation: float, value: float, alpha: int = 255) -> Self:
        """
        Creates a color structure from the given hue, saturation, value/brightness and alpha.

        Hue must be a real number in range [0, 360],
        saturation and value/brightness must be real numbers in range [0, 1],
        alpha must be an integer in range [0, 255].
        """
        if not (isinstance(hue, int_float) and 0. <= hue <= 360.):
            raise ValueError(
                f'hue must be a real number in range [0, 360], '
                f'got {hue!r} of type {type(hue)}'
                )
        if not (isinstance(saturation, int_float) and 0. <= saturation <= 1.):
            raise ValueError(
                f'saturation must be a real number in range [0, 1], '
                f'got {saturation!r} of type {type(saturation)}'
                )
        if not (isinstance(value, int_float) and 0. <= value <= 1.):
            raise ValueError(
                f'value/brightness must be a real number in range [0, 1], '
                f'got {value!r} of type {type(value)}'
                )

        # Algorithm: https://en.wikipedia.org/wiki/HSL_and_HSV#HSV_to_RGB_alternative
        saturation *= value
        hue /= 60.
        return cls(
            _hsv2rgb_helper(5, hue, saturation, value),
            _hsv2rgb_helper(3, hue, saturation, value),
            _hsv2rgb_helper(1, hue, saturation, value),
            alpha,
            )

    @property
    def hsv(self, /) -> tuple[float, float, float, int]:
        """
        Converts this structure to a tuple of 4 numbers
        representing color components in the following order:
        hue, saturation, value/brightness, alpha.

        The resulting tuple can be unpacked to the class method ``from_hsv``
        to get the same structure back.
        """
        # Algorithm: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
        comp = self.red_f, self.green_f, self.blue_f
        max_idx, v = max_with_index(comp)
        c = v - min(comp)
        s = 0. if v == 0. else c / v
        h = 0. if c == 0. else \
            (max_idx * 2. + (comp[(max_idx + 1) % 3] - comp[(max_idx + 2) % 3]) / c) % 6 * 60.

        return h, s, v, self.alpha

    from_hsb = from_hsv
    hsb = hsv


__all__ = 'Color', 'ColorMap',

import sys
from collections.abc import Iterable, Iterator
from itertools import product
from typing import override
from unittest import TestCase, skipUnless

from misclib.utils.color import Color


sample_numbers = [
    i
    for k in ((i - 2, i - 1, i, i + 1, i + 2) for i in range(0, 257, 32))
    for i in k
    if 0 <= i <= 255
    ]


class TestColorSample(TestCase):
    @staticmethod
    def values() -> Iterable[int]:
        return sample_numbers

    def data(self, /) -> Iterator[tuple[int, int, int, int]]:
        return product(self.values(), self.values(), self.values(), self.values())

    def data_no_alpha(self, /) -> Iterator[tuple[int, int, int]]:
        return product(self.values(), self.values(), self.values())

    def test_constructor(self, /) -> None:
        for red, green, blue, alpha in self.data():
            color = Color(red, green, blue, alpha)
            color_tuple = color.to_tuple()
            color_map = color.to_dict()
            self.assertEqual(color, Color(*color_tuple))
            self.assertEqual(color, Color(**color_map))

    def test_properties(self, /) -> None:
        for red, green, blue, alpha in self.data():
            color_kw = Color(red=red, green=green, blue=blue, alpha=alpha)
            color_pos = Color(red, green, blue, alpha)
            for color in (color_kw, color_pos):
                self.assertEqual(red, color.red)
                self.assertEqual(green, color.green)
                self.assertEqual(blue, color.blue)
                self.assertEqual(alpha, color.alpha)

                self.assertEqual(red / 255, color.red_f)
                self.assertEqual(green / 255, color.green_f)
                self.assertEqual(blue / 255, color.blue_f)
                self.assertEqual(alpha / 255, color.alpha_f)

                self.assertEqual(red * 100 / 255, color.red_p)
                self.assertEqual(green * 100 / 255, color.green_p)
                self.assertEqual(blue * 100 / 255, color.blue_p)
                self.assertEqual(alpha * 100 / 255, color.alpha_p)

    def test_hex(self, /) -> None:
        for red, green, blue in self.data_no_alpha():
            hex_no_alpha = f'{red:02x}{green:02x}{blue:02x}'

            for alpha in self.values():
                color = Color(red, green, blue, alpha)
                self.assertEqual(color, Color.from_hex(hex_no_alpha, alpha=alpha))

                hex_with_alpha = color.hex
                self.assertEqual(color, Color.from_hex(hex_with_alpha))
                self.assertEqual(color, Color.from_hex(hex_with_alpha, alpha=255-alpha))

    def test_conversions(self, /) -> None:
        for red, green, blue in self.data_no_alpha():
            color = Color(red, green, blue)
            hsl = color.hsl
            hsv = color.hsv
            self.assertEqual(color, Color.from_hsl(*hsl))
            self.assertEqual(color, Color.from_hsv(*hsv))

    def test_examples(self, /) -> None:
        hsl = [
            (119, 1, 0.625),
            (20.1, 1, 0.625),
            (212, 1, 0.53),
            (300, 1, 0.75),
            (60, 1, 0.75),
            (180, 1, 0.75),
            ]
        hsv = [
            (119, 0.75, 1),
            (20.1, 0.75, 1),
            (212, 0.94, 1),
            (300, 0.5, 1),
            (60, 0.5, 1),
            (180, 0.5, 1),
            ]

        for (hue1, sat_l, lightness), (hue2, sat_v, value) in zip(hsl, hsv):
            self.assertEqual(hue1, hue2)
            with self.subTest(H=hue1, S_L=sat_l, S_V=sat_v, L=lightness, V=value):
                self.assertEqual(
                    Color.from_hsl(hue=hue1, saturation=sat_l, lightness=lightness),
                    Color.from_hsv(hue=hue2, saturation=sat_v, value=value),
                    )


@skipUnless('TestColorFull' in sys.argv[-1], 'must be called directly')
class TestColorFull(TestColorSample):
    @staticmethod
    @override
    def values() -> Iterable[int]:
        return range(256)

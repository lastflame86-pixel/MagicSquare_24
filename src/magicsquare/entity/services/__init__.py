"""Domain services (FR-02~FR-04)."""

from magicsquare.entity.services.empty_cell_locator import find_blank_coords
from magicsquare.entity.services.magic_square_validator import is_magic_square
from magicsquare.entity.services.missing_number_finder import find_not_exist_nums
from magicsquare.entity.services.two_cell_solver import solution

__all__ = ["find_blank_coords", "find_not_exist_nums", "is_magic_square", "solution"]

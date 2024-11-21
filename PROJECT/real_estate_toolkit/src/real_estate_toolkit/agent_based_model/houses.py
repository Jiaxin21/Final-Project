from enum import Enum
from dataclasses import dataclass
from typing import Optional


class QualityScore(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1

@dataclass
class House:
    id: int
    price: float
    area: float
    bedrooms: int
    year_built: int
    quality_score: Optional[QualityScore]
    available: bool = True

    def calculate_price_per_square_foot(self) -> float:
        """
        Calculate and return the price per square foot.
        - Divide price by area.
        - Round to 2 decimal places.
        - Handle edge cases (e.g., area = 0).
        """
        if self.area <= 0:
            return 0.0  # Avoid division by zero
        return round(self.price / self.area, 2)

    def is_new_construction(self, current_year: int = 2024) -> bool:
        """
        Determine if house is considered new construction (< 5 years old).
        - Compare current_year with year_built.
        """
        return (current_year - self.year_built) < 5

    def get_quality_score(self) -> None:
        """
        Generate a quality score based on house attributes if not already set.
        Score is determined by:
            - Age of the house (newer houses score higher)
            - Area of the house (larger houses score higher)
            - Number of bedrooms
        If quality_score is already set, this method does nothing.
        """

        if self.quality_score is None:
            # Calculate individual scores
            age_score = self._calculate_age_score()
            area_score = self._calculate_area_score()
            bedroom_score = self._calculate_bedroom_score()

            # Calculate the average score and assign the quality score
            total_score = round((age_score + area_score + bedroom_score) / 3)
            self.quality_score = QualityScore(total_score)


    def sell_house(self) -> None:
        """Mark house as sold."""
        self.available = False

    def _calculate_age_score(self) -> int:
        """Calculate the age score based on the year built."""
        if self.year_built >= 2019:
            return 5
        elif self.year_built >= 2009:
            return 4
        elif self.year_built >= 1999:
            return 3
        elif self.year_built >= 1989:
            return 2
        else:
            return 1

    def _calculate_area_score(self) -> int:
        """Calculate the area score based on the square footage."""
        if self.area >= 3000:
            return 5
        elif self.area >= 2000:
            return 4
        elif self.area >= 1500:
            return 3
        elif self.area >= 1000:
            return 2
        else:
            return 1

    def _calculate_bedroom_score(self) -> int:
        """Calculate the bedroom score based on the number of bedrooms."""
        if self.bedrooms >= 5:
            return 5
        elif self.bedrooms >= 4:
            return 4
        elif self.bedrooms >= 3:
            return 3
        elif self.bedrooms >= 2:
            return 2
        else:
            return 1













from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
from .houses import House
from .house_market import HousingMarket


class Segment(Enum):
    FANCY = auto()  # Prefers new construction with high quality scores
    OPTIMIZER = auto()  # Focuses on price per square foot value
    AVERAGE = auto()  # Considers average market prices


@dataclass
class Consumer:
    id: int
    annual_income: float
    children_number: int
    segment: Segment
    house: Optional[House] = None
    savings: float = 0.0
    saving_rate: float = 0.3
    interest_rate: float = 0.05

    def compute_savings(self, years: int) -> None:
        """
        Calculate accumulated savings over time using compound interest.
        Args:
            years (int): The number of years to compute savings for.
        """
        annual_savings = self.annual_income * self.saving_rate
        self.savings = annual_savings * ((1 + self.interest_rate) ** years - 1) / self.interest_rate
    

    def buy_a_house(self, housing_market: HousingMarket) -> None:
        """
        Attempt to purchase a suitable house from the housing market
        based on consumer preferences and available savings.

        Args:
            housing_market (HousingMarket): The market containing houses for sale.
        """
        # Step 1: Filter houses based on segment preferences
        if self.segment == Segment.FANCY:
            # Segment prefers new construction with high quality scores
            suitable_houses = [
                house for house in housing_market.houses
                if house.is_new_construction() and house.quality_score and house.quality_score.value >= 4 and house.available
            ]
        elif self.segment == Segment.OPTIMIZER:
            # Segment prefers houses with the best price per square foot value
            suitable_houses = [
                house for house in housing_market.houses
                if house.calculate_price_per_square_foot() <= (self.annual_income / 12) and house.available
            ]
        elif self.segment == Segment.AVERAGE:
            # Segment prefers houses priced below the average market price
            average_price = housing_market.calculate_average_price()
            suitable_houses = [
                house for house in housing_market.houses
                if house.price <= average_price and house.available
            ]
        else:
            suitable_houses = []

        # Step 2: Allow flexible criteria based on family size or savings
        # No hardcoded assumptions for family size or specific down payment requirements
        suitable_houses = [
            house for house in suitable_houses
            if self.savings >= house.price  # Full affordability check (no partial payments assumed)
        ]

        # Step 3: Determine the best house to buy (if any)
        if suitable_houses:
            # Optionally, prioritize the lowest-priced house
            house_to_buy = min(suitable_houses, key=lambda house: house.price)

            # Assign the house to the consumer and deduct the price from savings
            self.house = house_to_buy
            self.savings -= house_to_buy.price
            house_to_buy.available = False  # Mark as sold
            print(f"Consumer {self.id} purchased house {house_to_buy.id} for ${house_to_buy.price}!")
        else:
            # No suitable house found
            print(f"Consumer {self.id} could not find a suitable house.")

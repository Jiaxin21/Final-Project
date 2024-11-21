from typing import List, Optional
from .houses import House


class HousingMarket:
    def __init__(self, houses: List[House]):
        self.houses: List[House] = houses

    def get_house_by_id(self, house_id: int) -> Optional[House]:
        """
        Retrieve specific house by ID.
        Args:
            house_id (int): The unique identifier of the house.
        Returns:
            Optional[House]: The house with the specified ID or None if not found.
        """
        for house in self.houses:
            if house.id == house_id:
                return house
        return None  # If no house with the given ID exists

    def calculate_average_price(self, bedrooms: Optional[int] = None) -> float:
        """
        Calculate average house price, optionally filtered by bedrooms.
        Args:
            bedrooms (Optional[int]): Number of bedrooms to filter by. If None, consider all houses.
        Returns:
            float: The average price of the filtered houses, or 0.0 if no houses match.
        """
        filtered_houses = (
            [house for house in self.houses if house.bedrooms == bedrooms] if bedrooms is not None else self.houses
        )
        if not filtered_houses:
            return 0.0
        total_price = sum(house.price for house in filtered_houses)
        return total_price / len(filtered_houses)

    def get_houses_that_meet_requirements(self, max_price: int, segment: str) -> List[House]:
        """
        Filter houses based on buyer requirements.
        
        Args:
            max_price (int): The maximum price the buyer is willing to pay.
            segment (str): The target segment based on quality (e.g., "EXCELLENT", "GOOD").
        
        Returns:
            List[House]: A list of houses that meet the requirements. Returns an empty list if no houses match.
        """
        segment_map = {
            "EXCELLENT": 5,
            "GOOD": 4,
            "AVERAGE": 3,
            "FAIR": 2,
            "POOR": 1
        }

        target_quality = segment_map.get(segment.upper())
        if target_quality is None:
            raise ValueError(f"Invalid segment: {segment}. Must be one of {list(segment_map.keys())}.")

        filtered_houses = [
            house for house in self.houses
            if house.price <= max_price and house.quality_score and house.quality_score.value == target_quality
        ]
        return filtered_houses










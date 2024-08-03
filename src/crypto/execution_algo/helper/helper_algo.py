"""
Helper Functions used in Trading Algos
"""

import ast
import math
import random
from typing import Optional

from src.crypto.execution_algo.tools.constants import Constants


class HelperAlgo:
    """
    Helper class for trading algos
    """

    @staticmethod
    def floor_amount(value: float, decimal_places: int):
        """
        returns value rounded down to specified number of decimal places
        """
        factor = 1 * 10**decimal_places
        return math.floor(value * factor) / factor

    @staticmethod
    def randomize(
        number_of_values: int,
        lower_bound: float,
        upper_bound: float,
        sum_values: float,
        rounding: Optional[float] = 8,
    ) -> list:
        """
        generates values with a lower and upper bound
        Used for generating clip sizes and sleep timings

        Args:
            number_of_values (int): The number of random values to generate.
            lower_bound (float): The minimum value of the range (inclusive).
            upper_bound (float): The maximum value of the range (inclusive).
            sum_values (float): The desired sum of the generated values.
            rounding (float): rounds to specified decimal places

        Returns:
            list of randomized values
        """
        print(f"generating {number_of_values} values with sum = {sum_values}")

        if lower_bound < 0 or upper_bound < 0:
            print("please select non-negative upper and lower bounds")
            return None

        if upper_bound - lower_bound >= lower_bound:
            print("please select smaller bounds or one that's more positive")
            return None

        if (
            number_of_values <= 0
            or sum_values < number_of_values * lower_bound
            or sum_values > number_of_values * upper_bound
        ):
            print("please select different parameters")
            return None

        values = []

        # generate values that are within the bounds
        for _ in range(number_of_values):
            value = random.uniform(lower_bound, upper_bound)
            values.append(value)
            sum_values -= value  # calculates the excess or shortfall from target amt

        # offset each element by this amount
        offset = sum_values / number_of_values

        for i, j in enumerate(values):
            values[i] += offset
            if rounding:
                values[i] = round(values[i], rounding)
        return values

    @staticmethod
    def generate_clip_sizes(
        clip_count: int,
        total_sum: float,
        proportions: list,
        rounding: int = None,
    ):
        """
        Generates clip sizes in descending order for OTC trade executions
        by dividing the total sum among clips according to preset proportions.

        Args:
            clip_count (int): The number of clip sizes to generate.
            total_sum (float): The desired total sum of the generated clip sizes.
            proportions (list): List of proportions.
            rounding (int): Number of decimal places to round to (optional).

        Returns:
            list: List of generated clip sizes.
        """
        print(f"Generating {clip_count} clip sizes with total sum = {total_sum}")

        # Check if proportions are acceptable
        if any(p <= 0 or not isinstance(p, float) for p in proportions):
            print("Proportions can only be non-zero positive float values.")
            return

        if sum(proportions) != 1:
            print("Sum of proportions has to be 1.")
            return

        if clip_count < len(proportions):
            print(f"Clip count has to be at least >= {len(proportions)}")
            return

        if clip_count % len(proportions) != 0:
            print("select different clip counts and proportions")
            return

        # Calculate clips per proportion and remaining clips
        proportioned_values = [p * total_sum for p in proportions]

        clip_sizes = []
        clip_proportion_length = clip_count // len(proportions)
        print(clip_proportion_length)
        for p in proportioned_values:
            clip_sizes += int(clip_proportion_length) * [
                round(p / clip_proportion_length, rounding)
            ]
        return clip_sizes

    @staticmethod
    def params_parser(trading_params: dict) -> dict:
        """
        Accepts Trading params as input and returns a dict with input params
        as well as calculated params in the correct data type

        Args:
            params (dict): Trading Params

        Returns:
            dict:
        """

        def safe_eval(value, target_type):
            try:
                return target_type(ast.literal_eval(value))
            except (ValueError, SyntaxError):
                return target_type(value)

        string_params = [
            Constants.EXCHANGE,
            Constants.ACCOUNT_NAME,
            Constants.ALGO_TYPE,
            Constants.BASE_CURRENCY,
            Constants.QUOTE_CURRENCY,
            Constants.TICKER,
            Constants.DIRECTION,
            Constants.CLIP_TYPE,
            Constants.ORDER_ID,
            Constants.TRADE_STATUS,
        ]
        float_params = [
            Constants.CLIP_LIMIT,
            Constants.QUANTITY,
            Constants.LEVERAGE_RATIO,
            Constants.PRICE,
            Constants.PERCENTAGE_OF_VOLUME,
            Constants.PERCENTAGE_OF_VOLUME_LOOKBACK,
            Constants.POST_ONLY_CLIP_SIZE,
            Constants.RANDOMIZER,
        ]
        int_params = [
            Constants.TWAP_DURATION,
            Constants.TWAP_CLIP_INTERVAL,
            Constants.TELEGRAM_GROUP,
        ]
        eval_params = [
            Constants.OTC_EXECUTION_PROPORTIONS,
        ]

        # Using dictionary comprehension to construct order_params
        order_params = {
            param.value: str(trading_params[param].upper()) for param in string_params
        }
        order_params.update(
            {param.value: float(trading_params[param]) for param in float_params}
        )
        order_params.update(
            {param.value: int(trading_params[param]) for param in int_params}
        )
        order_params.update(
            {
                param.value: safe_eval(trading_params[param], list)
                for param in eval_params
            }
        )

        if order_params[Constants.CLIP_TYPE].upper() == "BASE":
            order_params[Constants.CLIP_CCY.value] = order_params[
                Constants.BASE_CURRENCY
            ]
        elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            order_params[Constants.CLIP_CCY.value] = order_params[
                Constants.QUOTE_CURRENCY
            ]
        else:
            print("Check on Clip Type")
            return

        # calculated params
        order_params[Constants.CLIP_COUNT.value] = int(
            order_params[Constants.TWAP_DURATION]
            / order_params[Constants.TWAP_CLIP_INTERVAL]
        )
        order_params[Constants.CLIP_SIZE.value] = (
            order_params[Constants.QUANTITY] / order_params[Constants.CLIP_COUNT]
        )
        return order_params

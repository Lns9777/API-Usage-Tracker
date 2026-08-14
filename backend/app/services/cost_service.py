from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PricingSnapshot:
    input_price_per_1m: float = 0.0
    output_price_per_1m: float = 0.0
    thinking_price_per_1m: float = 0.0
    cached_input_price_per_1m: float = 0.0


def calculate_costs(
    *,
    pricing: PricingSnapshot,
    input_tokens: int = 0,
    output_tokens: int = 0,
    thinking_tokens: int = 0,
    cached_tokens: int = 0,
) -> dict[str, float]:
    input_cost = (input_tokens / 1_000_000) * pricing.input_price_per_1m
    output_cost = (output_tokens / 1_000_000) * pricing.output_price_per_1m
    thinking_cost = (thinking_tokens / 1_000_000) * pricing.thinking_price_per_1m
    cached_cost = (cached_tokens / 1_000_000) * pricing.cached_input_price_per_1m
    total_cost = input_cost + output_cost + thinking_cost + cached_cost
    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "thinking_cost": thinking_cost,
        "cached_cost": cached_cost,
        "total_cost": total_cost,
    }

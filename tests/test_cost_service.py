from backend.app.services.cost_service import PricingSnapshot, calculate_costs


def test_calculate_costs():
    costs = calculate_costs(
        pricing=PricingSnapshot(
            input_price_per_1m=2.0,
            output_price_per_1m=4.0,
            thinking_price_per_1m=1.0,
            cached_input_price_per_1m=0.5,
        ),
        input_tokens=1_000_000,
        output_tokens=500_000,
        thinking_tokens=250_000,
        cached_tokens=100_000,
    )

    assert costs["input_cost"] == 2.0
    assert costs["output_cost"] == 2.0
    assert costs["thinking_cost"] == 0.25
    assert costs["cached_cost"] == 0.05

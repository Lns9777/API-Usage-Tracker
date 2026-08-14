PRICING = {

    "openai": {

        "gpt-5": {
            "input": 0.0,
            "output": 0.0,
            "thinking": 0.0,
            "cached": 0.0,
        },

    },

    "gemini": {

        "gemini-2.5-flash": {
            "input": 0.0,
            "output": 0.0,
            "thinking": 0.0,
            "cached": 0.0,
        },

    },
}


def calculate_cost(
    provider: str,
    model: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    thinking_tokens: int = 0,
    cached_tokens: int = 0,
):
    provider_data = PRICING.get(
        provider.lower(),
        {},
    )

    model_data = provider_data.get(
        model,
        {
            "input": 0.0,
            "output": 0.0,
            "thinking": 0.0,
            "cached": 0.0,
        },
    )

    input_cost = (
        input_tokens / 1_000_000
    ) * model_data["input"]

    output_cost = (
        output_tokens / 1_000_000
    ) * model_data["output"]

    thinking_cost = (
        thinking_tokens / 1_000_000
    ) * model_data["thinking"]

    cached_cost = (
        cached_tokens / 1_000_000
    ) * model_data["cached"]

    total_cost = (
        input_cost
        + output_cost
        + thinking_cost
        + cached_cost
    )

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "thinking_cost": thinking_cost,
        "cached_cost": cached_cost,
        "total_cost": total_cost,
    }
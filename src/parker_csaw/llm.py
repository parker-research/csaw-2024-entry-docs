import openai

from parker_csaw.secrets_and_paths import get_secrets


def make_openai_client() -> openai.OpenAI:
    """Creates an OpenAI client."""

    secrets = get_secrets()
    openai_kwargs = secrets["openai_client_kwargs"]

    if "project" not in openai_kwargs or "organization" not in openai_kwargs:
        raise ValueError(
            'The "project" and "organization" keys must be in the OpenAI client kwargs.'
        )

    # TODO: Add other auth options, maybe.

    client = openai.OpenAI(
        **openai_kwargs,
        timeout=45,  # Long timeout required for large modules.
    )
    return client


def basic_llm_prompt(prompt: str) -> str:
    """Make a basic prompt to an LLM, and get the response."""
    # Source: https://platform.openai.com/docs/quickstart?language-preference=python

    client = make_openai_client()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, with experience in Verilog design.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    resp = completion.choices[0].message.content

    if resp is None:
        raise ValueError(
            "The response is None. The LLM may have failed to generate a response."
        )

    return resp

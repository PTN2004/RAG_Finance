import torch
from transformers import BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.llms import HuggingFacePipeline

# nf4_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_compute_dtype=torch.bfloat16,
#     bnb_4bit_quant_type='nf4',
#     bnb_4bit_use_double_quant=True
# )


def get_model(model_name: str = "meta-llama/Llama-3.2-3B-Instruct", max_token=1024, **kwargs):
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    ).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model_pipeline = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_token=max_token
    )

    llm = HuggingFacePipeline(
        pipeline=model_pipeline,
        model_kwargs=kwargs
    )

    return llm

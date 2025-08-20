from ai_researcher.utils import get_paper_from_generated_text
import openai
import os


class CycleResearcher:
    """
    A class for generating research papers using CycleResearcher models.
    """

    def __init__(self, max_model_len=8192):
        """
        Initialize the CycleResearcher.

        Args:
            max_model_len (int): Maximum number of tokens for generation (default: 8192, can be increased for longer papers)
        """
        # CycleResearcher ONLY works with gpt-5
        
        self.use_openai = True
        self.model_name = "gpt-5"
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tokenizer = None  # Not needed for OpenAI API
        self.model = None  # Not needed for OpenAI API
        self.model_config = {
            "model": "gpt-5",
            "max_tokens": max_model_len,
            "temperature": 0.4,
            "reasoning_effort": "high"
        }


    def generate_paper(self, topic=None, references=None, max_tokens=19000, n=1):
        """
        Generate a research paper on the given topic.

        Args:
            topic (str): Research paper topic
            references (str, optional): BibTeX context
            max_tokens (int, optional): Maximum number of tokens to generate

        Returns:
            dict: Generated paper with various components
        """
        # Prepare system prompt
        system_prompt = "You are a research assistant AI tasked with generating a scientific paper based on provided literature. Follow these steps:\n\n1. Analyze the given References. \n2. Identify gaps in existing research to establish the motivation for a new study.\n3. Propose a main idea for a new research work.\n4. Write the paper's main content in LaTeX format, including:\n   - Title\n   - Abstract\n   - Introduction\n   - Related Work\n   - Methods/\n5. Generate experimental setup details in JSON format to guide researchers.\n6. After receiving experimental results in JSON format, analyze them.\n7. Complete the paper by writing:\n   - Results\n   - Discussion\n   - Conclusion\n   - Contributions\n\nEnsure all content is original, academically rigorous, and follows standard scientific writing conventions."""

        # Prepare user prompt
        user_prompt = ''
        if topic != None:
            user_prompt = f"Generate a research paper on the topic: {topic}\n\n"
        if references != None:
            user_prompt += references
            user_prompt += '\n\n'
        user_prompt += 'The above content represents the relevant literature in this field. Please analyze it and provide the motivation and main idea. Then, provide the Title, Abstract, Introduction, Related Work, and Methods sections in LaTeX format.'
        # Prepare messages for generation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        papers = []
        
        if self.use_openai:
            # Use OpenAI gpt-5 API (recommended approach)
            for i in range(n):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model_config["model"],
                        messages=messages,
                        max_completion_tokens=min(max_tokens, self.model_config["max_tokens"]),
                        temperature=self.model_config["temperature"],
                        reasoning_effort=self.model_config["reasoning_effort"]
                    )
                    generated_text = response.choices[0].message.content
                    
                    # Use existing CycleResearcher utility to parse generated text
                    paper = get_paper_from_generated_text(generated_text)
                    papers.append(paper)
                    
                except Exception as e:
                    print(f"OpenAI API error for paper {i+1}: {e}")
                    # Return empty paper structure if API fails
                    papers.append({
                        "title": f"Error generating paper {i+1}",
                        "abstract": f"API Error: {str(e)}",
                        "content": generated_text if 'generated_text' in locals() else ""
                    })
        else:
            # Use local vLLM models (legacy approach)
            # Prepare sampling parameters
            sampling_params = SamplingParams(
                temperature=0.4,
                top_p=0.95,
                max_tokens=max_tokens,
                ignore_eos=True,
                stop=['\clearpage','\clear','clearpage']
            )
            # Apply chat template
            prompts = []
            batch_size = 10
            for p in range(0, n, batch_size):
                for _ in range(min(batch_size, n - p)):
                    input_text = self.tokenizer.apply_chat_template(messages, tokenize=False,
                                                      add_generation_prompt=True)
                    prompts.append(input_text)
                # Generate paper
                outputs = self.model.generate(
                    prompts,
                    sampling_params
                )
                for output_num in range(len(outputs)):
                    # Process generated text
                    generated_text = outputs[output_num].outputs[0].text
                    # Use existing CycleResearcher utility to parse generated text
                    paper = get_paper_from_generated_text(generated_text)
                    papers.append(paper)
        
        return papers
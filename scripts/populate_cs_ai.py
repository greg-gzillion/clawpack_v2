import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\claw_coder"
files = {}

# === CS FUNDAMENTALS - TOP UNIVERSITIES ===
files["cs_fundamentals/mit_ocw/mit_courses.md"] = """# MIT OpenCourseWare - Computer Science

## Core CS Curriculum
| Course | Topic | URL |
|--------|-------|-----|
| 6.0001 | Intro to CS and Python | https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python/ |
| 6.0002 | Computational Thinking | https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science/ |
| 6.006 | Introduction to Algorithms | https://ocw.mit.edu/courses/6-006-introduction-to-algorithms/ |
| 6.046 | Design and Analysis of Algorithms | https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms/ |
| 6.033 | Computer System Engineering | https://ocw.mit.edu/courses/6-033-computer-system-engineering/ |
| 6.034 | Artificial Intelligence | https://ocw.mit.edu/courses/6-034-artificial-intelligence/ |
| 6.036 | Machine Learning | https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning/ |
| 6.042 | Mathematics for CS | https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science/ |
| 6.824 | Distributed Systems | https://ocw.mit.edu/courses/6-824-distributed-computer-systems-engineering/ |
| 6.858 | Computer Systems Security | https://ocw.mit.edu/courses/6-858-computer-systems-security/ |
"""

files["cs_fundamentals/stanford/stanford_courses.md"] = """# Stanford University - Computer Science

## Core CS Resources
| Course | Topic | URL |
|--------|-------|-----|
| CS106B | Programming Abstractions | https://web.stanford.edu/class/cs106b/ |
| CS107 | Computer Organization & Systems | https://web.stanford.edu/class/cs107/ |
| CS110 | Principles of Computer Systems | https://web.stanford.edu/class/cs110/ |
| CS144 | Introduction to Computer Networking | https://cs144.github.io/ |
| CS161 | Design and Analysis of Algorithms | https://web.stanford.edu/class/cs161/ |
| CS221 | Artificial Intelligence: Principles | https://stanford-cs221.github.io/ |
| CS229 | Machine Learning | https://cs229.stanford.edu/ |
| CS230 | Deep Learning | https://cs230.stanford.edu/ |
| CS231N | Computer Vision | https://cs231n.stanford.edu/ |
| CS224N | NLP with Deep Learning | https://web.stanford.edu/class/cs224n/ |
| CS234 | Reinforcement Learning | https://web.stanford.edu/class/cs234/ |
| CS255 | Cryptography | https://crypto.stanford.edu/~dabo/cs255/ |
"""

files["cs_fundamentals/berkeley/berkeley_courses.md"] = """# UC Berkeley - Computer Science

## Core CS Resources
| Course | Topic | URL |
|--------|-------|-----|
| CS61A | Structure and Interpretation | https://cs61a.org/ |
| CS61B | Data Structures | https://sp24.datastructur.es/ |
| CS61C | Machine Structures | https://cs61c.org/ |
| CS70 | Discrete Math and Probability | https://www.eecs70.org/ |
| CS161 | Computer Security | https://fa24.cs161.org/ |
| CS162 | Operating Systems | https://cs162.org/ |
| CS164 | Programming Languages | https://cs164.org/ |
| CS170 | Efficient Algorithms | https://cs170.org/ |
| CS186 | Database Systems | https://cs186berkeley.net/ |
| CS188 | Artificial Intelligence | https://inst.eecs.berkeley.edu/~cs188/ |
| CS189 | Machine Learning | https://www.eecs189.org/ |
| CS182 | Deep Neural Networks | https://cs182sp21.github.io/ |
| CS285 | Deep Reinforcement Learning | https://rail.eecs.berkeley.edu/deeprlcourse/ |
| CS294 | Advanced ML Topics | https://www.eecs189.org/ |
"""

files["cs_fundamentals/cmu/cmu_courses.md"] = """# Carnegie Mellon University - Computer Science

## Core CS Resources
| Course | Topic | URL |
|--------|-------|-----|
| 15-112 | Fundamentals of Programming | https://www.cs.cmu.edu/~112/ |
| 15-122 | Principles of Imperative Computation | https://www.cs.cmu.edu/~15122/ |
| 15-150 | Functional Programming | https://www.cs.cmu.edu/~15150/ |
| 15-210 | Parallel and Sequential Algorithms | https://www.cs.cmu.edu/~15210/ |
| 15-213 | Introduction to Computer Systems | https://www.cs.cmu.edu/~213/ |
| 15-251 | Great Ideas in Theoretical CS | https://www.cs.cmu.edu/~15251/ |
| 15-312 | Foundations of Programming Languages | https://www.cs.cmu.edu/~15312/ |
| 15-381 | Artificial Intelligence | https://www.cs.cmu.edu/~15381/ |
| 15-440 | Distributed Systems | https://www.cs.cmu.edu/~15440/ |
| 15-445 | Database Systems | https://15445.courses.cs.cmu.edu/ |
| 15-721 | Advanced Database Systems | https://15721.courses.cs.cmu.edu/ |
| 10-701 | Machine Learning | https://www.cs.cmu.edu/~10701/ |
| 11-785 | Deep Learning | https://deeplearning.cs.cmu.edu/ |
"""

files["cs_fundamentals/harvard/harvard_courses.md"] = """# Harvard University - Computer Science

## Core CS Resources
| Course | Topic | URL |
|--------|-------|-----|
| CS50 | Introduction to Computer Science | https://cs50.harvard.edu/ |
| CS50 AI | Introduction to AI with Python | https://cs50.harvard.edu/ai/ |
| CS50 Web | Web Programming with Python | https://cs50.harvard.edu/web/ |
| CS51 | Abstraction and Design | https://cs51.io/ |
| CS61 | Systems Programming | https://cs61.seas.harvard.edu/ |
| CS109 | Data Science | https://cs109.github.io/ |
| CS124 | Data Structures and Algorithms | https://cs124.seas.harvard.edu/ |
| CS152 | Programming Languages | https://cs152.seas.harvard.edu/ |
| CS181 | Machine Learning | https://cs181.seas.harvard.edu/ |
| CS182 | Artificial Intelligence | https://cs182.seas.harvard.edu/ |
"""

# === AI/ML CUTTING EDGE ===
files["ai_ml/university_curriculum/ai_curriculum.md"] = """# Complete AI/ML Curriculum from Top Programs

## MIT AI Track
| Course | Topic | URL |
|--------|-------|-----|
| 6.034 | Artificial Intelligence | https://ocw.mit.edu/courses/6-034-artificial-intelligence/ |
| 6.036 | Machine Learning | https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning/ |
| 6.S191 | Introduction to Deep Learning | http://introtodeeplearning.com/ |
| 6.S094 | Deep Learning for Self-Driving Cars | https://selfdrivingcars.mit.edu/ |

## Stanford AI Track
| Course | Topic | URL |
|--------|-------|-----|
| CS221 | AI Principles and Techniques | https://stanford-cs221.github.io/ |
| CS229 | Machine Learning | https://cs229.stanford.edu/ |
| CS230 | Deep Learning | https://cs230.stanford.edu/ |
| CS224N | NLP with Deep Learning | https://web.stanford.edu/class/cs224n/ |
| CS231N | Computer Vision | https://cs231n.stanford.edu/ |
| CS234 | Reinforcement Learning | https://web.stanford.edu/class/cs234/ |
| CS324 | Large Language Models | https://stanford-cs324.github.io/winter2022/ |
| CS329A | Applied ML | https://web.stanford.edu/class/cs329a/ |
"""

files["ai_ml/transformer_models/transformer_references.md"] = """# Transformer Architecture & Attention Mechanisms

## Foundational Papers
| Paper | URL |
|-------|-----|
| Attention Is All You Need (2017) | https://arxiv.org/abs/1706.03762 |
| BERT: Pre-training of Deep Bidirectional Transformers | https://arxiv.org/abs/1810.04805 |
| GPT-3: Language Models are Few-Shot Learners | https://arxiv.org/abs/2005.14165 |
| T5: Text-to-Text Transfer Transformer | https://arxiv.org/abs/1910.10683 |
| Vision Transformer (ViT) | https://arxiv.org/abs/2010.11929 |
| Swin Transformer | https://arxiv.org/abs/2103.14030 |

## Modern LLM Architecture
| Resource | URL |
|----------|-----|
| Llama 2 Paper | https://arxiv.org/abs/2307.09288 |
| Mistral 7B Paper | https://arxiv.org/abs/2310.06825 |
| Anthropic Claude Research | https://www.anthropic.com/research |
| OpenAI Research | https://openai.com/research/ |
| Google DeepMind Papers | https://deepmind.google/research/ |

## Training & Optimization
| Resource | URL |
|----------|-----|
| Scaling Laws for Neural Language Models | https://arxiv.org/abs/2001.08361 |
| FlashAttention | https://arxiv.org/abs/2205.14135 |
| QLoRA: Efficient Finetuning | https://arxiv.org/abs/2305.14314 |
| RLHF: Learning from Human Feedback | https://arxiv.org/abs/2203.02155 |
| DPO: Direct Preference Optimization | https://arxiv.org/abs/2305.18290 |
"""

files["ai_ml/llm_engineering/llm_engineering.md"] = """# LLM Engineering & Production

## Building with LLMs
| Resource | URL |
|----------|-----|
| LangChain Documentation | https://python.langchain.com/ |
| LlamaIndex | https://docs.llamaindex.ai/ |
| Hugging Face Transformers | https://huggingface.co/docs/transformers/ |
| OpenAI API Documentation | https://platform.openai.com/docs |
| Anthropic API Documentation | https://docs.anthropic.com/ |
| Ollama (Local LLMs) | https://ollama.ai/ |

## Prompt Engineering
| Resource | URL |
|----------|-----|
| Prompt Engineering Guide | https://www.promptingguide.ai/ |
| Anthropic Prompt Library | https://docs.anthropic.com/en/prompt-library |
| OpenAI Prompt Engineering | https://platform.openai.com/docs/guides/prompt-engineering |
| Chain of Thought Paper | https://arxiv.org/abs/2201.11903 |

## RAG & Vector Search
| Resource | URL |
|----------|-----|
| Retrieval Augmented Generation | https://arxiv.org/abs/2005.11401 |
| ChromaDB | https://docs.trychroma.com/ |
| Pinecone | https://www.pinecone.io/ |
| Weaviate | https://weaviate.io/ |
| FAISS (Facebook AI) | https://github.com/facebookresearch/faiss |

## Agents & Tool Use
| Resource | URL |
|----------|-----|
| AutoGPT | https://github.com/Significant-Gravitas/AutoGPT |
| CrewAI (Multi-Agent) | https://docs.crewai.com/ |
| Function Calling Guide | https://platform.openai.com/docs/guides/function-calling |
"""

files["ai_ml/generative_ai/generative_ai.md"] = """# Generative AI

## Image Generation
| Resource | URL |
|----------|-----|
| Stable Diffusion | https://stability.ai/ |
| DALL-E 3 | https://openai.com/dall-e-3 |
| Midjourney | https://www.midjourney.com/ |
| ComfyUI (Workflow) | https://github.com/comfyanonymous/ComfyUI |
| ControlNet | https://github.com/lllyasviel/ControlNet |

## Video Generation
| Resource | URL |
|----------|-----|
| Runway ML | https://runwayml.com/ |
| Pika Labs | https://pika.art/ |
| Sora (OpenAI) | https://openai.com/sora |

## Audio & Music
| Resource | URL |
|----------|-----|
| ElevenLabs (Voice) | https://elevenlabs.io/ |
| Suno AI (Music) | https://suno.ai/ |
| Whisper (Transcription) | https://github.com/openai/whisper |
"""

files["ai_ml/mlops/mlops.md"] = """# MLOps & ML Infrastructure

## Platforms
| Resource | URL |
|----------|-----|
| MLflow | https://mlflow.org/ |
| Weights & Biases | https://wandb.ai/ |
| Hugging Face Hub | https://huggingface.co/ |
| Replicate | https://replicate.com/ |
| Modal (Serverless ML) | https://modal.com/ |

## Deployment
| Resource | URL |
|----------|-----|
| Triton Inference Server | https://developer.nvidia.com/triton-inference-server |
| vLLM | https://github.com/vllm-project/vllm |
| Ray Serve | https://docs.ray.io/en/latest/serve/ |
| BentoML | https://www.bentoml.org/ |
"""

files["ai_ml/ethics_safety/ethics_safety.md"] = """# AI Ethics & Safety

## Research Organizations
| Organization | URL |
|--------------|-----|
| Anthropic Safety Research | https://www.anthropic.com/research |
| OpenAI Safety | https://openai.com/safety/ |
| DeepMind Safety | https://deepmind.google/discover/blog/category/safety/ |
| Center for AI Safety | https://www.safe.ai/ |
| ARC (Alignment Research Center) | https://www.alignment.org/ |

## Key Papers
| Paper | URL |
|-------|-----|
| Constitutional AI | https://arxiv.org/abs/2212.08073 |
| RLHF Paper | https://arxiv.org/abs/2203.02155 |
| Red Teaming Language Models | https://arxiv.org/abs/2202.03286 |
| Model Cards for Model Reporting | https://arxiv.org/abs/1810.03993 |
"""

files["ai_ml/research_papers/top_conferences.md"] = """# Top AI/ML Conferences & Journals

## Conferences
| Conference | URL |
|------------|-----|
| NeurIPS | https://neurips.cc/ |
| ICML | https://icml.cc/ |
| ICLR | https://iclr.cc/ |
| AAAI | https://aaai.org/ |
| CVPR (Vision) | https://cvpr.thecvf.com/ |
| ACL (NLP) | https://aclanthology.org/ |
| EMNLP | https://2024.emnlp.org/ |
| COLM (Language Models) | https://colmweb.org/ |

## Paper Archives
| Resource | URL |
|----------|-----|
| arXiv CS/AI | https://arxiv.org/list/cs.AI/recent |
| arXiv CS/CL (NLP) | https://arxiv.org/list/cs.CL/recent |
| arXiv CS/CV (Vision) | https://arxiv.org/list/cs.CV/recent |
| arXiv CS/LG (ML) | https://arxiv.org/list/cs.LG/recent |
| Papers With Code | https://paperswithcode.com/ |
| Semantic Scholar | https://www.semanticscholar.org/ |
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files.")

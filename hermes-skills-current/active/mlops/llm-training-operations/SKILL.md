---
name: llm-training-operations
description: Use when planning or troubleshooting LLM training runs across parameter-efficient fine-tuning, GRPO/RL training, distributed PyTorch/FSDP, memory optimization, checkpoints, evaluation loops, and production training runbooks.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [llm-training, grpo, rlhf, fsdp, pytorch, peft, finetuning]
    related_skills: [fine-tuning-with-trl, peft-fine-tuning, pytorch-fsdp, grpo-rl-training]
---

# LLM Training Operations

## Overview

This is the umbrella skill for operational LLM training workflows: supervised fine-tuning, parameter-efficient tuning, GRPO/RL training, distributed PyTorch/FSDP, memory tradeoffs, checkpointing, and verification. Historical narrow skills are preserved as references.

## When to Use

- A task asks how to train, fine-tune, RL-tune, or scale an LLM.
- You need to choose between LoRA/QLoRA/PEFT, full fine-tuning, GRPO/RL, or FSDP-style distributed training.
- A training run fails due to memory, sharding, checkpointing, distributed launch, reward functions, or unstable optimization.
- You need a reproducible training plan with validation and artifact handling.

## Routing

1. **Define the training objective.** SFT for imitation; DPO/ORPO for preference alignment; GRPO/RL for verifiable-reward reasoning or task policies; continued pretraining for domain adaptation.
2. **Pick the adaptation strategy.** PEFT/LoRA first for cost and iteration speed unless full fine-tuning is required.
3. **Choose scaling infrastructure.** Single GPU, multi-GPU DDP/FSDP, or serverless/cloud GPU based on model size, sequence length, batch, and checkpoint constraints.
4. **Build data and evaluation before launch.** Include smoke tests, tiny overfit, validation metrics, and final task-specific evaluation.
5. **Instrument the run.** Log hyperparameters, losses/rewards, memory, checkpoint cadence, and sample generations.
6. **Verify artifacts.** Confirm tokenizer/model compatibility, checkpoint loadability, inference behavior, and reproducibility notes.

## Labeled Subsections

### GRPO / RL training

Use for reward-driven reasoning or tasks with verifiable outcomes. Keep reward functions simple, inspect reward hacking, and validate on held-out prompts.

Reference: `references/grpo-rl-training.md`

### PyTorch FSDP / distributed scaling

Use when the bottleneck is model size, optimizer state, activation memory, or multi-GPU sharding. Verify launch configuration, wrapping policy, mixed precision, checkpoint format, and resume behavior.

Reference: `references/pytorch-fsdp.md`

## Verification Checklist

- [ ] Objective and training algorithm selected explicitly.
- [ ] Dataset format and validation split verified.
- [ ] Tiny run or overfit test completed before full training.
- [ ] Memory/sharding/checkpoint strategy documented.
- [ ] Final checkpoint loads for inference.
- [ ] Evaluation results and failure examples reviewed.

## Common Pitfalls

1. **Starting with full-scale runs.** Always smoke-test data and code first.
2. **Optimizing reward without inspecting behavior.** RL can reward-hack silently.
3. **Changing tokenizer/model artifacts inconsistently.** Save and reload the full artifact set.
4. **Treating FSDP as only a flag.** Wrapping, checkpointing, precision, and resume semantics are the real work.


## Consolidated Reference Index

The following formerly separate narrow skills have been absorbed into this umbrella. Load the listed reference file only when that specific provider, failure mode, or workflow detail is needed.

- `grpo-rl-training` → `references/grpo-rl-training.md`
- `pytorch-fsdp` → `references/pytorch-fsdp.md`

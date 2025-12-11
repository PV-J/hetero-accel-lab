# Bottlenecks and the Simple Scheduler

This note explains what a performance bottleneck is in the context of `hetero-accel-lab`, and how the simple scheduler identifies which accelerator is currently limiting end-to-end latency.

## What is a bottleneck?

In any pipeline, a **bottleneck** is the stage that takes the longest time and therefore limits overall throughput. Even if other stages are faster, the system cannot go faster than its slowest stage. [web:236][web:244]

In this lab, each accelerator (matrix, DSP, PQC) contributes some latency to the total. The bottleneck is the stage with the highest latency for a given configuration.

## How the simple scheduler works

The `SimpleScheduler` in `accel_system/scheduler.py`:

- Receives a dictionary of per-stage latencies from the system model.
- Ignores the aggregate `total` entry.
- Finds the stage with the maximum latency value.
- Returns the name of that stage and its latency.

The scheduler does **not** change the pipeline execution yet. It is an analysis tool that tells you “which accelerator is currently the slowest part of the system” for a specific run. [web:217][web:224]

## Using configuration to move the bottleneck

By changing the configuration knobs, you can intentionally shift the bottleneck:

- Increase `--matrix-size` to increase matrix work; the matrix accelerator tends to become the bottleneck.
- Increase `--dsp-window` to increase filtering work; the DSP accelerator tends to become the bottleneck.
- Keep `--matrix-size` and `--dsp-window` small so that fixed PQC costs are a larger fraction of total latency.

This behaviour illustrates a key systemization idea: architectural decisions and workload parameters determine which accelerator is the limiting resource at runtime. [web:221][web:252]

## How this connects to architecture writing

In future architecture or blog documents, you can:

- Use these runs as concrete examples of how bottlenecks shift as workloads change.
- Discuss how a more advanced scheduler might react (e.g., scaling out matrix resources or offloading more to DSP when it becomes the bottleneck).
- Extend the model with more realistic latency formulas without changing the high-level concept of “find the bottleneck from the latency breakdown”.

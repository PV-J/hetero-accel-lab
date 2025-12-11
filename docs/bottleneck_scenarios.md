# Bottleneck Scenarios: Compute vs Communication

This note summarizes two reproducible scenarios from `examples/compare_bottlenecks.py`:

- **Compute-heavy**: large matrix, high RF bandwidth → matrix tends to be bottleneck.
- **Communication-heavy**: same matrix, very low RF bandwidth → RF link tends to be bottleneck.

These scenarios demonstrate how changing RF bandwidth while keeping compute load constant can shift the system bottleneck from computation to communication, a classic trade-off in distributed and wireless systems. [web:278][web:283]

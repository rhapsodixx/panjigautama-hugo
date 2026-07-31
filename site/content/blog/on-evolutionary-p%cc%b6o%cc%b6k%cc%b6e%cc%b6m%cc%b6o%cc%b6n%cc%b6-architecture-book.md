---
title: "On Evolutionary Architecture Book"
date: 2023-12-29T13:40:13
lastmod: 2023-12-29T13:40:31
slug: "on-evolutionary-p%cc%b6o%cc%b6k%cc%b6e%cc%b6m%cc%b6o%cc%b6n%cc%b6-architecture-book"
draft: false
categories:
  - "Architecture"
---

![](/images/Pikachu-evolution-pixel.gif)

Evolutionary ~~Pokemon~~ Architecture is good architecture that adheres to the fitness functions of the company; **fitness function** terms emphasized by the authors help to define what characteristics define good architecture.

The author’s discussion revolves around evolvable change, a change that has little to no breaking changes to the existing feature or integration, and implementation coupling leaks.

The fitness function acts as governance or guidance of any changes because changes can happen anytime. Principles of principles are an alternative, but they tend to be impractical. Example of fitness function on Code Quality: Code has test coverage above 90%. On Resiliency: API is able to complete a transaction in under 10 seconds, even if there is network latency.

The concept of high cohesion and low coupling also (quite obvious, I would say) applies in architecture. The only evolutionary architecture is micro-services is not true, well-structured monolith exists, and it's irrelevant since, at the end of the day, it goes back to how well we defined the boundaries (refer to Bounded Context) as it will help to move pieces around when we do changes.

How to start assessing whether we are building in the right direction (read: good architecture) : **Identify Fitness Function** : critical architectural characteristics that help decision making, i.e., Security is non-negotiable for Regulated Companies.

References:

  * <https://www.amazon.com/Building-Evolutionary-Architectures-Automated-Governance-dp-1492097543/dp/1492097543/ref=dp_ob_title_bk>
  * <https://www.youtube.com/watch?v=m2ZlX1je3as>
  * <https://www.thoughtworks.com/insights/articles/fitness-function-driven-development>

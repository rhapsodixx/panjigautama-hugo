---
title: "Convergence as Tech Debt Safeguard"
date: 2023-08-23T11:57:15
lastmod: 2023-08-23T11:58:09
slug: "convergence-as-tech-debt-safeguard"
draft: false
categories:
  - "Management"
  - "Operational"
---

![](/images/9d8fa97f717b9f253324e88c39c99434.gif)

Managing technical debt is never an easy game. Even if we have ideas, we need to compare the impact with the product initiatives/feature that we need to build to ensure we stay strong on the product side and boost the business. So what to do? lo and behold : Diverge-Convergence, comes as one of the strategies.

![](https://panjigautama.com/wp-content/uploads/2023/08/ideas-2-1024x640.jpg)

Each Sprint diverged into two streams: shaping & building, execute convergence sprint every triples.

### **Divergence**

Divergence is a concept of splitting task assignments into two streams: Shaping and Building. Note that it doesn't mean that every sprint must have both streams at the same time; there might be a sprint that only has either building or shaping streams only.

Divergence is intended to set boundaries to ensure the engineer assigned as a builder (building stream) only focus on building feature while shaper (shaping stream) is helping builder to focus by handling the production bugs/inquiries for planning (i.e., requirements gathering, RFC, Post Mortem).

An exceptional case might be triggered in case of emergency i.e., critical bug fix that requires an engineer who happened to be a builder.

  * **Shaping**
    * Gathering requirements, RFC & PRD refining.
    * Production Bug fixing.
  * **Building**
    * Uninterrupted work on Product & Engineering initiatives.
    * For any production, issue bugs redirect to Shaper (engineer whos in shaping mode)



### **Convergence**

  * convergence is a sprint wrap-up, listening to feedback from various channels (i.e. slack, user complaint) and bringing bugs, critical tech debt & must-have improvements to zero
  * converge may have feature development if it's being carried over from the last sprint. no new feature work picked up during the convergence sprint unless exceptional.
  * prior to the convergence sprint, the engineer/TPM/product may allocate or plan the findings from the running sprint to be fixed during convergence.
  * all bugs or work is prioritized in the following categories:
    * P0 - Blocks Ship/All Hands on deck.
    * P1 - Critical Fixes & Technical Debt
    * P2 - Nice to Have
    * P3/4 - Things to look into but neither nice to have nor critical fixes.
    * P5 - Unscreened.
    * P6 - Investigation bugs that we are not sure if P4 or higher.
  * The expected output of the convergence sprint:
    * 0 bugs backlog
    * Engineering Initiative Deliverable



### References:

  * [Shape Up: Stop Running in Circles and Ship Work that Matters](<https://basecamp.com/shapeup>)
  * [BA (22/52): How Apple Plans Software (A Visual Guide)](<https://buildingromes.substack.com/p/ba-2252-how-apple-plans-software>)
  * [Why we transitioned from Sprints to Basecamp’s “Shape Up” methodology](<https://medium.com/adventures-in-consumer-technology/why-we-transitioned-from-sprints-to-basecamps-shape-up-f416114224e7>)
  * [BA (23/52): Apple’s Contrarian Approach to Convergence](<https://buildingromes.substack.com/p/ba-2352-apples-contrarian-approach>)
  * [Stop using Velocity! Use this metric instead](<https://medium.com/@michmich112/stop-using-team-velocity-use-this-metric-instead-f5688905f268>)

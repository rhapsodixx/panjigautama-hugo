---
title: "Talking about Runbook"
date: 2023-01-24T21:18:29
lastmod: 2023-01-24T21:19:09
slug: "talking-about-runbook"
draft: false
categories:
  - "Documentation"
  - "Management"
---

![](/images/AchingIncompleteBetafish-size_restricted.gif)

### Why do we need a runbook?

the alert is only a signal, the very first step; reducing [MTTR](<https://www.splunk.com/en_us/data-insider/what-is-mean-time-to-repair.html>) and solving the customer problem is the ultimate goal;

an actionable alert is one of the repetitive tasks; Adding a runbook for the repetitive task will help to increase debugging, accuracy, and efficiency in the triaging process.

### But.. what exactly is runbook?

A **runbook** is a series of steps and detailed instructions to solve common issues or tasks effectively.

Most of the time, we run into escalated issues or production alerts where we need to solve and figure out a solution or the root cause as fast as we can. This problem-solving typically involves a quick search into the logging or reporting tools (at [TipTip](<https://tiptip.co/>) : Grafana/Loki/Sentry), third-party log (Payment Gateway, SMS provider, Fraud Tools), asking a coworker, or even asking for help from other different departments (Data team). These procedures are nontrivial, require experience or self-initiative, and surely take time. Runbook comes to help to ensure we have an effective problem-solving process, no matter how new or experienced the person on the team is.

### Ok, I got it, so when should we use Runbook?

At tiptip, runbooks are extremely helpful for two kinds of operations:

  * Incident response operations
    * runbook for specific alerts or incidents is needed to become documentation and ensuing shared knowledge from the Subject Matter Experts (i.e. engineer from the specific pod/squad)
    * with detailed runbooks, there is less need for escalation, and the team can function with L1 on call
  * Engineering operations
    * , i.e., Infra Maintenance, Operation that doesn’t have a feature yet (bulk user suspension)



### Clear! How do I create a runbook for our team services alert?

At TipTip, we have our own **Production Incident Runbook Template** on confluence, just create a new page and choose the template.

![](https://panjigautama.com/wp-content/uploads/2023/01/bc338fab-075a-4dba-b2e2-8551e2b61fa7-1024x557.png)

### References

  * <https://gitlab.com/gitlab-com/runbooks>
  * <https://about.gitlab.com/handbook/about/on-call/>
  * <https://pages.eml.atlassian.com/rs/594-ATC-127/images/Whitepaper-On-Call-Book.pdf>
  * <https://thechief.io/c/blameless/having-on-call-nightmares-runbooks-can-help-you-wake-up/>
  * <https://www.pagerduty.com/resources/learn/what-is-a-runbook/>
  * <https://www.amazon.com/DevOps-Handbook-World-Class-Reliability-Organizations/dp/1942788002>

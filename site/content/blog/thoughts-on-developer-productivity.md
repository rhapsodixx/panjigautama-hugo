---
title: "Thoughts on Developer Productivity"
date: 2023-11-15T07:29:59
lastmod: 2023-11-15T17:37:11
slug: "thoughts-on-developer-productivity"
draft: false
categories:
  - "Management"
  - "OKR"
  - "team"
---

![Color Cycling in Pixel Art | by Stephen Schroeder | Prototypr](https://miro.medium.com/v2/resize:fit:512/1*nYbbM6V6ZJmlmUToZmLNTw.gif)

I used to have a dream to work at a consulting giant until a few years ago. I worked with a bunch of them, as my parent company decided to hire one of the consulting companies, and they gave me nothing but a mess (Duh! 🙄). A while back, I stumbled upon this ["Yes, you can measure software developer productivity"](<https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/yes-you-can-measure-software-developer-productivity>) article from the consulting giant, and it sparked debate in a lot of tech blogs/newsletters.

I'm not going much into the critique of the article, as there are things that we, as a startup, can take from the consulting approach. 2020 onward has been a year where the hyper-growth vs profitability is no longer a conundrum. Industry, especially the software engineering team, is going through "normalization." Engineering leaders are being asked to do more with less (read: budget, manpower) compared to the hyper-growth era, which induces the need for the Engineering Leaders to explain how valuable is the engineering team in a quantifiable manner to the company. I won't go much into the details on how complex it is to measure engineering team impact on the company; Gergely Orosz and Kent Beck have a great article on that. Here are a few takeaways that I used to craft the productivity measurement at TipTip:

  * Measuring outcomes and impact is not enough as there are other factors (effort spent, deliverables)
  * Individual performance does not directly predict team performance
  * Team performance is more straightforward to measure than individual performance
  * Existing frameworks complement each other: DORA, SPACE, [DVI](<https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/developer-velocity-how-software-excellence-fuels-business-performance>)



Going back to TipTip, as a growing startup with a sizeable number of team members, TipTip needs measurement metrics for the engineering team to ensure everyone has effective work in hybrid mode (WFH+WFO), a fair workload, and gets contribution recognition based on data. Thus, we came up with metrics called **Engineering Delivery Proxy Metrics.**

These metrics are proxy metrics. It's not meant to be black and white performance rating. Engineering manager calibration and 360 feedback are still needed for performance justification. 

Category| Metrics| Definition| How to Track  
---|---|---|---  
Communication, Satisfaction & Well-Being| Engineering Satisfaction Survey| How fulfilled developers feel with their work, team, tools, or culture; How healthy and happy they are, and how their work impacts it| An average number of pull or merge requests merged by one developer in one week.  
| Async Contribution Recognition| Expression of recognition and gratitude toward peers.| [Employee Recognition](<https://heytaco.com/features/peer-to-peer-recognition>), alternative for HeyTaco: [GitHub - chralp/heyburrito](<https://github.com/chralp/heyburrito>)  
Efficiency| Merge Frequency| Average number of pull or merge requests merged by one developer in one week.| Gitlab API  
| PR Pickup Time| Time a pull requests waits for someone to start review. Low pickup time ~= Good review process.| Gitlab API  
| PR Review Time| Time it takes to complete a code review and get a pull request merged.| Gitlab API  
| Approved PR| Numbers of PR that contributed (review, comment) and approved| Gitlab API  
Quality and Predictability| Shift-Left Metrics| Measures bug slipped from shift left testing scenarios| QA Manual Tracking  
| Planning Accuracy| The ratio of planned work vs what actually delivered during sprint or iteration.| TPM manual tracking  
  
References

  * [SPACE Framework](<https://queue.acm.org/detail.cfm?id=3454124>)
  * [DORA Metrics](<https://docs.gitlab.com/ee/user/analytics/dora_metrics.html>)
  * [2023 Software Engineering Benchmark Report](<https://linearb.io/resources/software-engineering-benchmarks-report?utm_source=ByteByteGo&utm_medium=email&utm_campaign=Newsletter+-+Paid+-+ByteByteGo+-+2023+Benchmarks+Report>)
  * [2023 State of Engineering Management](<https://jellyfish.co/resources/the-state-of-engineering-management-in-2023/>)
  * [Measuring developer productivity? A response to McKinsey](<https://newsletter.pragmaticengineer.com/p/measuring-developer-productivity>)
  * [What McKinsey got wrong about developer productivity](<https://leaddev.com/process/what-mckinsey-got-wrong-about-developer-productivity>)

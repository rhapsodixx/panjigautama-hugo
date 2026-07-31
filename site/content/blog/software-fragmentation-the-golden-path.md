---
title: "Software Fragmentation - The Golden Path"
date: 2021-08-25T09:29:07
lastmod: 2021-08-25T09:32:07
slug: "software-fragmentation-the-golden-path"
draft: false
categories:
  - "Code"
  - "Management"
  - "Operational"
  - "team"
  - "Tenet"
---

![](/images/32f8ee1f68495231452451a2edfe9b7b.gif)

There is a direct correlation between teams that give their engineers autonomy to own their technical decisions and the team's ability to hire and retain A-class or Senior talent. There is a tradeoff, but an acceptable level of chaos in exchange for a stronger sense of individual/team ownership is usually the right one and leads to higher performing teams in the long run - at least this is what I've been seeing if a couple of companies in Indonesia.

So, how to make sure these "chaotic" things are manageable and actually give the benefit to the team? 

Here are the [seven steps inspired by this post](<https://charity.wtf/2018/12/02/software-sprawl-the-golden-path-and-scaling-teams-with-agency/>)

  1. Assemble a small council of trusted senior engineers.  

  2. Delegate them to list existing components/dependencies/tools for developers to use when building out and managing new services.  

  3. Scrutinize the list together with the council, weed out the poor/not-so-right-anymore component, the result should be list of recommended default components. This will be the Golden Path, or the path of convergence (and the path of least resistance) as the post said.  

  4. Inform to your team, through all-hands and sharing sessions, that the golden will be fully supported by engineering team (and the org may have dedicated team to support) and the golden road will be paved including libraries, upgrades, security fixes, monitoring, or even tier 1 on-call support.   
  
It's not going to be a MUST have components, but if engineers end up of using something else, the service/feature will be considered as insignificant feature, or technical debt/poor decision due to unforeseeable reason.   

  5. Work with all team leads to lay out plan (e.g. migration plan) for adopting the golden path; identify the gap between existing implementation and the golden path. Remember to allocate dedicated engineering team on this, believe me that you won't get anything done with just "spare time".   

  6. Work with the council to identify potential custom generic component / wrapper / libraries (e.g. Logging Library, API Gateway, Circuit Breaker) based on the gap identified by team leads & gap with the desirable architecture.   

  7. Set cutoff date for the support on component outside of the golden path, establish review process to get feedback and iterate on the golden path itself. Remember that gold should be polished regularly to keep it shine.



The intention of the golden path is not isolation of options, after all, there is no silver bullet for every engineering problem. The intention is to balance between optimizing locally for the problem in the team and optimizing globally for operability and maintainability (and sanity).

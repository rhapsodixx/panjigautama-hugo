---
title: "Software Estimation"
date: 2024-03-12T15:07:25
lastmod: 2024-03-12T15:08:08
slug: "software-estimation"
draft: false
categories:
  - "Code"
  - "Management"
  - "Project"
---

![](/images/0ec368d72828dc9509c66b7600a86ed7-1.gif)

You may be surprised that we are not able to give an estimation as well as we think, and you may be more surprised that not all of the software engineers are able to estimate (properly), most just guesstimate with rough intuition. Though it's not completely wrong, we can actually learn how to estimate properly. If you are graduated from Computer Science major like me, you will remember that software estimation technique is one of the courses by itself.

First, let's start on why software estimation is important in business or software development. 

## #importance of software estimation

  1. **💰 Decision Making**  
Estimation which is considered a Development Effort will be taken as one of the proxy metrics for business decisions. A lot of reasons, but ultimately development effort means cost and time to market.   

  2. **🤼‍♂️ Coordination**  
Estimation is not being used only for decision-making, once done, the estimation needs to be taken as a reference by another department e.g. marketing, sales for their campaigns, program, or even sales strategy.  

  3. **🌋 Risk Management**  
Estimation of the dev effort, especially for bug fixes, important feature improvements, or even strategic project where it has to be done, is also used to manage the risk that may happen during development or during the deployment process.



Now that everyone aligns that estimation is indeed important, the team also needs to be aware of the common estimation pitfalls.

## #common estimation pitfalls

  1. **📝 Misaligned Estimation Checklist**  
If you and others within the same team have a different estimation for simple tasks like "deploy new DB schema", this is a symptom of the misaligned checklist. Most likely steps that you plan to do for the simple task are different from the other person, which is worth discussing with the team. It's a best practice to have the same alignment on how to do a certain things/task, e.g. use an opinionated template for RFC, or runbook for deployment.  

  2. **🫨 Uncertainties Not** **Included**  
If you are familiar with the term postmortem, you may already hear about premortem, if you don't - I strongly suggest you practice this process with your team. During estimation, we need to account for the numbers of the uncertainties, when the uncertainties are revealed or things more clearer, the estimation can be re-estimated to get a more confident estimation.  
  
See this reference on the cone of uncertainty to get a bigger picture of how uncertainty affects estimation/cost.  

  3. **🎯 Estimates considered Deadline**  
It's a pitfall that commonly happens around us. Estimates need to stay true to the definition, once it considers precise numbers, it turns into the deadline. The deadline is ok, as long as justified and aligned by the team. Taking estimates as a deadline is totally not cool, as it wastes everyone's effort to estimate things.



## #estimation

![](https://lh7-us.googleusercontent.com/HJ208UDbHvrO_sec6Ze4X5tAII9lZLbGEjJgGvhMh5FmLLK9iIMqH03wWnrADvXr38a_tsfFrjPALGxVugUZq-FHDQ_uJuTE6KdKGlrnLzA-EHESBeXz74vOnTxzggNULLu4zuYbimu0ycUgNhFGWqkewg=s2048)

we are all aware of the importance of estimation, so it's also important for us to ensure we are getting a confident estimation. Estimation itself can be classified into 3 types:

  1. **Ballpark/Rough  
** Typically this is done in the early phase of the project where there are a lot of uncertainties. Accuracy might really be off and considered inaccurate. The time to do this estimation should be very fast or not worth it at all.  

  2. **Budgetary**  
Budgetary typically is done once the project has more things to share, e.g. solid product requirements and accuracy somewhat accurate. The team has more strong confidence to deliver within the estimation.  

  3. **Definitive**  
This is the estimation that is being done where a lot of things are clear e.g. high fidelity design, RFC/ADR/Tech Doc has been reviewed. Estimation should be fairly accurate and can be used as an estimation of other departments' planning.  




Now, there are a lot of ways to do software estimation which I have mentioned here <https://www.slideshare.net/slideshows/software-estimation-strategy-technique/266609835>, but I also suggest reading a post from Jacob, [he mentioned interesting part where it best for us to track our estimation accuracy and find a way to improve it over time](<https://jacobian.org/2021/may/25/my-estimation-technique/>).

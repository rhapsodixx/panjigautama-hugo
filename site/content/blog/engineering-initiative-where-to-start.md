---
title: "Engineering Initiative, where to start?"
date: 2021-03-18T11:31:04
lastmod: 2021-03-18T11:43:07
slug: "engineering-initiative-where-to-start"
draft: false
categories:
  - "OKR"
  - "Tenet"
---

Performance improvement we must do, but where to identify it? Sometimes this kind of things might not obvious as they are, as experience and frame of reference from each of the individual engineer within your team might vary. 

This post intended to share questions and framework that I've been using (and pushing) to my team to give cue and where to start on finding room for engineering improvements.

We start with very basic [Minto Pyramid](<http://www.barbaraminto.com/>) framework to help us have clear written thoughts of problems & solutions.

Steps| Action| Remark| Sample| Tips  
---|---|---|---|---  
1| Situation| Explain context and story on what is the current bottleneck / painpoints in problem statement| For 3 quarters Payment platform including Mobile API has been performing slow and lot of downtime despite of good business around it.| Get insight from product manager, engineering in day to day activities, and get from overall engineering metrics ( e.g. APM, Latencies )  
2| Complication| Explain real root cause / problem in details along with metrics as data / evidence based on the problem statement| QTD availability 85% with Payment service related trx endpoints 95-percentile latencies on 2 secs. QTD no sprint achieve 80% story points. Legacy stack on python has been slowing team down due to limited knowledge on python & angular.| Fishbone diagram  
3| Questions| Ask a question that will define your objective which will you use for resolution| \- how can we improve Messaging platform availability ?  
\- how can we improve latencies on SMS related endpoints to 200 ms ?  
\- how can we achieve steady story points deliverable within the team?| Use 5 why's / 3 why's  
4| Resolution| Based on problem & complication define initiative that answering objective| \- Migrate existing python & angular to golang & react to improve confidence and support on tech stack. Backed with monorepo and high maturity in golang will significantly help the team during development and incident.  
\- Perform database refactoring & indexing to improve latencies to 150ms  
\- Implement tracing & monitoring to improve availability and incident response, currently Payment Team have limited observability ( only limited log )| Try to come up with mutually exclusive and completely exhaustive resolution plan  
  
List of the initiatives could be on google sheet or docs, or whatever documentation that works for your team. Then we move to the next 2 steps :

  1. **Identify where we are today in terms of Engineering Metrics  
**  
I wrote engineering metrics that [I personally usually track here on this link.](<https://panjigautama.com/engineering-north-star-metrics/>) Generally speaking it's going to be revolve around Apdex, Latencies, Availability, and [Internal Service SLA](<https://cloud.google.com/blog/products/devops-sre/sre-fundamentals-slis-slas-and-slos>).  

  2. **Follow up questions and drill down on #1 metrics**  
  
I personally use [12factor](<https://12factor.net/>) , and service tenets [[1]](<https://www.infoq.com/articles/microservices-design-ideals/#:~:text=For%20object%2Doriented%20design%20we,%2Dcoupling%2C%20and%20single%20responsibility.>) [[2]](<https://opensource.com/article/18/4/guide-design-microservices>) [[3]](<https://www.researchgate.net/publication/310759471_Microservices_tenets_Agile_approach_to_service_development_and_deployment>), and these following questions to start evaluating our services.



**Agility**

  * Any bottleneck on development ? which part taking long time on WIP e.g. testing, CI/CD, env creation 
  * Any operational issue that often needs to be taken care by dev ? ( silent productivity killer ) 
  * Any repetitive things that can be automated ( automation debt )
  * How fast is your lead / deployment time ?



**Availability**

  * What is your current system availability ? 
  * Is your system hosted in proper instance configuration / type ? 
  * How well is the monitoring & observability on the system at the moment ? 
  * What is the current number on the production incident ? 
  * Which part contributing the most : response vs resolution time



**Performance**

  * How is your current number on latencies ? 
  * What is your current min - max RPS and what is your system capacity ? 
  * Hows the forecast look like ? 
  * What is your current error rate ? 
  * Which component / part contribute the most ? Any SPOF on your architecture ? What is your top most crash/error on sentry ?



**Security**

  * What is your current infra state on infrastructure vulnerable scan ? 
  * Is your system exposing / storing PII data ? 
  * how well is your access management ? 
  * What is the current number on the security incident ? which part contributing the most : response vs resolution time
  * whats your score on SAST scan (e.g. rubocop, php cs sniffer)



**Automation**

  * What is your unit test coverage at the moment ? 
  * how confident are you to fix things without having QA manual to test ? 
  * What is your UI test coverage ? 
  * is your team able to spot functionality issue quickly ?

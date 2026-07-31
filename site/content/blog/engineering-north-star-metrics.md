---
title: "Engineering North Star Metrics"
date: 2021-01-09T12:11:10
lastmod: 2021-01-09T12:11:10
slug: "engineering-north-star-metrics"
draft: false
categories:
  - "Code"
  - "Management"
  - "OKR"
  - "Tenet"
---

In the world where all of the metrics are available to be fetch and tracked, we end up on too many things being measured or worst, too little things that are being measured. It is impractical to make smart decisions based upon all available data and impossible to make any decision without data, and virtually impossible to make every metric as a priority worthy of improvement. The first challenge is deciding on what to measure, this article is intended to propose following metrics as the de jure metrics that being tracked and constantly improved going forward within tech team that I led so far.

![](/images/bbbb5235-0cb1-4767-9d80-52cb4d8dcea2.png)The 4 Layers of A Team

**Objective**| **Key Results**  
---|---  
**Tech & Infrastructure**| Improve and maintain _System Availability_ 1 and _Reliability_ (_MTTR 2_)  
**People & Organization**| Improve _Employee Engagement 3 _& Reduce _Churn Rate 4_  
**Observability & Security**| Increase observability on _monitoring_ (_Dashboard_)5, _alerting (Business and Engineering Metrics 6), and protect customers from security vulnerabilities (Security Tickets7)_  
**Productivity**|  Improve and maintain predictability on the sprint (_Sprint Velocity 8_) and _product quality (number of Bugs 9)_  
  
_1 System Availability by pinging the health check endpoint, the secondary metric would be Apdex (Application Performance Index), my favorite tools would be either Elastic APM or Datadog_

_2 MTTR, mean time to recover tracked through technical support ticket and post mortem chronologies_

_3 Employee Engagement tracked by the people operation / HR team_

_4 Churn Rate tracked by the people operation / HR team_

_5 Dashboard tracked in single monitoring tools: my favorite would be either ELK stack or Datadog_

_6 Engineering metrics are pushed to Datadog from AWS CloudWatch, agent on the application instances, and various integrations, Business Metrics also pushed as custom metrics. Logs are are pushed to centralized logging tools. Alert needs to be actionable and all critical alerts need to be a push to PagerDuty._

_7 Security Tickets, created through the following sources: Black Box (Bug Bounty, Vulnerability Scanner Tools, and Penetration Testing) and White Box (Static Code Analysis Tools)_

_8 Sprint velocity, tracked by Technical Program Manager along with other productivity metrics_

_9 Number of Bugs is bugs that are produced during a sprint, comes with granular metric including Number of Bugs back to Dev, tracked by Technical Program Manager / Scrum Master_

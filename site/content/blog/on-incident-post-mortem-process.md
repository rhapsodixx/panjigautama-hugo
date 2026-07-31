---
title: "Incident & Post Mortem Process"
date: 2021-02-07T12:50:06
lastmod: 2021-02-07T12:58:26
slug: "on-incident-post-mortem-process"
draft: false
categories:
  - "Operational"
  - "Stability"
---

![](/images/1f35bd89034764d07136e71c41265190.gif)This article is part of **On Managing Stability** series.

Recurring incidents are the enemy of scalability. Recurring incidents steal time away from our teams - time that could be used to create new functionality and greater value. Our past performance is the best indicator we have of our future performance and our past performance is best described by the incidents we have experienced and the underlying problems that caused those incidents.

Failing to recognize and resolve our past problems means failing to learn from our past mistakes in either architecture, engineering, process, and operations, and also communication.

![](https://panjigautama.com/wp-content/uploads/2021/02/d44df4d8-6ba6-48f4-941a-361bdfe4d0f0-1024x399.png)Incident Management Workflow

### **Incident**

To keep everyone on the same page on the definition of an incident, at Mekari we refer to well-known ITIL as a reference. The ITIL definition of an incident is “Any event which is not part of the standard operation of a service and which causes, or may cause, an interruption to, or a reduction in the quality of that service”, or to keep simply “Any event that reduces the quality of our service”

### **Post Mortem**

A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring. This article defines the guideline and official process on how we manage post mortem at Mekari. We shared the same philosophy with google on post mortem “The primary goals of writing a postmortem are to ensure that the incident is documented, that all contributing root cause(s) are well understood, and, especially, that effective preventive actions are put in place to reduce the likelihood and/or impact of recurrence.”.

The post mortem process requires effort from the team to ensure that we achieve the principle, hence we need guidance on choosing when to write one.

### **Post Mortem Triggers**

Common post mortem trigger may include any incident that related but not limited to:

**When to Write PostMortem**| **When to Not Write PostMortem**  
---|---  
\- Unexpected User-visible downtime or degradation beyond a certain threshold (~5 mins or apdex < 0.8)  
  
\- Data loss or Security Breach of any kind  
  
\- Escalation from On-call engineer related to P0   
  
\- Escalation from monitoring tools (e.g. Datadog, Pager Duty) related to P0| \- Scheduled maintenance / deployment failure that doesn't impact downtime  
  
\- Escalation from Technical Support or Customer Service for P1-P3 Bugs that has no user-visible downtime or major degradation (apdex < 0.8)  
  
### **Post Mortem Template**

Mekari has an opinionated post mortem, intended to have same template across mekari engineering team to ensure cross pollination knowledge. Post Mortem available as a template in our Confluence.

![](https://panjigautama.com/wp-content/uploads/2021/02/screencapture-sleekr-atlassian-net-wiki-spaces-814196484-pages-1984004097-Post-Mortem-Template-2021-02-07-12_45_48-514x1024.jpg)

**References :**

  * The Art of Scalability
  * Google SRE Book

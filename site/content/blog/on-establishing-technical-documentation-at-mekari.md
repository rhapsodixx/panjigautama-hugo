---
title: "On Establishing Technical Documentation at Mekari"
date: 2021-03-04T10:21:42
lastmod: 2021-03-04T10:26:18
slug: "on-establishing-technical-documentation-at-mekari"
draft: false
categories:
  - "Documentation"
  - "Management"
---

**  
**

![](/images/tumblr_mcfqj603fq1rfjowdo1_500.gif)

We all hate time wasters. Documentation often is seen as one of these time wasters, mostly because it is boring to do. Planning is often seen as kind documentation, so there is a natural tendency to just skip this step for efficiency. However, people forget the hidden cost of skipping this documentation step: no agreement on shared understanding may cause the project will take a lot longer than people think, and this is only the beginning of other disadvantages of not having proper documentation.

### **Introduction**

Being a software engineer or rather someone who's working in software and tech infrastructure, our main purpose is not to produce code or setup infrastructure per se, but rather to solve problems, and ultimately deliver the value of our product to our customers.

Documentation may be the better tool for solving problems and give clarity in a project lifecycle, as it may be more concise and easier to digest, and communicates the problems and solutions at a higher scale and wider audience than code.

Either large companies like Microsoft or smaller ones like Mekari, [there are two things related to planning that might always be there](<https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs/>).

  * lack of visibility on other building or having built the same thing across the team
  * the tech and architecture debt accumulated due to different teams building things very differently, both approach-wise and quality-wise



Fortunately, this isn't new things in software industries, successful companies have one common approach to solve this: Technical Documentation including its Review. This approach not only tackling visibility issues or reducing tech/architecture debt, but these steps also spreading knowledge and having engineers be more engaged day to day.

Documentation turn ideas into words. They force clarity: it’s hard to write tech documentation unless we are sure about what problem we are trying to solve, and why. They encourage us to think through all aspects of their design and to make and document decisions.

We build better systems when we work together. Having a written design allows other engineers to review those decisions. Reviewers may have opinions on whether the problem needs to be solved at all, or whether simpler approaches might work just as well. They may notice risks to the project, flaws in the design, or edge cases that won't work.

Throughout this document, we at Mekari call this technical documentation as **RFC — Request For Comments** , given the many similarities it has with the RFC process in the tech community. It's quite similar as well with ADRs, but comes with a broader scope: capturing architectural changes and non-trivial project.

RFCs, also called Design Documents / Technical Doc / Engineering Specification, are a common industry practice and for good reason. They give us a mechanism for reviewing each other’s ideas and describing our own.

### **Building RFC process that scales at Mekari**

RFC at Mekari is intended to solve the following challenges:

  * Be an upfront investment of time and effort that in the long run can create exponential payoffs for the product
  * Helping onboarding new engineers or engineers that confronted with a system that they hadn't previously touched.



While design docs, like all documentation, tend to get out of sync with reality over time, they still often present the most accessible entry point to learning about the thinking that guided the creation of the system.

  * Surfacing legacy work. RFC with design reviews, engineers can know that a particular technology problem had already been solved in the past and learn takeaways from it.
  * Productive contribution. Design reviews make it easy for a whole range of engineers to contribute thoughts towards a design. Often times little details are caught because someone with a different point of view jumps in.
  * Promote the concept that projects are a team effort



RFC (well..practically anything) without purpose will be a waste of time. Hence, it's important for us to know what is the purpose of our RFC, this will be varied depending on the problems that we want to solve and who's is our target audience for the documentation. This purpose will give us an idea of the level of detail on our RFC.

Here is a good reference that shamelessly taken from [Lyft engineering blog post](<https://eng.lyft.com/awesome-tech-specs-86eea8e45bb9>).

![](https://panjigautama.com/wp-content/uploads/2021/03/d3df9312-0617-4d15-af58-aa4ee8d4bf86-1024x351.png)

### **Opinionated RFC template**

As we want to make it easy and intuitive for people to do the right thing. It's important for us to give guidance to the team on what the RFCs should include. On the other hand, people who review many engineering proposals often had the same type of questions. Questions like "What is the motivation to do this work?" or "How will this be tested?" or "Will any architecture changes are made here?" were very common questions. These common questions worth to be included in the guidance to avoid things being oversight.

Due to those reasons, an **opinionated RFC template is preferred**.

However, note that the RFC process is an iterative process, its important for us to get people to feedback and iterate our process time to time to ensure we have an effective and efficient process. The functional team e.g backend and frontend (mobile/web) might have different sections within the plan since each has its unique part (e.g. mobile/web have UI/UX).

### Checklist / Should I write an RFC?

We use this simple checklist, if the answer YES to any of the questions below, engineer expected to create RFC  

![](https://panjigautama.com/wp-content/uploads/2021/03/Screen-Shot-2021-03-04-at-10.17.41-1024x661.png)

## When NOT to use RFCs

RFCs can be a great tool for driving change across a company. As we’ve seen, they give us a structured way to document a transformation, get buy-in from teammates and evaluate the results. However, they’re not a one-size-fits-all tool, and there are a few scenarios where we shouldn’t create full-blown RFC (some level of tech documentation is obviously still needed). Please always refer to checklist above.

  * **When the change is so small it doesn’t warrant a full-blown discussion.**  This can be the case for instance with small implementation changes for existing initiatives. At the end of the day, engineer set this boundary, but make sure to use personal judgment.  
e.g. changes on the API parameters or API resources  

  * **When the change has a limited scope (i.e. it only affects another person in a team of the company).**  In this case, the engineer probably better off discussing the change with the individuals involved directly rather than trying to capture all the details in advance.  
e.g. changes on the API payload JSON  

  * **When engineer don’t actually care about the feedback.**  We strongly encourage people to own their aspects of the business here at Mekari and we give them all the freedom they need to do it. If the engineer feels very strongly about a choice and the engineer can validate it easily and with little to no repercussions, then just go for it. Our experience mileage may vary, always consult with the engineer's tech lead.

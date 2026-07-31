---
title: "My Ex-Boss Cultural Hints"
date: 2021-01-02T09:46:38
lastmod: 2021-01-02T09:47:32
slug: "my-ex-boss-cultural-hints"
draft: false
categories:
  - "Management"
---

_⚠️ This isn’t my note nor intent to take any credit._

TL;DR: We take our job of building quality services for our customers seriously in every way. Rigor at every level is the only way to do that reliably and efficiently. 

#### **TTT - Try Three Things**

Don't reach out to others unless you have tried a reasonable number of things first. Not only will this stop you from task-switching others, but it will slowly build up your expertise in our tools and procedures. Most of the time, you'll find the answer to your question by the time you've tried that third thing - without bothering somebody else. This is our equivalent of "LMGTFY". Of course, don't go overboard and unproductively go into a black hole of learning everything yourself - that would be the fourth thing and be a waste of time too. 

#### **Dates and Goals**

As a prior CEO of mine once said, "We have goals. Those goals have dates. But be very careful about letting the date _become_  the goal. You will go down paths you regret if you do that." Remember that we're here to produce quality experiences for our customers and we're here for the long term.   Sure, there are some high-profile dates that actually have a meaningful impact on the company, such as a conference or a key funding date or partnership commitment. But most other dates are just somebody's best guess 18 months ago - and your guess now is probably a lot better.  The best dates are given either with 50% achievability (internal and team goals) or 70% achievability (public and business goals).  Of course I want to get things done. We move fast here. But I will never tell you to produce buggy software to make a date. You personally own this reality for your own work, your manager owns it for their team's work - and so on.  If you break it at your point in the chain and tell untruths, it's broken at every level above you.  And it won't get better with time. 

#### **Focus on your unique value first before helping others too much**

What's the best definition of Teamwork you've ever heard?  What about "Get your job under control before reaching out to help others"? People who offer to help others while their job is not under control can create a spiral where nobody in an organization is actually on top of their work, but they're all being oh-so-helpful. It is also a refuge for people who are struggling in their own job, to find something they can be viewed as being valuable at.  This doesn't mean to be a jerk - we should all help each other. But meter that help against whether you're getting your own job, your own special individual contribution, done well. 

#### **AAA - Anticipate, Analyze, Answer**

When you write an email, re-read it before you send it, through the eyes of your readers. If you see an obvious question, so will your readers. Analyze the problem enough to answer that new question and then answer it in your email. Repeat until you think you've answered the questions at a reasonable level of depth. For example, by sending an email (especially a status email), you are spending a lot of people's time for them to read and understand.  Partially, they want to know the actual details of the project. But for the most part, they want to know that you're on top of it. If you write a wishy-washy summary, you will get responses that sound like they are requests for details. But what they most likely are is votes-of-no-confidence on your running of the project. By answering all reasonable follow-on questions to a reasonable level of depth, you inform effectively, cut down on email churn, and show your readers you are managing your work rigorously.

#### **DDD - Dates, Dates, Dates**

_Everything_   should have a date. Don't send an email that says you're "working with the widget team to figure out how to make their new API work with our code" unless you have a date of when that will be done - and include that date. Or a date for when you think it will be done. Or even a date for when you think you'll know a date for when it will be done. Emails or updates or decks that end without dates can be a huge waste of time.  AAA/DDD go together, because many things that are unanswered in poor status reports are what the next step is and when it will be done. 

#### Brilliant and Well Intentioned

Working together to get work done is a lot about working with people. People work best together when they feel respected, both for their intent and for their capabilities. As we grow as leaders and contributors, we often find that we retain early instincts we had in our career - that somebody who holds a different point of view or who even outright disagrees with us must not be as bright as we are, or must have poor intentions. It's actually irrelevant whether that's true or not. If you treat the person you're working with as if they aren't brilliant and well-intentioned, your chances of success approach zero. On the other hand, if you treat people as if they are brilliant and well-intentioned (and you must really believe it or all your body language and tone gives you away), you have a chance to get things done. This is because you are working together as a team - well-intentioned, and you're both good at your jobs - brilliant. Given these ground rules, you can align on what's best to delight our customers, respect our stakeholders, and fulfill our employees. 

#### Unclear Commitments are the Root of a lot of Evil

We all have a lot of things to do. And we get asked to do more things "urgently", and "ASAP", all the time. The problem is that if you accept an ASAP item silently or incorrectly, you're betraying everybody around you. If you had lots of spare time in your day, you must be working in some other industry than Tech, so we really don't expect that. So for any ask, you need to think about it like this: 

  1. You (the Person in Charge) needs figure out whether to do (and appropriately prioritize) Project P for Requesting Person R? (If you're not the PIC of this task, hand off cleanly to the real PIC). 



2a) If Yes, commit to Project P, with Target Timeline T, and outline the Impact I to other projects that have already been committed (if any).

2b) Update Project P status towards completion, including updating Target Timeline T, probably weekly, and communicate as appropriate.

  1. If No, explain why you can't or won't do your part of Project P, and figure out a way forward - either it doesn't get done, gets done on a different timeline, or we change the goalposts.



**RCA - Root Cause Analysis**

When bad things happen, that's ok. What's not ok is not changing things so it doesn't happen again. This doesn't mean we go after every single thing that happens in the code or fleet once, but it sure means that when it happens a second time, you look into it. We have a lot of folks who have never worked on either enterprise or distributed software, or only did it at school. So they think blaming the subsystem is actually a root cause. Don't settle for "the EBS volume was stuck", or "Service XXX threw a 500." Ticket EBS and follow up, even if it eventually lands you talking to Leslie Lamport about TLA and the unproveability of algorithms that depend on 2-member quorum or debugging a kernel mode device driver. Don't just close the ticket. Go get the service code and look into it - or get somebody who does know the code involved. The definition of a complete Root Cause Analysis is that there is no more investigation needed to have somebody start figuring out how to solve the problem. Sometimes, a cultural problem with RCAs is that "nobody has time". That's a false choice - if a problem is going to come back time and time again, somebody sometime is going to have to fix it - you're saving time by starting to solve it now. If doing a good RCA causes you not to be able to do other parts of your job, talk to your manager about how deep you should go or whether it should be given to somebody else - but don't drop it silently. 

#### **There Are No Ghosts**

This principle ties together with RCA. As much as we all like to blame things on gamma rays, one-off timing considerations that will never happen again, AWS network deployments, etc, there is a real cause with a real solution to every single thing to happens to our software. At our scale, not only will most one-off things actually happen again, but if we get much bigger, we're going to have to start worrying about gamma rays :-)  Software systems, like chemical reactions between molecules, are both deterministic and hard to monitor precisely.  Just because you can't figure out why a variable got set to something doesn't mean that an instruction didn't set it in a piece of code that looks just fine. If you get to the end of a problem where you have nowhere else to go, add monitoring, alarming so that next time you can get closer to the root cause.  But never ever write off a problem to random chance  \- there are truly no ghosts in computer science. That's why it's called a science. 

#### **Build Mechanisms**

There are always problems, and that's ok, and even repeated occurrences of the same problem. People often have good intentions to fix them - but good intentions don't work. When something is bad enough to require your attention multiple times, isn't it bad enough to want you to take the time to build a self-correcting feedback-based mechanism so that this will get better over time and then stay within an acceptable operating range without supervision?  Whether this is something as simple as weekly emails to raise the visibility of bad things happening or code that actually stops deployment, initiates rollbacks and blocks deployments whenever it sees a watched metric go into alarm, we must have mechanisms. The overall goal is to put something in place that continues to fix a problem and make it better without humans being involved. 

#### **BMWS. Be More Worried - Sooner**

The truth is that most things you think are going well in your group probably aren't going as well as you wish - and the things you know aren't going well are probably going a lot worse than you care to admit. What does this mean?  Whenever you sniff smoke of a fire possibly happening, don't analyze the urgency of the issue based on the smoke - realize that the fire is probably much worse than the wisp of smoke that made it to you.  And very few software fires go out on their own. Projects described to you as yellow are probably red, and most green-ish projects are actually yellow. Work to get projects to "bright green" in order to deliver projects that will delight your customers - even if you have to deliver less of them.

#### **Your Job is to Get To Yes**

When you're asked whether you can do something, your job is not to say "No", if you can't do it. It's to remove the boundaries of constraints and explore what it would take to get to "Yes". Maybe those constraints are impossible - but maybe they aren't. Discussions which start with "No" shut down innovation and creative thought. The leaders who are asking you for a deliverable that is really hard (and may well be impossible) don't have the same information on the ground that you do - and a short answer that only contains "No" sure doesn't change that. So rather than just saying "No", you add value to the room by giving all the possibly crazy ways you can get to "Yes". Most of the time this ends up in us either getting to a very different "Yes" than the impossible crazy thing that was asked for or even sometimes with everybody in the room understanding that "No" is indeed not only the choice one person is making, but the right choice for the business and our customers. We can hire lots of people who can say "No". Instead, add value to the company and our customers by figuring out the right "Yes."

**Embrace the Post-Mortem**

Post-Mortem are our way of acknowledging that something went wrong and the mechanism for how to get it fixed. As Jeremiah, one of the most senior engineers I've ever met at Amazon, liked to say: "At Amazon, one of the only times that you get to call out everything you'd like to fix and actually be rewarded for it is in connection to a COE (Amazon's equivalent of a Post-Mortem). Most other times you'll get either grudging approval or the dreaded 'how important is this to revenue/adoption-producing feature X?' question, which as we all know is just unanswerable."  So when things go wrong, open a post-mortem. Be vocally self critical as much as you need to, but focus more on the actions you will take to fix the problem. We make lots of mistakes because we move fast and because we'd probably make almost as many if we moved slowly. But ones that make it to having a customer-impacting negative effect are the worst. Use the company culture to your advantage to produce the code and service and customer experience you will be proud of, in a group that has the culture you want. 

**You must hold the Tiger's Tail until you hand it to somebody else**

Ownership is a hard thing to fully understand. Think of walking down the street in a city you care about and seeing a piece of garbage. Ownership is picking it up, even though you were on your way to a meeting, and putting it into the trash. But it doesn't stop there. Maybe the piece  of trash is stuck to the sidewalk - then ownership is taking a note and calling the street cleaner and getting acknowledgement that they will fix it. In other words, once a problem is identified, it shouldn't be let go again. Think about it as a wild tiger, a dangerous beast - you're awesome and you've managed to grab the tiger by the tail. But it's not your tiger. You can't tame it or subdue it. So do you let it go, assuming somebody else will grab it? No - a true owner wouldn't let the tiger tail go - it will just go hurt somebody else - a true owner would find somebody who can actually fix the problem and hand it the problem (the tiger's tail) carefully and rigorously to them. So ownership includes both the initial finding of a problem and a reasonable degree of following through. When you see something wrong, you owe to everybody else what you expect from them - that you'll be on top of it, or find somebody else to own it, so that it gets fixed, and entropy doesn't win. 

#### **It's All in the Semi-Colon**

Amazon has a principle that guides people to stand up when needed by to back down appropriately as well - in the best way for the company. This principle is called "Have Backbone; Disagree and Commit". The key to this principle is to _balance on the semi-colon_.  We don't want sheep - people who lean too fast to the right of the semi-colon. But we also can't have people who stay to the left of the semi-colon too much - and have backbone unproductively. A good book for you if you're having problems here is "Crucial Conversations", and if things really get bad, "Crucial Confrontations".  It is not acceptable to not say what needs to be said for the sake of social cohesion, but it's even better if you manage to say what needs to be said productively. In our culture, we may bias even more strongly towards being respectful and kind than the brash American culture I grew up in - and that's awesome. That just means we need to have a higher bar for figuring out how to say the important things that need to be said - nicely and respectfully.

#### **Respect Others. No matter what**

Take care of people just as well on the way down or out as on the way up or in. We treat people with respect during PIPs (Performance Improvement Plans), meeting with them regularly and going above and beyond. If we or they decide this company or group isn't the right place for them, we make sure we publicly announce them leaving and send out encouraging words publicly to make sure that everybody knows that transitions out are just as important as transitions in. 

#### **Don't let entropy win**

In the absence of people making things better, they will get worse. Pages will get outdated, method signatures will become convoluted, regression tests won't work, etc.  It is the expectation of every employee that they put some reasonable amount of effort into fixing things. So when you visit a wiki page that is valuable to you but see problems with it, leave it slightly better. When you see code that could use some comments, add them.  This small tax (5%? 10%?) more than pays for itself if you live in a culture where most people do this. Sometimes people don't fix things because they think their managers or product managers won't prioritize this work; but teach them the value of great code, great docs, and great products. 

#### **The Onion of our Requirements**

We need to always make sure we prioritize our requirements correctly.  In order, we think about Security, Durability, Availability, Scalability (Scale-out), Features, Performance (Scale-Up), Efficiency. What this means is that for each item on the left side, it is more important than the items on the right side. For example, if we had to, we would give up availability of the data (shut the servers down) rather than risk it being deleted (loss of durability). The two that are often debated are the relationship between Scalability and Performance. The reason I place them in this order is that if we have the ability to scale out arbitrarily, we won't be at risk of having our workload become impossible to run - but if we only have single-node scale-up, we could be trapped in a solution that doesn't scale to fit our needs.  Of course we want both.

#### **Delighted Mistakes**

The power of _delighted mistakes_ is huge. When I was in Amazon, when we messed up sending somebody a package, sent it to the wrong place, or sent them the wrong thing, and they contacted us, we could fix it. That's the low bar - anybody can do that. But we could do better. We could pick up the "call me now" button in 15 seconds or less with the customer's messed up order already up on our screen and make them feel cared for, even though we messed up. We could fix it in a way that absolutely delights our customer; we could tell them to keep the wrong thing, we could refund them the whole purchase price, and we could send them the correct one overnight express - for free. We could send an apology letter from Amazon to the person who didn't get their gift on time. _Correctly handled, a mistake is actually one of our best opportunities to create longterm loyalty from our customers._   For our part of the world, (transport/food/logistics/payments), this is really hard. When you've lost a customer the ability to go to work, cost them credibility with their customers by failing to deliver something, or lost them money or availability during a peak time, it's almost impossible to delight. But we can fix that in the same way retail does; we can respond quickly, we can refund/credit without being asked, we can make them feel like they are the single most important customer we have. Delight is the bar, even (especially?) when you've messed up. At least for me, that makes my job more meaningful. I hope that holding this bar high makes your job more meaningful as well.

#### **The Iron Pentagram**

You're often asked to pull in dates. Think about it - if you're doing the right things, in the right order, with the right level of quality, with the right people, and you're giving them the right support, then _the date is the date._  If you want to change the date, then figure out which of the 5 sides of the pentagram to change. Please ask your leaders to not "Just ask for a new date". Educate them that they'll get a new date, but it will be wrong. Help brainstorm through the constraints of the project rather than the optical date at the end. 

#### **Hope/Think/Know**

One of the worst things a senior member of the team can do is misrepresent something they _hope is true_  as something they _think is true_  or even worse, _know is true_. Other members of the team will make decisions based on that surety - and those decisions will likely be wrong.  In order for us to make good decisions, everybody needs to be clear about their level of confidence of every statement that will affect a decision. Don't over-represent your optimism about an architecture or project, and don't under-represent it either.

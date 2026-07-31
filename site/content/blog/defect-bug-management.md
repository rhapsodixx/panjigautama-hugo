---
title: "Defect/Bug Management"
date: 2021-11-17T08:30:33
lastmod: 2021-11-17T09:56:06
slug: "defect-bug-management"
draft: false
categories:
  - "Management"
  - "Project"
  - "Tenet"
---

![](/images/JadedPointlessBufeo-size_restricted.gif)

who doesn't love bugs? they are small yet beautiful...ly ruining our life 🙂. Bug is inevitable, choosing 0 Bug as your OKR/KPI is an insane choice, it's not impossible but it will astronomically hit your productivity & cost, your best bet is to manage it properly. So how are you organizing and managing these bugs? Assigning the right priority(by assessing its severity) is the key, inspired by a couple of references, here is how I typically categorize them.

## **Severity**

  * **P0 - Critical:** The defect affects critical functionality or critical data. It does not have a workaround. Example: Unsuccessful installation, complete failure of a feature.



Look at this NOW, fix ASAP within tolerable. This priority should typically be tied together with an on-call rotation so that someone gets alerted. Services going down, significant parts of functionality going unavailable, major security problems — these sorts of things should result in a P0 bug. P0 bugs should be rare enough to warrant a formal review process around what caused the problem, its discovery, fixes applied, and lessons learned.  
System down, service unavailable, feature blocked.

  * **P1 - Major:** The defect affects major functionality or major data. It has a workaround but is not obvious and is difficult. Example: A feature is not functional from one module but the task is doable if 10 complicated indirect steps are followed in another module/s.



Fix within 24 hours. Examples include significant flaws in the product, bugs that affect a subset of the user base, bugs that impact the brand in a significant way.

  * **P2 - Minor:** The defect affects minor functionality or non-critical data. It has an easy workaround. Example: A minor feature that is not functional in one module but the same task is easily doable from another module.



Fix within a sprint. Minor problem, but it would be good to get fixed before the next major release of the feature goes out.

  * **P3 - Trivial:** The defect does not affect functionality or data. It does not even need a workaround. It does not impact productivity or efficiency. It is merely an inconvenience. Example: Petty layout discrepancies, spelling/grammatical errors.



Catchall priority for things that should go into the next sprint. Expect these bugs never to be looked at unless they get upgraded to P2s. Different teams prefer to have these lying around because they are documentation of everything wrong or delete them because they are mostly useless.

Note that Priority != Severity, priority can be based on the magnitude of bug (e.g. # users, # of app version affected) or based on violation quota and SLA.

## **SLA Violations Quota**

![0_C14v-T2y-r9ryPVF.jpg](https://codahosted.io/docs/hrSRgWRxsW/blobs/bl-eOo35CGo1V/4c0d80aec76765d4de96168ef1f2e6e40dadaa514a0678158bd711c237c6939becd126325ec68d78efdb1cb3bc4de17cb3b3608c73ee20a5d58eeae7324d1cf4a09b8f0bf55e392711dc7676d95c104dfd01c9638f68ab8636265f60ed03bc97a2fae412)

  * P0: No outstanding bugs. If you have a P0 bug, stop all feature development until you have fixed that bug.
  * P1: A small number, say 0.25 / engineer.
  * P2: You should expect a fair number of these bugs and give teams room to get these under control — say 3 / engineer.
  * P3: Unbounded.



## **Bug Management**

![1520104050183.jpg](https://codahosted.io/docs/hrSRgWRxsW/blobs/bl-fA5sralvgj/95ca3e626c2f0990f84f778d5eb1f58cb87b9ffbedc374471fab084206894c600512e0757e24a05cab3ddd27eba9e3580d94b6836469cd3849e9f9d5c6cf4f69bddebd80edbda027edb606d82a877cf2b7840a9d8bf3ed99207144cf96245ba92cc183b3)

references

  * <https://softwaretestingfundamentals.com/defect/>
  * <https://medium.com/swlh/software-quality-bugs-and-slas-3d4a6bf7aa5e>
  * <https://www.lambdatest.com/blog/bug-severity-vs-priority-in-testing-with-examples/>
  * <https://www.linkedin.com/pulse/defect-resolution-slas-skip-dragoo/>

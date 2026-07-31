---
title: "Standardizing FrontEnd development at Mekari"
date: 2021-01-02T09:54:59
lastmod: 2021-01-02T09:56:35
slug: "standardizing-frontend-development-at-mekari"
draft: false
categories:
  - "Front End"
---

### TL;DR

**VUE as a first-class frontend framework at Mekari.**

React is a perfectly reasonable tool for building front ends, and we are not claiming it’s bad. In Mekari’s case, Vue has a couple of strong points based on decision principles. which may or may not change in the long future.

*note that there is no silver bullet in software engineering, this decision needs to be a review on a periodic and case-by-case basis to ensure the decision is to solve the problem, not being biased by personal preference. To minimize subjectivity and bias into framework decision, we use the following criteria:

### Decision Principles (sorted based on criticality):

#### Flexibility, Templating vs JSX

React excel in this principle, but Vue able to cater Mekari needs*  
  
Given that Mekari has a lot of product lines with different purpose and behavior, our chosen framework would need to present a range of configuration options and be relatively simple to customize. Given the relatively medium codebase that we have in our core products which currently split into multiple stand-alone products (e.g. talenta, jurnal, klikpajak).  
  
React is a library for building composable user interfaces, works out of the box due to its flexibility to offer flawless integration however, there are chances of wrong decisions and dependencies due to its complexity. Vue is the cleanest framework in comparison to all. It helps to keep our code efficient with the balance of internal dependencies and flexibility. It is simple, straightforward, and a framework that aims to simplify web development.  
  
Also good to note that React offers great flexibility with a price: the [paradox of choice,](<https://en.wikipedia.org/wiki/The_Paradox_of_Choice>) which can make things hard for newcomers, and a higher chance of introducing higher complexity if things not set up right from the beginning.

*One of the key differences between the two frameworks is the way they handle templates. However, in the end, the choice between JSX and templates comes down to personal preference. JSX can feel more powerful and flexible while templates offer a clear separation of concerns preventing us from injecting too much logic into views. On Mekari’s case, we favor the latter one: clear separation of concerns.  


#### Simplicity / Maintainability

Vue excel in this principle.

Vue has[ wonderful docs](<https://vuejs.org/v2/guide/>) and its API references are one of the best in the industry. They’re well-written, clear, and accessible dealing with pretty much everything we need to know to create Vue applications. Just like React, the docs are translated in several languages in addition to English. For better or worse, Vue is more opinionated than React with many issues having a clear answer in the docs. When dealing with legacy code, Vue is more of an ideal solution because it can be grafted onto existing HTML markup and DOM content in-place with almost zero development effort or prerequisites. [Couple of case studies ](<https://cdn2.hubspot.net/hubfs/1667658/State_of_vue/State%20of%20Vue.js%202019.pdf>)suggested that their codebase is easy to maintain, test, and share across multiple applications after migrated to Vue from other frameworks (angular, react).

#### Performance

Tie.

React and Vue has a Virtual DOM. Both provide great performance and memory allocation, as it has a well-built structure. Both libraries have tiny bundle sizes which speed up the initial load (31 KB for Vue/84.4 KB uncompressed and 32.5/101.2KB for React). Note that Performance mainly relies on the size of the application and optimization of the code, we shouldn’t judge a library’s performance based on benchmarks alone

Out of the box, both libraries have:

  * server-side rendering (SSR);  
**Vue**  is ahead of React with its in-built SSR capabilities and [a detailed guide](<https://ssr.vuejs.org/>) right in the documentation. **React** , on the other hand, needs third-party libraries like [Next.js](<https://nextjs.org/>) to render pages on the server.
  * tree shaking; and
  * bundling.  
  
<https://stefankrause.net/js-frameworks-benchmark8/table.html>  
_*Keyed implementations create an association between the domain data and a dom element by assigning a 'key'. If data changes the dom element with that key will be updated. In consequence, inserting or deleting an element in the data, array causes a corresponding change to the dom._



**Duration in milliseconds ± standard deviation (Slowdown = Duration / Fastest)**

![](/images/vue-1.png)

**Startup metrics**  
lighthouse with mobile simulation

![](/images/vue-2.png)

**Memory allocation in MBs ± standard deviation**

![](/images/vue-3.png)

####   
Learning Curve

Vue excel in this principle.  
  
React is renowned for its steep learning curve, Angular’s learning curve is much steeper. Before you can really get started, you need to know about JSX and probably ES2015+, since many examples use React’s class syntax. You also have to learn about build systems, because although you could technically use Babel Standalone to live-compile your code in the browser, it’s absolutely not suitable for production. While Vue scales up just as well as React, it also scales down just as well as jQuery.  
\-- <https://vuejs.org/v2/guide/comparison.html>

Many have [claims ](<https://www.sitepoint.com/vue-right-framework/>)seen juniors with no prior Vue experience get productive in a matter of hours, and many projects fall apart after a few years of React when the senior dev leaves the company it all falls apart. Due to these criteria, we put aside the concern on shortage of Vue talent in the market.

* * *

### React and Vue

One of the biggest differences between Vue and React is the way the view layer is built. By default, Vue uses HTML templates, but there’s an option to write in JSX. In React, on the other hand, there’s solely JSX. Vue’s traditional separation of concerns into HTML, CSS, and JS makes it easier even for beginner frontend developers to learn how to create Web applications. HTML templates are also familiar to most Web designers, and thus improve collaboration between developers and designers. React’s JavaScript Expressions (JSX) combine HTML and CSS together into JavaScript. This XML-like syntax lets developers build self-contained UI components with view-rendering instructions included.

![](https://panjigautama.com/wp-content/uploads/2021/01/vue-4-843x1024.jpeg)

Few companies that use React are Facebook, Instagram, Netflix, New York Times, Yahoo, Whatsapp, Codecademy, Dropbox, Airbnb, Atlassian, Intercom, Microsoft, Slack, Storybook. Companies that use Vue are Xiaomi, Codeship, Reuters, Adobe, Alibaba, WizzAir, EuroNews, Grammarly, Gitlab, and Laracasts, Behance.

Vue, despite the fact that it is initially a “one-man-show”, it can grab the attention of developers due to its stocky and trouble-free architecture. is gaining exponential adoption with a strong reason.

![](/images/vue-5.png)

### Challenges

Choosing a framework or adopting any standardization on existing products obviously require changes here and there (read: refactoring). KlikPajak fortunately has been started with Vue since the very beginning, however, Talenta & Jurnal has various frontend frameworks at the moment (e.g. react, bootstrap). In order for us to maximize the value of standardization and avoid overengineering / improvement with low-to-zero business value, we are going with the following guidance:

  * Invest in creating a web component with Vue for Mekari UI (Detail TBD)
  * Any new frontend feature / UI need to adopt Mekari UI with Vue, unless there is a technical constraint that requires another framework, this requires approval from engineering lead.
  * Any Mekari UI adoption is strongly encouraged to use Vue web components, this might mean refactoring the feature to Vue



References:

  * <https://stackoverflow.blog/2020/02/03/is-it-time-for-a-front-end-framework/>
  * <https://www.monterail.com/blog/vue-vs-react-2020>
  * [https://www.doodleblue.com/blogs/angular-vs-react-vs-vue](<https://www.doodleblue.com/blogs/angular-vs-react-vs-vue?utm_source=AVR%20Blogs&utm_medium=Quora%20Answers&utm_campaign=Quora_Best>)
  * <https://www.mindk.com/blog/react-vs-vue/>
  * <https://stefankrause.net/js-frameworks-benchmark8/table.html>
  * <https://www.simform.com/react-vs-vue/>
  * [https://cdn2.hubspot.net/hubfs/1667658/State_of_vue/State of Vue.js 2019.pdf](<https://cdn2.hubspot.net/hubfs/1667658/State_of_vue/State%20of%20Vue.js%202019.pdf>)
  * <https://medium.com/better-programming/when-to-use-vue-over-react-9a4e0f01e064>

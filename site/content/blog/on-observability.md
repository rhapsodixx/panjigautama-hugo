---
title: "On Observability"
date: 2021-09-12T19:46:30
lastmod: 2021-09-12T19:50:04
slug: "on-observability"
draft: false
categories:
  - "Code"
  - "Operational"
  - "Stability"
---

![](/images/sniper.gif)

Running an application without having a proper monitoring is akin to driving without a dashboard. You don’t really know if you still have enough gas, or if you are within the speed limit, or how far are you till your next oil change. There are many uncertainties involved in running an application. Monitoring is instrumental in getting first hand awareness on possible incident or help predict that an incident is about to happen so we can prevent it.  


This post outlines some observables that we can monitor and setup alert for along with some recommended practice.

## Observables

Things we can observe related to a running application. Observables can help us monitor and diagnose issues.

  1. **Application Errors**. There are many ways to report errors. The simplest one is using an error reporting platform like Sentry or Firebase Crashlytics. Alternatively you can also log your errors and check it via log management tools.  

  2. **System Uptime/Downtime**. The most straightforward way we measure our system availability. You can use uptime SaaS product (e.g. uptimerobot, freshping) to periodically check if an application is up and running and how long has it spent on downtime within a period of time.  

  3. **Infrastructure Metrics**. If your application runs on the server side, you might want to monitor stuff like resources (CPU, Memory, Disk, network throughput) usage, how many machines/container are running, or what zone are they running from.  

  4. **Traces**. Trace can be used to track down operations that spans multiple components, how long it takes to complete each step, and if it fails, which part gives the error. Datadog have tracing library than can be used to instrument you application (you can also use OpenTracing with Datadog). Alternatively, you can assign a uuid to every request that flows through the system and put the uuid every time you write a log message.  

  5. **Performance Metrics**. If you care your application performance, you should track stuff like latency, error rate, number of requests, and Apdex. You can use popular tools like new relic, datadog, or Elastic APM to get this metric.  

  6. **Business Metrics**. Business metrics is the kind of metrics that business people usually cares about on the feature/application. It is usually taken care by using analytics tool such as Google Analytics. However such tools is usually not integrated to the monitoring & alerting pipeline and serve more as a business intelligent tool.



Every application have a different business metrics. Some examples are number of transactions or successful login. Setting up your own business metrics monitoring can be really helpful in giving you insight on you application’s health.

## Health Check

Health check API is one of the most common way to check if an application is running well. For a web application, the simplest form of a health check is usually just visiting the front page and see if it loads. The better way to do it is by providing a dedicated health endpoint.  
  
For monitoring and uptime measurement purpose, it is recommended to check connectivity to core dependencies as part of the health check. A core dependency is defined as **a hard dependency that exist solely as part of that application**. The most prominent example is the application’s database.
    
    
    {
      redis: {
        connected: true
      },
      db: {
        connected: true,
        migrations_updated: true
      }
    }

Obviously you don’t want to check every single dependencies. The reason being is that your application should be able to run and retain some of its functionality even if part of the dependencies is down.

### **Health Check and Kubernetes Liveness Probe**

If your application is deployed on a container orchestration system that make use of liveness probe (e.g. Kubernetes), you might be tempted to use your health check endpoint as the liveness probe. While it could work on paper, **it is probably best if you use a separate dedicated endpoint for liveness probe**. The reason being, if your health endpoint also checks for dependencies, your liveness can fail when one of your dependency is failing.  
  
To see why this can be a problem, liveness checks is used by Kubernetes to check if the process in the container is alive. When liveness check fails a certain amount of time, it will attempt to restart the container hoping that restart can fix it. However, if you are using health endpoint and it fails because your DB is down, Kubernetes will restart your container when in fact the process is actually running well.

## Signal to Noise Ratio

Alerts are helpful. However, in the midst of our passion to not miss any single indication that our application might be in trouble, sometimes we can get carried away and setup an overly sensitive alerts. In the end, we end up flooding our inbox or Flock channel with superfluous alerts which is more of a noise than signal.  
  
We want there to be more actual signal (true positive) than noise (false positives or unimportant events) in our alerting system. A low signal to noise ratio means that there are more noises to your alerting system than there are signals. This is dangerous because people will be so used to the noise that they could care less to actually check the alerts anymore.  
  
In order to avoid this, we need to design our alerting rules to avoid useless alarm. However, there’s an art in balancing our rules so that we are not getting alerted when it is already too late; What’s the use of an alarm if it only goes off after our customer yells at us? We cannot totally eradicate all the noises, but we can at the very least work on minimizing them.  
  
The following practice can help out in reducing the noise and keep us alerted on the important things:

  * For error reporting, don’t alert for every single event. Instead:  

    * Alert for an issue regression (closed issue is happening again).
    * Alert if the same error happens more than X time within the past 10 minutes.
    * Alert if the total number of errors within the past 10 minutes exceed Y times.
    * Alert if there are Z users encountering error within the past 10 minutes.


  * For any time series metrics (e.g. CPU/memory usage, error rate, Apdex), avoid alerting whether the metrics cross a particular threshold a certain point of time. Instead:  

    * Use [anomaly monitoring](<https://docs.datadoghq.com/monitors/monitor_types/anomaly/>) feature if exist on your monitoring tools. It can adapt to the metrics behaviour in the past and detect if there’s any anomaly.
    * Alert if the metrics cross a relatively high/low threshold for an extended amount of time (15 minutes)


  * For logging alert, assign a proper log levels to any event you log. Different logging library may have different log levels. However, the most common one usually have FATAL, ERROR, WARN, INFO, DEBUG, TRACE.   
  
There are many excellent guide on which kind of events should be logged on which level. For the purpose of discussing signal to noise ratio we can categorize it like this:  

    * FATAL is alert worthy every single time
    * ERROR is alert worthy if happens multiple time within a short time span
    * WARN is alert worthy if happens in a large number within a short time span
    * The rest of log levels are not alert worthy.

Observables| Description| Alarm Rules  
---|---|---  
Application Error| Have application error reporting integrated. The following error must be reported.  
Backend Service: 5xx server error & fatal error that stops program execution  
Front End Web App: Uncaught exception on JavaScript  
Mobile App: Application Crash| Regressed issue  
The number of issue occurrence in the project within the last 5 minutes exceed a specified number.  
Service Downtime| Service uptime checks exist on UptimeRobot   
HTTP service: Checks via health endpoint.  
Background Worker or similar: Send heartbeat to uptime checker.  
Checks interval: 1 min| When the application goes down.  
When the application goes back up.  
Infrastructure Health| Host or container metrics can be observed at either Datadog or Grafana.  
The following metrics should exist:  
Usable memory & Memory usage  
Usable CPU cores & CPU usage| When resources usage cross a certain threshold within the last 10 mins  
If the service being monitored have a seasonality, then trigger alarm when there’s an anomaly in the seasonality.  
Traceability| The application have a capability of tracking down how request/events flow through the system.  
This can be achieved by either:  
Having trace instrumentation using Datadog/NewRelic  
Accepts request uuid and include when you log a message.| N/A  
Performance| Existence of service to monitor the following performance metrics:  
Request per second  
Request latency  
Apdex| Warning: When Apdex drops below 0.8 within the last 10 mins.  
Error: When Apdex drops below 0.5 within the last 10 mins.

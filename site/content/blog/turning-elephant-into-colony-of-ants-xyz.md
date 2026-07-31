---
title: "Turning Elephant into Colony of Ants - XYZ"
date: 2022-11-18T10:49:18
lastmod: 2022-11-18T10:50:10
slug: "turning-elephant-into-colony-of-ants-xyz"
draft: false
categories:
  - "Code"
---

XYZ is fictional product inspired by personal experience, that happen went into the journey of monolith to microservices.

![](/images/giphy.gif)

## #1 Context

### Problem Statement

XYZ Codebase has tech debt where the monolith majestically hosts mobile API and Web Backend at the same time. This Big system is highly susceptible to a changing environment. They're big and slow and unwieldy, tricky to scale horizontally (x-axis scale), costly to scale vertically (y-axis scale), and challenging to scale on the z-axis (e.g. serve multitenancy)

### Goal

The intention is to capture initiatives to ensure XYZ can scale following the Scale Cube model, decomposing the monolith into segmented services adhering to domain driven design to ensure we have clarity on Segregation of Duties between services. The expected outcome doesn’t necessarily be a microservices, it could be macro services as [AirBnB](<https://www.infoq.com/presentations/airbnb-services-scalability/>) did, but the final set of services needs to strictly follow y-axis scale design tenet :

  * Highly maintainable and testable - enables rapid and frequent development and deployment
  * Loosely coupled with other services - improved fault isolation, enables a team to work independently the majority of time on their service(s) without being impacted by changes to other services and without affecting other services
  * Independently deployable - enables a team to deploy their service without having to coordinate with other teams
  * Capable of being developed by a small team - essential for high productivity by avoiding the high communication head of large teams



## #2 Proposal

To put simply, as the intention is on moving off a legacy application to a more scalable codebase, we propose using the famous strangler pattern and creating a routing facade, we are avoiding big bang migration and should demonstrate value early and often in order to ensure that the business supports the migration effort. The routing facade or we call as a **strangler facade** , can’t be using existing API Gateway because it serve different purpose.

Components and their responsibilities on this scope:

  * **API Gateway on Kong SSO** : given current use cases it serves as a router from external service, and plan to use API management plugin to allow robust integration with the external services. This API gateway responsible as an edge function including
    * router - routing endpoints to the appropriate service based on the external service request
    * authentication – verifying the identity of the client making the request
    * authorization – verifying that the client is authorized to perform that particular operation
    * rate-limiting – limiting how many requests per second are allowed from either a specific client and/or from all clients
    * caching – cache responses to reduce the number of requests made to the services
    * metrics collection – collect metrics on API usage for billing analytics purposes
    * request logging – log requests  

  * **Facade Service** : Stand in the middle of API Gateway and Legacy Service and responsible for the following things:
    * router – direct requests to our monolith or new service from any calls from internal service
    * anti-corruption layer – As a service is rarely standalone. It usually needs to collaborate with the monolith. Sometimes a service needs to access data owned by the monolith or invoke its operations. This is where facade service plays an important role: isolate our new service from corruption by the legacy monolith. This layer can take multiple approaches depending on use case:
      * a) Invoke a remote API provided by the monolith
      * b) Access the monolith’s database directly, or
      * c) Maintain its own copy of the data, which is synchronized with the monolith’s database



There are multiple strategies for strangling the monolith and incrementally replacing it with microservices / macroservices. Two strategies that being proposed here on the document are:

  1. Implement new features as services.
  2. Break up the monolith by extracting functionality into services.



Ideally, we should implement every new feature in the strangler application rather than in the monolith. You’ll implement a new feature as either a new service or as part of an existing service. This way you’ll avoid ever having to touch the monolith code base. Unfortunately, though, not every new feature can be implemented as a service, that's why the second approach is needed and very important.

## #3 Issues and considerations

  * Consider using a programming language that lightweight (should avoid any big web framework like Laravel/Yii/Nuxt/Next( and has rich support of concurrency, supporting serverless approach to make sure the facade doesn't become a single point of failure or a performance bottleneck. (e.g. golang, python, java/micronaut/spring boot)
  * One way to minimize the impact on the monolith of extracting a service is to replicate the data that was moved to the service back to the monolith’s database. Because the monolith’s schema is left unchanged, this eliminates the need to make potentially widespread changes to the monolith codebase.
  * Structure of new applications and services in a way that they can easily be intercepted and replaced in future strangler migrations.
  * At some point, when the migration is complete, the strangler façade will either go away or evolve into an adaptor for legacy clients.
  * Make sure the facade keeps up with the migration

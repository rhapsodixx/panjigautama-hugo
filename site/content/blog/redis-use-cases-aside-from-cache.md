---
title: "Redis use-cases aside from Cache"
date: 2023-12-29T13:46:50
lastmod: 2023-12-29T13:46:50
slug: "redis-use-cases-aside-from-cache"
draft: false
categories:
  - "API"
  - "Architecture"
  - "Code"
---

![](/images/Pixel-Art.gif)

Redis can be more impactful aside from caching. Here are a few other use cases :  
1️⃣ As a persistent storage for use cases like shopping carts, user profiles, and social-media-related posts/newsfeeds. Easily sorted set simply by ZRANGE  
2️⃣ Tracking state with Bitmaps, easily track and get states with boolean logic with SETBIT and GETBIT  
3️⃣ Location Based with Redis geospatial, easily search and add geospatial data with GEOADD & GEOSEARCH. AFAIK it's quite tricky to do this with Postgre  
4️⃣ Distributed Lock, i.e., updating inventory stock to handle flash sale traffic  
5️⃣ Analytics Funnel with Probabilistic easily store event and or merge with the HyperLogLog  
6️⃣ Simple event-driven architecture with Redis Stream or as a Pub/Sub with SUBSCRIBE/PUBLISH commands, which can be seen as a message queue even with LIST

reference: [https://blog.bytebytego.com/p/redis-can-do-more-than-caching](<https://blog.bytebytego.com/p/redis-can-do-more-than-caching?utm_source=substack&utm_medium=email>)

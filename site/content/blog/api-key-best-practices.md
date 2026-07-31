---
title: "API Key Best Practices"
date: 2021-01-02T09:49:20
lastmod: 2021-01-02T09:49:34
slug: "api-key-best-practices"
draft: false
categories:
  - "API"
  - "Code"
---

API keys are required for apps and projects that being used across Mekari platforms, either GCP/AWS/Logging Tools or other third-party services. This document identifies the intended use of API keys, how to protect them as you would other credentials, and which restrictions are appropriate for your projects.

**Always try to adhere Principle of least privilege*.**

_*The principle of least privilege states that only the minimum access necessary to perform an operation should be granted, and that access should be granted only for the minimum amount of time necessary._

Guidance:

  * <https://developers.google.com/maps/api-key-best-practices>
  * <https://docs.datadoghq.com/account_management/api-app-keys/>
  * <https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html>



#### 1\. Don’t store your API key directly in your code. 

Embedding your API key in your source code may seem like a practical idea, but it’s a security risk as your source code can end up on many screens. Instead, store your API key and secret directly in your environment variables, however using Secret Management like VAULT or AWS KMS is strongly encourage. 

Environment variables are dynamic objects whose values are set outside of the application. This will let you access them easily (by using the [os.getenv() method](<https://www.geeksforgeeks.org/python-os-getenv-method/>) in Python, for example, or using [dotenv package](<https://www.npmjs.com/package/dotenv>) in a Node app), and avoid accidentally exposing a key when you push your code. 

Even private repositories can leave you vulnerable to hacks, so you should consider any API key exposed in any repository, public or private, as compromised. Instead, remove your API key and secret before publishing by using a [gitignore ](<https://git-scm.com/docs/gitignore>)file to specify files for Git to ignore or simply remember to hash your credentials before publishing. 

#### 2\. Don’t store your API key on client side. 

If you are developing a web app, remember to always store your credentials always on backend side. Fetch the API results from there and then pass them to the frontend. 

If you’re a mobile developer, it’s doubly important to store your credentials outside your app, as a seasoned user can easily reserve engineer your app and find your credentials. Try to store your API credentials on a separate server that you own and use that same server to fetch the API results before then passing them on to the client. 

#### 3\. Restrict your API Key.

You can best protect your API key by restricting it to specific IP addresses, referrer URLs or mobile apps, and specific APIs, as this significantly reduces the impact of a key compromise.

You can specify application and API restrictions for a key from the console by opening the Credentials page and then either creating a new API key with the settings you want or editing the settings of an API key. See the sample section from GCP [Restricting API keys](<https://developers.google.com/maps/api-key-best-practices#restrict_apikey>) for full details. 

On mobile apps that use APIs, consider one or more of the following techniques to further safeguard your API keys or signing secrets:

  * Use a proxy server. The proxy server provides a solid source for interacting with the appropriate Google Maps Platform API. For more information on using a proxy server
  * Obfuscate or encrypt the API key or signing secret. This complicates scraping of API keys and other private data directly from the application.
  * Use CA pinning or certificate pinning to verify the server resources are valid. CA pinning checks that a server's certificate was issued by a trusted certificate authority, and prevents Man-In-The-Middle attacks that could lead to a third party discovering your API key. Certificate pinning goes further by extracting and checking the public key included in the server certificate. Pinning is useful for mobile clients communicating directly with Google servers, as well as mobile clients communicating with the developer's own proxy server.For more information, see:
    * [Security with HTTPS and SSL](<https://developer.android.com/training/articles/security-ssl.html#HttpsExample>)
    * [Enforcing Stricter Server Trust Evaluation](<https://developer.apple.com/library/content/technotes/tn2232/_index.html#//apple_ref/doc/uid/DTS40012884-CH1-SECSTRICTER>)
    * [Certificate and Public Key Pinning](<https://www.owasp.org/index.php/Certificate_and_Public_Key_Pinning>)
    * [Repository of Documentation and Certificates](<https://pki.goog/>)



#### 4\. Use independent API keys for different apps & environment.

This limits the scope of each key. If an API key is compromised, you can delete and revoke the impacted key without needing to update your other API keys. Note that the development and production key must be a different keys.

#### 5\. Generate a new key if you suspect a breach 

Monitor usage of your API for anomalies. If you observe unauthorized usage, rotate your keys. If you think your API credentials have been compromised, keep calm, and simply revoke the key. Monitoring tools and rate-limiting alert should on the monitoring plans.

#### 6\. Delete unneeded API keys.

To minimize your exposure to attack, delete any API keys that you no longer need.

#### 7\. Regenerate your API keys periodically.

Always try to rotate your API keys periodically (e.g. every 90 days). Most of the Secret management tools provide this out of the box, however, we need to check on our code implementation.

**References** :

  * <https://learn.hashicorp.com/tutorials/vault/database-creds-rotation>
  * <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>
